"""
"""
import math

import bpy
import mathutils

from mabt import utils

VIEW_MAPPING = {
    "USER": 0,
    "-y": 1,
    "y": 2,
    "-x": 3,
    "x": 4,
    "z": 5,
    "-z": 6,
    "CAMERA": 7,
}


def get_active_axis_from_view_vector(view_vector):
    axes = {
        "-y": (0, -1, 0),
        "y": (0, 1, 0),
        "-x": (-1, 0, 0),
        "x": (1, 0, 0),
        "z": (0, 0, 1),
        "-z": (0, 0, -1),
    }
    dots = {}
    for axis, world_vector in axes.items():
        dots[axis] = view_vector @ mathutils.Vector(world_vector)

    return max(dots, key=dots.get)


def snap_view(view):
    # We need to setup some saved positions XXX: implement as context manager
    world_translate = mathutils.Vector(utils.camera_position(view.view_matrix))
    origin_location = view.view_location.copy()
    origin_distance = view.view_distance

    # Blender is using z axis as up axis, # Get the direction from a quaternion
    # rotation and convert it to a vector
    up_axis = mathutils.Vector((0.0, 0.0, 1.0))
    view_vector = view.view_rotation @ up_axis

    # figure out what axis the camera is looking down
    axis = get_active_axis_from_view_vector(view_vector)
    blender_internal_axis = VIEW_MAPPING[axis]

    if len(axis) > 1:
        axis = axis[-1]

    if view.is_perspective:
        # We are working with axis values, meaning any values that doesn't
        # line up correctly with an axis needs to be fixed. We use 90
        # degrees as the fix value and anything that is not dividable by
        # ninto will have it's value replaced by the closet value divided
        # by 90.
        snapped_vector = mathutils.Vector(
            [
                math.radians(int(90 * round(math.degrees(i) / 90)))
                for i in view.view_rotation.to_euler()
            ]
        )

        # the blender space view "camera" behaves in a way that it rotates
        # round it's center of interest (location). The distance is along
        # the local z axis and is just a pushed value. For a smoother
        # transition we translate the view location to the actual camera
        # position and we half the distance. This ensures there won't be a
        # "jankiness" and user ending up too far from the original target
        # view.view_location = world_translate
        # view.view_distance = view.view_distance/2

        euler_rot = view.view_rotation.to_euler()
        for ax in "xyz":
            setattr(euler_rot, ax, getattr(snapped_vector, ax))

        # Replace the rotation with the edited quaternion
        view.view_rotation = euler_rot.to_quaternion()

        # Restore original location and distance value
        # view.view_location = origin_location
        # view.view_distance = origin_distance

        # set camera mode to ortho
        view.view_perspective = "ORTHO"
        view.view_distance = view.view_distance / 2

        # We want to have gridlines displayed in the ortho view, this is achieved by
        # setting the below bool
        view.view = blender_internal_axis

        # We want to avoid rotation breaking the ortho view, so we lock the view rotations.
        # XXX: lock_rotation will perform a "matching" to the camera setup by
        # blender through "view_axis"
        view.lock_rotation = True

    else:
        # The toggle to perspective is much simpler - we just have to toggle
        # off the ortho values and set the camera to perspective and we're
        # there.
        view.lock_rotation = False
        view.view_perspective = "PERSP"
        view.view = VIEW_MAPPING["USER"]
        view.view_distance = view.view_distance * 2

    return {"FINISHED"}


class ViewSnap(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "view3d.view_snap"
    bl_label = "View Snap"

    @classmethod
    def poll(cls, context):
        return context.space_data == bpy.types.SpaceView3D

    def execute(self, context):
        return snap_view(context.space_data.region_3d)


def main():
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            break

    snap_view(area.spaces[0].region_3d)


if __name__ == "__main__":
    main()
