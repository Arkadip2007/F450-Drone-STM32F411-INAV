with open(r'C:\Users\arkad\Downloads\INAV Configurator\package.nw\tabs\configuration.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="magalign"')
print(text[idx-50:idx+600])
