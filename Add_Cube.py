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


#######FUNCTION3######

def add_shader():
    for obj in bpy.context.selected_objects:
        bpy.context.view_layer.objects.active = obj


######FUNCTION4######

def add_composition():
    for obj in bpy.context.selected_objects:
        bpy.context.view_layer.objects.active = obj


########UILAYER###########

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


import bpy
from bpy.types import Operator


class OBJECT_OT_OUTLINE(Operator):
    """Log 'test' to the console"""
    bl_idname = "object.outline"
    bl_label = "Add OutLine"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.report({'INFO'}, "test")
        print("Add_OutLine")
        add_Outline()
        return {'FINISHED'}


class OBJECT_OT_SHADER(Operator):
    '''add a custom shader to object'''
    bl_idname = "object.shader"
    bl_label = "Add NPRshader"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.report({'INFO'}, "test")
        print("Add NPRshader")
        add_shader()
        return {'FINISHED'}


class OBJECT_OT_COMPOSITION(Operator):
    '''add a COMPOSITION to object'''
    bl_idname = "object.composition"
    bl_label = "Add Composition"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.report({'INFO'}, "test")
        print("Add_OutLine")
        add_composition()
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
        layout.operator("object.outline")
        layout.operator("object.shader")
        layout.operator("object.composition")


def register():
    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.utils.register_class(OBJECT_OT_OUTLINE)
    bpy.utils.register_class(VIEW3D_PT_NPRtoolkit)
    bpy.utils.register_class(OBJECT_OT_SHADER)
    bpy.utils.register_class(OBJECT_OT_COMPOSITION)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.utils.unregister_class(OBJECT_OT_OUTLINE)
    bpy.utils.unregister_class(VIEW3D_PT_NPRtoolkit)
    bpy.utils.register_class(OBJECT_OT_SHADER)
    bpy.utils.register_class(OBJECT_OT_COMPOSITION)


if __name__ == "__main__":
    register()