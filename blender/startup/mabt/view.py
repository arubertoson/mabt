"""
"""
import bpy
import mathutils


def get_active_axis_from_view_vector(view_vector):
    axes = {
        "FRONT": (0, -1, 0),
        "BACK": (0, 1, 0),
        "LEFT": (-1, 0, 0),
        "RIGHT": (1, 0, 0),
        "TOP": (0, 0, 1),
        "BOTTOM": (0, 0, -1),
    }
    dots = {}
    for axis, world_vector in axes.items():
        dots[axis] = view_vector @ mathutils.Vector(world_vector)

    return max(dots, key=dots.get)


class ViewSnap(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "view3D.view_snap"
    bl_label = "View Snap"

    @classmethod
    def poll(cls, context):
        return context.space_data == bpy.types.SpaceView3D

    def execute(self, context):
        view = context.space_data.region_3d

        # Blender is using z axis as up axis
        up_axis = mathutils.Vector((0.0, 0.0, 1.0))

        if view.is_perspective:
            # Get the direction from a quaternion rotation and convert it to a vector
            view_vector = view.view_rotation @ up_axis
            axis = get_active_axis_from_view_vector(view_vector)

            bpy.ops.view3d.view_axis(context, type=axis)

            # We want to avoid rotation breaking the ortho view, so we lock the view rotations.
            view.lock_rotation = True
        else:
            view.lock_rotation = False
            view.view_perspective = "PERSP"

        return {"FINISHED"}


_classes = [ViewSnap]
