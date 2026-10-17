python -c "
def parse_hex(filename):
    base_addr = 0
    records = []
    mem = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line.startswith(':'): continue
            count = int(line[1:3], 16)
            addr = int(line[3:7], 16)
            rectype = int(line[7:9], 16)
            payload = bytes.fromhex(line[9:9+count*2])
            if rectype == 0:
                full_addr = base_addr + addr
                for i, b in enumerate(payload):
                    mem[full_addr + i] = b
            elif rectype == 4:
                base_addr = int(line[9:13], 16) << 16
            elif rectype == 1:
                break
    return mem

def write_hex(mem, out_filename):
    addrs = sorted(mem.keys())
    cur_base = None
    with open(out_filename, 'w') as f:
        i = 0
        while i < len(addrs):
            addr = addrs[i]
            base = addr & 0xFFFF0000
            if base != cur_base:
                cur_base = base
                # Write type 4 record (Extended Linear Address)
                high_word = cur_base >> 16
                payload = bytes([(high_word >> 8) & 0xFF, high_word & 0xFF])
                chk = (0x02 + 0x04 + payload[0] + payload[1]) & 0xFF
                chk = (-chk) & 0xFF
                f.write(f':02000004{payload.hex().upper()}{chk:02X}\n')
            
            # Pack up to 16 contiguous bytes
            chunk = []
            while i < len(addrs) and len(chunk) < 16 and addrs[i] == addr + len(chunk) and (addrs[i] & 0xFFFF0000) == cur_base:
                chunk.append(mem[addrs[i]])
                i += 1
            
            offset = addr & 0xFFFF
            length = len(chunk)
            chk = length + (offset >> 8) + (offset & 0xFF) + 0x00 + sum(chunk)
            chk = (-chk) & 0xFF
            f.write(f':{length:02X}{offset:04X}00{bytes(chunk).hex().upper()}{chk:02X}\n')
        
        # EOF record
        f.write(':00000001FF\n')

src_file = r'.\stm32f411ceu6\INAV_Blackpill\INAV-Blackpill-Flight-Controller-main\inav_5.1.0_BLACKPILL_QUAD_SD_108.hex'
dst_file = r'.\stm32f411ceu6\inav_5.1.0_BLACKPILL_QUAD_SD_108_CUSTOM_MPU6050_PB6_PB7.hex'

mem = parse_hex(src_file)
min_a, max_a = min(mem.keys()), max(mem.keys())

# Patch 1: WHO_AM_I check at 0x08038C64
# Original: 02f07e02682a05f1ff338df80e2000f08e83
# New: cmp r2, #0x68 (682a) -> beq 0x080393DC (00f0b983) -> cmp r2, #0x98 (982a) -> beq 0x080393DC (00f0b583) -> subs.w r3, r5, #1 (05f1ff33) -> nop (00bf)
patch1_addr = 0x08038C64
patch1_bytes = bytes.fromhex('682a00f0b983982a00f0b58305f1ff3300bf')
for k, b in enumerate(patch1_bytes):
    mem[patch1_addr + k] = b

# Patch 2: I2C1 Pins at 0x08073CB4
# Original: 00540040 28 29 7500 (PB8, PB9)
# New: 00540040 26 27 7500 (PB6, PB7)
patch2_addr = 0x08073CB8
mem[patch2_addr] = 0x26     # PB6 SCL
mem[patch2_addr + 1] = 0x27 # PB7 SDA

# Patch 3: Motor 3 & Motor 4 in timerHardware at 0x080739C4
# Entry 2 (Motor 3): was PB6 CH1 -> change to PB8 CH3
# Offset 0x080739C4 + 40 = 0x080739EC
mem[0x080739EC + 4] = 0x28 # PB8
mem[0x080739EC + 5] = 0x02 # CH3
mem[0x080739EC + 16] = 0x02
mem[0x080739EC + 17] = 0x17 # DMA1 Stream 7 Channel 2

# Entry 3 (Motor 4): was PB7 CH2 -> change to PB9 CH4
# Offset 0x080739C4 + 60 = 0x08073A00
mem[0x08073A00 + 4] = 0x29 # PB9
mem[0x08073A00 + 5] = 0x03 # CH4
mem[0x08073A00 + 16] = 0x00
mem[0x08073A00 + 17] = 0x00

write_hex(mem, dst_file)
print(f'Successfully created {dst_file}')

# Verification
mem2 = parse_hex(dst_file)
print('Verifying Patch 1:', bytes([mem2[patch1_addr + k] for k in range(len(patch1_bytes))]).hex())
print('Verifying Patch 2 (I2C):', bytes([mem2[patch2_addr], mem2[patch2_addr+1]]).hex())
print('Verifying Patch 3 (Motor 3): Pin', hex(mem2[0x080739EC + 4]), 'CH', mem2[0x080739EC + 5])
print('Verifying Patch 3 (Motor 4): Pin', hex(mem2[0x08073A00 + 4]), 'CH', mem2[0x08073A00 + 5])
"