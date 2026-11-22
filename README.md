# GazeBench
### Synthetic Eye Movement & Virtual Camera Rendering
**Samsung XR Hackathon 2026 — Track 01**

GazeBench is a Blender-based 3D eye movement system controlled through Python. It demonstrates controlled gaze direction, calibrated eye movement, a fixed virtual camera, and a sequence of ten clockwise gaze positions.

The project provides a Blender scene, a Python eye-control wrapper, rendered image outputs, and per-frame metadata.

---

## 1. Project Overview

The objective of GazeBench is to simulate controlled 3D eye movements and generate consistent rendered outputs with corresponding ground-truth data.

The system supports:
- Horizontal and vertical eye movement.
- A defined gaze movement range.
- Returning both eyes to a neutral position.
- Ten clockwise gaze samples starting from the upward direction.
- Per-frame metadata containing gaze inputs, eye rotations, pupil coordinates, and camera information.

## 2. Repository Structure

```text
GazeBench/
│
├── scene.blend
│
├── scene_HEAD_RIGGED.blend
│
├── wrapper/
│   └── eyes.py
│
├── renders/
│   ├── frame_00.png
│   ├── frame_01.png
│   ├── ...
│   └── frame_09.png
│
├── textures/
│
├── validation/
│
├── videos/
│
├── metadata.json
├── contact_sheet.png
├── VALIDATION_REPORT.md
└── README.md
```

**Primary scene:** `scene.blend`  
**Additional scene:** `scene_HEAD_RIGGED.blend`

The original scene is retained as the primary eye-control scene. The head-rigged version is provided separately for inspection.

## 3. Technologies Used

- Blender — 3D scene creation and rendering
- Python — eye movement control and automation
- NumPy — numerical operations
- JSON — ground-truth metadata
- PNG — rendered image outputs
- GitHub — source code and project documentation

## 4. Scene Calibration

The project uses the following calibration targets:

| Parameter | Target |
|---|---:|
| Fixation target distance | 0.35 m |
| Horizontal movement bounds | ±0.05 m |
| Vertical movement bounds | ±0.05 m |
| Camera distance | 0.40 m |
| Render resolution | 1024 × 1024 pixels |
| Number of gaze samples | 10 |

The camera is configured as a fixed virtual camera facing the face.

## 5. Setup and Initialization

### Requirements

- Blender 4.5.x is the version used to save the submitted scene.
- Python is provided through Blender's Python environment.

For best compatibility, use Blender 4.5.x.

### Steps

1. Clone or download this repository.
2. Open `scene.blend` in Blender.
3. Switch to the Python Console.
4. Add the repository's local path to Python's module search path.

Replace the example path below with the actual location of your downloaded GazeBench folder.

```python
import sys
sys.path.append(r"C:\PATH\TO\GazeBench")

import wrapper.eyes as eyes
```

If the import succeeds, the eye-control functions can be called through the imported module.

## 6. Python Eye Control API

The wrapper exposes module-level control functions.

### Move the eyes

```python
eyes.move(-1, 0)  # Left
eyes.move(1, 0)   # Right
eyes.move(0, 1)   # Up
eyes.move(0, -1)  # Down
```

The horizontal and vertical inputs are clamped to the supported movement range.

### Reset the eyes

```python
eyes.reset()
```

This returns the eye controls to their neutral position.

**Note:** The submitted wrapper exposes `move()` and `reset()`. A separate `eyes.render()` API is not currently documented as implemented.

## 7. Ten-Frame Clockwise Gaze Sequence

The project contains ten rendered gaze samples following a clockwise circular sequence.

The sampling angle is:

\[
\theta_k = \frac{2\pi k}{10}, \quad k=0,\ldots,9
\]

The horizontal and vertical inputs are:

\[
h = \sin(\theta_k)
\]

\[
v = \cos(\theta_k)
\]

The sequence begins at the upward position and proceeds clockwise.

The ten rendered frames are available in the `renders/` directory.

## 8. Ground-Truth Metadata

The `metadata.json` file stores per-frame information associated with the gaze sequence.

The metadata includes:
- Gaze input values.
- Left and right eye rotations.
- Left and right pupil centre coordinates.
- Camera information and matrix data.

### Metadata limitation

The pupil centre coordinates are projected from pupil-object origins. They are not independently measured physical eye-tracking coordinates.

Validation has shown close agreement between the projected pupil positions and image-based pupil segmentation on the supplied renders. This should be understood as a rendering and geometric consistency check, not a claim of physical eye-tracking accuracy.

## 9. Validation and Results

The project includes validation materials and a contact sheet.

The tested eye-control behaviour includes:
- Left movement.
- Right movement.
- Upward movement.
- Downward movement.
- Reset to neutral.

The supplied ten-frame sequence and metadata have also been checked for consistency.

The structural validation report checks the presence and basic structure of project files. It should not be interpreted as independent proof of every numerical or visual requirement.

## 10. Project Outputs

| Output | Location |
|---|---|
| Blender scene | `scene.blend` |
| Additional head-rigged scene | `scene_HEAD_RIGGED.blend` |
| Python controller | `wrapper/eyes.py` |
| Ten rendered frames | `renders/` |
| Ground-truth data | `metadata.json` |
| Contact sheet | `contact_sheet.png` |
| Validation report | `VALIDATION_REPORT.md` |

## 11. Project Links

- **GitHub Repository:** https://github.com/as4918/GazeBench
- **Presentation:** [Open Presentation](https://docs.google.com/presentation/d/11rujTvg5XPhXqhUAprfr-sGjaQVuPf5U/edit?usp=drive_link)
- **AI Disclosure:** [Open AI Disclosure](https://docs.google.com/document/d/1lAgwAaDVfV28Aj4a58znJcG-uyfo6nJp/edit?usp=drive_link&ouid=117653696680622693660&rtpof=true&sd=true)
- **Demo Video:** [Open Video Folder](https://drive.google.com/drive/folders/1anGJ_G9Rz1hrrXb0DwQ1y9j0L_WNCjjj?usp=sharing)

The demo video link should be updated to the direct recording once the final video is uploaded.

## 12. Team

**Institution:** SRM Institute of Science and Technology  
**Project:** GazeBench  
**Hackathon:** Samsung XR Hackathon 2026  
**Track:** Track 01 — Synthetic Eye Movement & Virtual Camera Rendering

---

*GazeBench — Controlled 3D eye movement and virtual camera rendering.*
