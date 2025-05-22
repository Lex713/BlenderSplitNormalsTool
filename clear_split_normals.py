bl_info = {
    "name": "Custom Normals Tools",
    "author": "Lex713",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Misc Tab",
    "description": "Select all mesh objects and clear custom split normals",
    "category": "3D View",
}

import bpy

# Operator: Select All Meshes
class OBJECT_OT_select_all_meshes(bpy.types.Operator):
    bl_idname = "object.select_all_meshes_custom"
    bl_label = "Select All Mesh Objects"
    bl_description = "Select all mesh objects in the scene"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        for obj in context.scene.objects:
            if obj.type == 'MESH':
                obj.select_set(True)
        return {'FINISHED'}

# Operator: Clear Custom Split Normals
class OBJECT_OT_clear_custom_normals(bpy.types.Operator):
    bl_idname = "object.clear_custom_split_normals"
    bl_label = "Clear Custom Split Normals"
    bl_description = "Clear custom split normals from selected mesh objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        original_mode = bpy.context.mode

        for obj in context.selected_objects:
            if obj.type == 'MESH':
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                try:
                    bpy.ops.mesh.customdata_custom_splitnormals_clear()
                    self.report({'INFO'}, f"Cleared: {obj.name}")
                except Exception as e:
                    self.report({'WARNING'}, f"{obj.name}: Failed - {str(e)}")
                bpy.ops.object.mode_set(mode='OBJECT')

        # Return to original mode
        if original_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode=original_mode)

        return {'FINISHED'}

# Panel: Right Sidebar
class VIEW3D_PT_custom_normals_panel(bpy.types.Panel):
    bl_label = "Custom Normals Tools"
    bl_idname = "VIEW3D_PT_custom_normals_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Misc'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.select_all_meshes_custom", icon='RESTRICT_SELECT_OFF')
        layout.operator("object.clear_custom_split_normals", icon='X')

# Register
classes = (
    OBJECT_OT_select_all_meshes,
    OBJECT_OT_clear_custom_normals,
    VIEW3D_PT_custom_normals_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
