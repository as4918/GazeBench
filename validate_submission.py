#!/usr/bin/env python3
"""
GazeBench Track 01 - Submission Validator
Run from the GazeBench repository root:
    py validate_submission.py

This script is read-only: it does not modify the Blender scene, renders,
metadata, or wrapper. It writes VALIDATION_REPORT.txt.
"""
from pathlib import Path
import json
import re
import struct
import sys

ROOT = Path(__file__).resolve().parent
EXPECTED_FRAMES = [f"frame_{i:02d}.png" for i in range(10)]

checks = []

def record(name, passed, detail=""):
    checks.append((name, bool(passed), detail))

def png_dimensions(path):
    with path.open("rb") as f:
        header = f.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    if header[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", header[16:24])

# Core submission files
scene_new = ROOT / "scene_HEAD_RIGGED.blend"
scene_original = ROOT / "scene.blend"
wrapper = ROOT / "wrapper" / "eyes.py"
renders_dir = ROOT / "renders"
metadata_path = ROOT / "metadata.json"
readme_path = ROOT / "README.md"
contact_sheet = ROOT / "contact_sheet.png"

record("New head-rigged Blender scene exists", scene_new.is_file(),
       str(scene_new.name))
record("Original Blender scene retained", scene_original.is_file(),
       str(scene_original.name))
record("Eye controller wrapper exists", wrapper.is_file(),
       "wrapper/eyes.py")
record("Renders folder exists", renders_dir.is_dir(),
       "renders/")
record("Metadata JSON exists", metadata_path.is_file(),
       "metadata.json")
record("README exists", readme_path.is_file(),
       "README.md")
record("Contact sheet exists", contact_sheet.is_file(),
       "contact_sheet.png")

# Check eye API text without importing bpy outside Blender.
if wrapper.is_file():
    source = wrapper.read_text(encoding="utf-8", errors="replace")
    module_move = re.search(r"(?m)^def\s+move\s*\(", source) is not None
    module_reset = re.search(r"(?m)^def\s+reset\s*\(", source) is not None
    record("Module-level eyes.move(h, v) exists", module_move)
    record("Module-level eyes.reset() exists", module_reset)
else:
    record("Module-level eyes.move(h, v) exists", False, "wrapper missing")
    record("Module-level eyes.reset() exists", False, "wrapper missing")

# Check ten expected render files and their dimensions.
found_frames = []
for filename in EXPECTED_FRAMES:
    path = renders_dir / filename
    if path.is_file():
        found_frames.append(path)
record("All 10 expected frame PNGs exist", len(found_frames) == 10,
       f"{len(found_frames)}/10 found")

dimension_results = []
for path in found_frames:
    dims = png_dimensions(path)
    dimension_results.append((path.name, dims))
bad_dims = [(name, dims) for name, dims in dimension_results
            if dims != (1024, 1024)]
record("All found frames are valid 1024x1024 PNGs",
       len(found_frames) == 10 and not bad_dims,
       "All 10 are 1024x1024" if len(found_frames) == 10 and not bad_dims
       else f"Unexpected dimensions: {bad_dims}")

# Parse metadata and report its structure without assuming undocumented key names.
metadata = None
if metadata_path.is_file():
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        record("Metadata JSON parses successfully", True,
               f"Top-level type: {type(metadata).__name__}")
    except Exception as exc:
        record("Metadata JSON parses successfully", False, str(exc))
else:
    record("Metadata JSON parses successfully", False, "File missing")

def collect_dicts(value, out):
    if isinstance(value, dict):
        out.append(value)
        for v in value.values():
            collect_dicts(v, out)
    elif isinstance(value, list):
        for v in value:
            collect_dicts(v, out)

if metadata is not None:
    dicts = []
    collect_dicts(metadata, dicts)
    # Look for frame-like records using frame/image identifiers or gaze inputs.
    frame_records = []
    for d in dicts:
        keys = {str(k).lower() for k in d.keys()}
        if (any("frame" in k for k in keys)
            or any(k in keys for k in ("h", "v", "input_h", "input_v"))
            or any("pupil" in k for k in keys)):
            frame_records.append(d)
    record("Metadata contains frame/gaze-related records",
           len(frame_records) >= 10,
           f"{len(frame_records)} candidate records detected; inspect schema if fewer")
    # Check presence of common categories, allowing different naming conventions.
    all_keys = set()
    for d in dicts:
        all_keys.update(str(k).lower() for k in d.keys())
    categories = {
        "input coordinates": any(k in all_keys for k in ("h", "v", "input_h", "input_v", "inputs")),
        "eye rotation data": any("rotation" in k for k in all_keys),
        "pupil centre data": any("pupil" in k for k in all_keys),
        "camera matrix data": any("camera" in k or "matrix" in k for k in all_keys),
    }
    for label, present in categories.items():
        record(f"Metadata includes {label}", present,
               "Key-name presence check only; values not independently validated")

# Build report
passed = sum(1 for _, ok, _ in checks if ok)
failed = len(checks) - passed
lines = [
    "GazeBench Track 01 - Submission Validation Report",
    "=" * 54,
    f"Project folder: {ROOT}",
    f"Checks passed: {passed}/{len(checks)}",
    "",
]
for name, ok, detail in checks:
    status = "PASS" if ok else "CHECK"
    lines.append(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
lines += [
    "",
    "Notes:",
    "- This is a local file/package sanity check, not an official hackathon score.",
    "- It does not open or re-render the .blend scene.",
    "- Metadata key checks detect likely fields; they do not validate numerical correctness.",
    "- Blender head-rig behavior and five-direction gaze behavior still require visual/runtime testing.",
]
report_path = ROOT / "VALIDATION_REPORT.txt"
report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
print(f"\nSaved report: {report_path}")
sys.exit(0 if failed == 0 else 1)
