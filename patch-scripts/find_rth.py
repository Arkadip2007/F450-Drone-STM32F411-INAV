with open(r'C:\Users\arkad\Downloads\INAV Configurator\package.nw\tabs\advanced_tuning.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('rthAltitude')
print(text[idx-600:idx])
