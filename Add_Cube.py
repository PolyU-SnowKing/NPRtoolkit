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

    def execute(self, context):
        add_object(self, context)
        return {'FINISHED'}

class OBJECT_OT_log_test(Operator):
    """Log 'test' to the console"""
    bl_idname = "object.log_test"
    bl_label = "Log Test"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.report({'INFO'}, "test")
        print("test")
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