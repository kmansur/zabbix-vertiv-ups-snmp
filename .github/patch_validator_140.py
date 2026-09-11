from pathlib import Path

path = Path("tools/validate_templates.py")
text = path.read_text(encoding="utf-8")
old = '''                        if item_key in {"ups.alarms.present", "ups.battery.runtime"}:
                            if str(fields_by_name.get("decimal_places", {}).get("value", "")) != "0":
                                errors.append(
                                    f"dashboard numeric card decimal_places must be 0: {widget.get('name')!r}"
                                )
'''
new = '''                        if (
                            item_key in {"ups.alarms.present", "ups.battery.runtime"}
                            and str(fields_by_name.get("decimal_places", {}).get("value", "")) != "0"
                        ):
                            errors.append(
                                f"dashboard numeric card decimal_places must be 0: {widget.get('name')!r}"
                            )
'''
if old not in text:
    raise SystemExit("validator style anchor not found")
path.write_text(text.replace(old, new, 1), encoding="utf-8")
