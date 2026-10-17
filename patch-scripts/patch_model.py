import os

script_path = r'C:\Users\arkad\Downloads\INAV Configurator\package.nw\build\script.js'

with open(script_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace model_file = 'custom' with model_file = 'quad_x'
old_snippet = "if (MIXER_CONFIG.appliedMixerPreset === -1) {\n            model_file = 'custom';"
new_snippet = "if (MIXER_CONFIG.appliedMixerPreset === -1) {\n            model_file = 'quad_x';"

print("Count old snippet:", content.count(old_snippet))
content_modified = content.replace(old_snippet, new_snippet)

# Also check for alternate spacing
if content_modified == content:
    # try regex replacement
    import re
    content_modified, count = re.subn(
        r"if\s*\(\s*MIXER_CONFIG\.appliedMixerPreset\s*===\s*-1\s*\)\s*\{\s*model_file\s*=\s*'custom';",
        "if (MIXER_CONFIG.appliedMixerPreset === -1) {\n            model_file = 'quad_x';",
        content
    )
    print(f"Replaced {count} instances via regex.")

with open(script_path, 'w', encoding='utf-8') as f:
    f.write(content_modified)

print("Saved script.js successfully!")
