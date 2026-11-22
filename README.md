
PPT link: https://docs.google.com/presentation/d/11rujTvg5XPhXqhUAprfr-sGjaQVuPf5U/edit?usp=drive_link&ouid=117653696680622693660&rtpof=true&sd=true

AI disclosure: https://docs.google.com/document/d/1lAgwAaDVfV28Aj4a58znJcG-uyfo6nJp/edit?usp=sharing&ouid=117653696680622693660&rtpof=true&sd=true

Video link: https://drive.google.com/drive/folders/1anGJ_G9Rz1hrrXb0DwQ1y9j0L_WNCjjj?usp=sharing


# GazeBench - Samsung XR Hackathon Track 1

## Contents
scene.blend: calibrated Blender scene with two eye control bones
wrapper/eyes.py: Python controller
renders/: ten 1024x1024 PNG frames
metadata.json: per-frame gaze and camera data

## Initialization
Open scene.blend in Blender. In the Python Console run:
import sys; sys.path.append(r'<submission-folder-path>'); import wrapper.eyes as eyes

## API
eyes.eyes.move(h,v)
eyes.eyes.reset()

## Calibration
Fixation distance: 0.35 m
Horizontal and vertical target half-range: 0.05 m
Camera distance: 0.40 m
Resolution: 1024x1024

## Sequence
Ten clockwise frames starting at the top.
theta = 2*pi*k/10; h = sin(theta); v = cos(theta).

## Metadata limitation
Pupil centres are projected pupil-object origins, not independently segmented image measurements.
Validation establishes internal geometric consistency, not independent physical eye-tracking accuracy.
