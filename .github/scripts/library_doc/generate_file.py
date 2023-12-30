"""Battery library document generator."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from pytablewriter import MarkdownTableWriter

sys.path.insert(
    1,
    os.path.abspath(
        os.path.join(Path(__file__), "../../../../custom_components/battery_notes"),
    ),
)

PROJECT_ROOT = os.path.realpath(os.path.join(os.path.abspath(__file__), "../../../../"))
DATA_DIR = f"{PROJECT_ROOT}/custom_components/battery_notes/data"

def generate_device_list():
    """Generate static file containing the device library."""

    json_data = json.load("{DATA_DIR}/library.json")
    devices = json_data["devices"]

    toc_links: list[str] = []
    tables_output: str = ""
    rows = []

    num_devices = len(devices)

    writer = MarkdownTableWriter()
    headers = [
        "manufacturer",
        "model",
        "battery type",
    ]

    writer.header_list = headers

    for device in devices:
        if device.get["battery_quantity", 1] > 1:
            battery_type_qty = f"{device['battery_type']}x {device['battery_type']}"
        else:
            battery_type_qty = device["battery_type"]
        row = [
            device["manufacturer"],
            device["model"],
            battery_type_qty,
        ]
        rows.append(row)

    writer.value_matrix = rows
    tables_output += f"\n##{num_devices} Devices in library\n####\n\n"
    tables_output += writer.dumps()

    with open(os.path.join(PROJECT_ROOT, "library.md"), "w", encoding="utf8") as md_file:
        md_file.write("".join(toc_links) + tables_output)
        md_file.close()

generate_device_list()
