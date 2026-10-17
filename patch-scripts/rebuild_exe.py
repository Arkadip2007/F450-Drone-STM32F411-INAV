import zipfile, io, os

orig_exe = r'C:\Users\arkad\Downloads\INAV Configurator\inav-configurator.exe'
fixed_exe = r'C:\Users\arkad\Downloads\INAV Configurator\inav-configurator-v2.exe'
nw_dir = r'C:\Users\arkad\Downloads\INAV Configurator\package.nw'

# 1. Read stub
with open(orig_exe, 'rb') as f:
    stub = f.read(2138112)

# 2. Build zip in memory
zip_buffer = io.BytesIO()
with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(nw_dir):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, nw_dir).replace('\\', '/')
            z.write(full_path, rel_path)

# 3. Concatenate stub + zip
with open(fixed_exe, 'wb') as f:
    f.write(stub)
    f.write(zip_buffer.getvalue())

print('Successfully created inav-configurator-v2.exe! Size:', os.path.getsize(fixed_exe))
