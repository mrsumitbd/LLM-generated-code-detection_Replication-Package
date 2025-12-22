import bpy
import rr_avatar_tools

def run_roomie_diagnostics(old, new):
    # Do not run diagnostics in edit mode
    if bpy.context.active_object and bpy.context.active_object.mode == "EDIT":
        return

    collections = [
        c for c in rr_avatar_tools.data.collections if c.get("rec_room_roomie_uuid")
    ]
    for collection in collections:
        collection["has_errors"] = False

        for mesh in [
            m for m in collection.objects if m.type == "MESH" and "_LOD" in m.name
        ]:
            collection["has_errors"] |= any(
                [
                    op
                    for op in rr_avatar_tools.roomie.operators.diagnostics.classes
                    if op.diagnose(mesh)
                ]
            )