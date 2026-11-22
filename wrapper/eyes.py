
import bpy
import math
from mathutils import Vector

TARGET_DISTANCE = 0.350
TARGET_HALF_RANGE = 0.050
CAMERA_DISTANCE = 0.400


class EyeController:

    def __init__(self):
        required = [
            "GazeBench_Eye_Armature",
            "Eye_L_Pivot",
            "Eye_R_Pivot",
            "Fixation_Target",
            "GazeBench_Camera",
        ]

        missing = [
            name for name in required
            if bpy.data.objects.get(name) is None
        ]

        if missing:
            raise RuntimeError(
                "Missing rig objects: " + ", ".join(missing)
            )

        self.armature = bpy.data.objects["GazeBench_Eye_Armature"]

        self.left = bpy.data.objects["Eye_L_Pivot"]
        self.right = bpy.data.objects["Eye_R_Pivot"]

        self.target = bpy.data.objects["Fixation_Target"]
        self.camera = bpy.data.objects["GazeBench_Camera"]

        self.left_bone = self.armature.pose.bones["Eye_L_Bone"]
        self.right_bone = self.armature.pose.bones["Eye_R_Bone"]

        self.left_bone.rotation_mode = "XYZ"
        self.right_bone.rotation_mode = "XYZ"

        self.midpoint = (
            self.left.matrix_world.translation
            + self.right.matrix_world.translation
        ) / 2.0

        if self.target.parent is not None:
            raise RuntimeError(
                "Fixation_Target must not have a parent."
            )

        self.reset()

    def move(self, h, v):

        h = max(-1.0, min(1.0, float(h)))
        v = max(-1.0, min(1.0, float(v)))

        goal = self.midpoint + Vector((
            h * TARGET_HALF_RANGE,
            -TARGET_DISTANCE,
            v * TARGET_HALF_RANGE
        ))

        self.target.location = goal

        for pivot, bone in (
            (self.left, self.left_bone),
            (self.right, self.right_bone)
        ):

            eye_position = pivot.matrix_world.translation
            direction = goal - eye_position

            yaw = math.atan2(
                direction.x,
                -direction.y
            )

            pitch = -math.atan2(
                direction.z,
                math.sqrt(
                    direction.x ** 2
                    + direction.y ** 2
                )
            )

            bone.rotation_euler = (
                pitch,
                0.0,
                yaw
            )

        bpy.context.view_layer.update()

        return {
            "h": h,
            "v": v,
            "left_rotation": tuple(self.left_bone.rotation_euler),
            "right_rotation": tuple(self.right_bone.rotation_euler),
            "target": tuple(goal)
        }

    def reset(self):
        return self.move(0.0, 0.0)


def register():

    controller = EyeController()

    bpy.app.driver_namespace["eyes"] = controller

    return controller


eyes = register()


# Public module-level API required by the Track 01 interface.
# The controller instance remains available as `eyes` for backward compatibility.
def move(h, v):
    return eyes.move(h, v)


def reset():
    return eyes.reset()
