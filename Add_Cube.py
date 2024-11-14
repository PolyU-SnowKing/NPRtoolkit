bl_info = {
    "name": "NPRtoolkit",
    "author": "24062576g",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > NPRtoolkit",
    "description": "Adds a new Mesh Object and logs 'test'",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}

import bpy
from bpy.types import Operator, Panel
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
import os

####设置初始化参数####
current_dir = os.path.dirname(__file__)
PRESET_FILE_PATH = os.path.join(current_dir, "file/props.blend")


###FUNCTION1######

def add_object(self, context):
    scale_x = self.scale.x
    scale_y = self.scale.y

    verts = [
        Vector((-1 * scale_x, 1 * scale_y, 0)),
        Vector((1 * scale_x, 1 * scale_y, 0)),
        Vector((1 * scale_x, -1 * scale_y, 0)),
        Vector((-1 * scale_x, -1 * scale_y, 0)),
    ]

    edges = []
    faces = [[0, 1, 2, 3]]

    mesh = bpy.data.meshes.new(name="New Object Mesh")
    mesh.from_pydata(verts, edges, faces)
    object_data_add(context, mesh, operator=self)


######FUNCTION2#######


def add_Outline():
    for obj in bpy.context.selected_objects:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        solidify_modifier = obj.modifiers[-1]
        solidify_modifier.name = "Outline"
        solidify_modifier.thickness = 0.1
        solidify_modifier.offset = 1
        solidify_modifier.use_flip_normals = True
        solidify_modifier.use_rim = True

def add_Outline():
    for obj in bpy.context.selected_objects:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        solidify_modifier = obj.modifiers[-1]
        solidify_modifier.name = "Outline"
        solidify_modifier.thickness = 0.1
        solidify_modifier.offset = 1
        solidify_modifier.use_flip_normals = True
        solidify_modifier.use_rim = True


class OBJECT_OT_add_object(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_object"
    bl_label = "Add Mesh Object"
    bl_options = {'REGISTER', 'UNDO'}

    scale: FloatVectorProperty(
        name="scale",
        default=(1.0, 1.0, 1.0),
        subtype='TRANSLATION',
        description="scaling",
    )

    # Write Function Here

    def execute(self, context):
        add_object(self, context)
        return {'FINISHED'}


class OBJECT_OT_log_test(Operator):
    """Log 'test' to the console"""
    bl_idname = "object.log_test"
    bl_label = "Add OutLine"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.report({'INFO'}, "test")
        print("Add_OutLine")
        add_Outline()
        return {'FINISHED'}


class VIEW3D_PT_NPRtoolkit(Panel):
    bl_label = "NPRtoolkit"
    bl_idname = "VIEW3D_PT_NPRtoolkit"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'NPRtoolkit'

    def draw(self, context):
        layout = self.layout
        layout.operator("mesh.add_object")
        layout.operator("object.log_test")


def register():
    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.utils.register_class(OBJECT_OT_log_test)
    bpy.utils.register_class(VIEW3D_PT_NPRtoolkit)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.utils.unregister_class(OBJECT_OT_log_test)
    bpy.utils.unregister_class(VIEW3D_PT_NPRtoolkit)


if __name__ == "__main__":
    register()