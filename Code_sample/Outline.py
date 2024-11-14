import bpy

# Ensure we are in object mode
if bpy.context.mode != 'OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')

for obj in bpy.context.selected_objects:
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.faces_shade_smooth()
    bpy.ops.object.mode_set(mode='OBJECT')

    # Ensure we are in the correct context
    if bpy.context.area.type == 'VIEW_3D':
        bpy.context.area.ui_type = 'VIEW_3D'
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        bpy.context.object.modifiers["Solidify"].use_flip_normals = True
        bpy.context.object.modifiers["Solidify"].thickness = 0.01
        bpy.context.area.ui_type = 'MATERIAL'
        bpy.ops.object.material_slot_add()