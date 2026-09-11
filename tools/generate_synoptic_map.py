"""Generate an importable Zabbix synoptic network map for one Vertiv UPS host."""

from __future__ import annotations

import argparse
import base64
import binascii
import struct
import zlib
from pathlib import Path
from typing import Any

import yaml

ICON_OK = "VERTIV UPS Synoptic - OK"
ICON_PROBLEM = "VERTIV UPS Synoptic - Problem"
SUPPORTED_VERSIONS = ("7.0", "8.0")


def _png_chunk(chunk_type: bytes, payload: bytes) -> bytes:
    crc = binascii.crc32(chunk_type + payload) & 0xFFFFFFFF
    return (
        struct.pack(">I", len(payload)) + chunk_type + payload + struct.pack(">I", crc)
    )


def make_ups_icon(problem: bool = False, width: int = 96, height: int = 64) -> bytes:
    """Create a tiny dependency-free RGBA PNG used by the generated map."""
    pixels = bytearray(width * height * 4)

    def set_pixel(x: int, y: int, rgba: tuple[int, int, int, int]) -> None:
        if 0 <= x < width and 0 <= y < height:
            offset = (y * width + x) * 4
            pixels[offset : offset + 4] = bytes(rgba)

    transparent = (255, 255, 255, 0)
    body = (222, 226, 230, 255)
    dark = (45, 49, 54, 255)
    panel = (82, 88, 94, 255)
    led = (205, 45, 45, 255) if problem else (44, 160, 85, 255)

    for y in range(height):
        for x in range(width):
            set_pixel(x, y, transparent)

    for y in range(5, height - 5):
        for x in range(13, width - 13):
            set_pixel(x, y, body)
    for x in range(13, width - 13):
        set_pixel(x, 5, dark)
        set_pixel(x, height - 6, dark)
    for y in range(5, height - 5):
        set_pixel(13, y, dark)
        set_pixel(width - 14, y, dark)

    for y in range(17, 38):
        for x in range(25, width - 25):
            set_pixel(x, y, panel)

    for y in range(23, 31):
        for x in range(width // 2 - 4, width // 2 + 4):
            set_pixel(x, y, led)

    for x in range(27, width - 27):
        set_pixel(x, 45, dark)
        set_pixel(x, 46, dark)

    rows = []
    row_size = width * 4
    for y in range(height):
        start = y * row_size
        rows.append(b"\x00" + bytes(pixels[start : start + row_size]))
    raw = b"".join(rows)
    header = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + _png_chunk(b"IHDR", header)
        + _png_chunk(b"IDAT", zlib.compress(raw, level=9))
        + _png_chunk(b"IEND", b"")
    )


def _shape(x: int, y: int, width: int, height: int, text: str) -> dict[str, str]:
    return {
        "type": "0",
        "x": str(x),
        "y": str(y),
        "width": str(width),
        "height": str(height),
        "text": text,
        "font": "9",
        "font_size": "13",
        "font_color": "202428",
        "text_halign": "0",
        "text_valign": "0",
        "border_type": "1",
        "border_width": "2",
        "border_color": "6C757D",
        "background_color": "F4F6F8",
        "zindex": "0",
    }


def _line(x1: int, y1: int, x2: int, y2: int) -> dict[str, str]:
    return {
        "x1": str(x1),
        "y1": str(y1),
        "x2": str(x2),
        "y2": str(y2),
        "line_type": "1",
        "line_width": "3",
        "line_color": "6C757D",
        "zindex": "1",
    }


def build_export(host: str, zabbix_version: str = "7.0") -> dict[str, Any]:
    host = host.strip()
    if not host:
        raise ValueError("host name must not be empty")
    if zabbix_version not in SUPPORTED_VERSIONS:
        raise ValueError(
            f"unsupported Zabbix version {zabbix_version!r}; expected one of {SUPPORTED_VERSIONS}"
        )

    ok_icon = base64.b64encode(make_ups_icon(problem=False)).decode("ascii")
    problem_icon = base64.b64encode(make_ups_icon(problem=True)).decode("ascii")

    map_data = {
        "name": f"VERTIV UPS Synoptic - {host}",
        "width": "1200",
        "height": "650",
        "label_type": "0",
        "label_location": "0",
        "highlight": "1",
        "expandproblem": "1",
        "markelements": "1",
        "show_unack": "0",
        "severity_min": "2",
        "show_suppressed": "0",
        "grid_size": "50",
        "grid_show": "1",
        "grid_align": "1",
        "label_format": "0",
        "label_type_host": "2",
        "label_type_hostgroup": "2",
        "label_type_trigger": "2",
        "label_type_map": "2",
        "label_type_image": "2",
        "label_string_host": "",
        "label_string_hostgroup": "",
        "label_string_trigger": "",
        "label_string_map": "",
        "label_string_image": "",
        "expand_macros": "1",
        "background": {},
        "iconmap": {},
        "urls": {},
        "selements": [
            {
                "elementtype": "0",
                "elements": [{"host": host}],
                "label": "{HOST.NAME}\n{HOST.CONN}",
                "label_location": "0",
                "x": "552",
                "y": "278",
                "elementsubtype": "0",
                "areatype": "0",
                "width": "200",
                "height": "200",
                "viewtype": "0",
                "use_iconmap": "0",
                "selementid": "1",
                "icon_off": {"name": ICON_OK},
                "icon_on": {"name": ICON_PROBLEM},
                "icon_disabled": {"name": ICON_OK},
                "icon_maintenance": {"name": ICON_OK},
                "urls": {},
                "evaltype": "0",
            }
        ],
        "shapes": [
            _shape(0, 0, 1200, 42, "{MAP.NAME}"),
            _shape(90, 170, 250, 120, "INPUT\nUtility / Rectifier"),
            _shape(90, 390, 250, 120, "BYPASS\nMaintenance / Static"),
            _shape(860, 170, 250, 120, "OUTPUT\nProtected Load"),
            _shape(860, 390, 250, 120, "BATTERY\nDC Energy Storage"),
            _shape(
                410,
                500,
                380,
                90,
                "Host problems dynamically highlight the UPS icon.\nPeripheral blocks are an operational schematic.",
            ),
        ],
        "lines": [
            _line(340, 230, 552, 300),
            _line(340, 450, 552, 335),
            _line(648, 300, 860, 230),
            _line(648, 335, 860, 450),
        ],
        "links": {},
    }

    return {
        "zabbix_export": {
            "version": zabbix_version,
            "images": [
                {"name": ICON_OK, "imagetype": "1", "encodedImage": ok_icon},
                {
                    "name": ICON_PROBLEM,
                    "imagetype": "1",
                    "encodedImage": problem_icon,
                },
            ],
            "maps": [map_data],
        }
    }


def render_yaml(host: str, zabbix_version: str = "7.0") -> str:
    return yaml.safe_dump(
        build_export(host, zabbix_version),
        sort_keys=False,
        allow_unicode=True,
        width=1000,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate an importable Zabbix VERTIV UPS synoptic map."
    )
    parser.add_argument(
        "--host",
        required=True,
        help="Exact Zabbix host name already linked to VERTIV by SNMP.",
    )
    parser.add_argument(
        "--zabbix-version",
        choices=SUPPORTED_VERSIONS,
        default="7.0",
        help="Map export version (default: 7.0).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("vertiv-ups-synoptic.yaml"),
        help="Output YAML path.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output.write_text(
        render_yaml(args.host, args.zabbix_version), encoding="utf-8"
    )
    print(f"Wrote {args.output} for host {args.host!r} (Zabbix {args.zabbix_version})")


if __name__ == "__main__":
    main()
