from pathlib import Path

ROOT = Path.cwd()

for name, heading, label in (
    ("README.md", "## Project status\n", "Current release: **1.4.1**\n\n"),
    ("README.pt-BR.md", "## Status do projeto\n", "Versão atual: **1.4.1**\n\n"),
):
    path = ROOT / name
    text = path.read_text(encoding="utf-8")
    if "1.4.1" not in text:
        if heading not in text:
            raise RuntimeError(f"README heading not found in {name}")
        text = text.replace(heading, heading + "\n" + label, 1)
    path.write_text(text, encoding="utf-8")

validator = ROOT / "tools/validate_templates.py"
text = validator.read_text(encoding="utf-8")
text = text.replace(
    '    "vertiv.battery.test.interval",\n    "ups.battery.runtime.hours",\n}',
    '    "vertiv.battery.test.interval",\n}',
    1,
)
text = text.replace(
    'item_key in {"ups.alarms.present", "ups.battery.runtime"}',
    'item_key == "ups.alarms.present"',
)
validator.write_text(text, encoding="utf-8")
