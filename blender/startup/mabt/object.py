import bpy


class CombineSeparate(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "object.combine_separate"
    bl_label = "Combine Separete"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None or len(context.selected_objects) == 0

    def execute(self, context):
        # We are operating on active and the selected objects.
        active = bpy.context.active_object
        objs = bpy.context.selected_objects
        if active not in objs:
            print("ERROR: Active object not in selected ({})".format(active))
            return

        if len(objs) > 1:
            bpy.ops.object.join()
        else:
            bpy.ops.mesh.separate(type="LOOSE")

        return {"FINISHED"}


_classes = [CombineSeparate]
