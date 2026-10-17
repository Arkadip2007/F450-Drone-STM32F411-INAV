with open(r'C:\Users\arkad\Downloads\INAV Configurator\package.nw\build\script.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = 2602786
print("Chunk 1:")
print(text[idx-50:idx+250])

idx2 = 2993776
print("Chunk 2:")
print(text[idx2-50:idx2+250])
