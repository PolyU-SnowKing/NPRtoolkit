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
#PRESET_FILE_PATH = os.path.join(current_dir, "file/prop.blend")
#PRESET_FILE_PATH = os.path.join(current_dir, "D:\Blender_NPRtoolkit\NPRtoolkit\prop.blend")
PRESET_FILE_PATH = "D:\Blender_NPRtoolkit/NPRtoolkit/prop.blend"

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


def add_Outline(obj, node_group_name):
    for obj in bpy.context.selected_objects:
        # Create Geometry Nodes Modifier
        modifier = obj.modifiers.new(name="GeometryNodes", type='NODES')

        # Load the node group from the preset file
        with bpy.data.libraries.load(PRESET_FILE_PATH, link=False) as (data_from, data_to):
            data_to.node_groups = [node_group_name]

        # Link the node group to the modifier
        modifier.node_group = bpy.data.node_groups[node_group_name]

        # Add a vertex group named "Normal_edge" and set all vertex weights to 1
        if "Normal_edge" not in obj.vertex_groups:
            vertex_group = obj.vertex_groups.new(name="Normal_edge")
            for i in range(len(obj.data.vertices)):
                vertex_group.add([i], 1.0, 'REPLACE')
        else:
            print("Vertex group 'Normal_edge' already exists.")


#######FUNCTION3######

def add_shader():
    for obj in bpy.context.selected_objects:
        bpy.context.view_layer.objects.active = obj




def add_composition():
    for obj in bpy.context.selected_objects:
        bpy.context.view_layer.objects.active = obj



def add_edge_modifier(obj, node_group_name):
    # 创建 Geometry Nodes Modifier
    modifier = obj.modifiers.new(name="GeometryNodes", type='NODES')

    # 加载预设文件中的节点组
    with bpy.data.libraries.load(PRESET_FILE_PATH, link=False) as (data_from, data_to):
        data_to.node_groups = [node_group_name]

    # 链接节点组到 Modifier
    modifier.node_group = bpy.data.node_groups[node_group_name]

    # 添加名为 "inkedge" 的顶点组并设置所有顶点权重为 1
    if "inkedge" not in obj.vertex_groups:
        vertex_group = obj.vertex_groups.new(name="inkedge")
        for i in range(len(obj.data.vertices)):
            vertex_group.add([i], 1.0, 'REPLACE')
    else:
        print("Vertex group 'inkedge' already exists.")

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




class OBJECT_OT_OUTLINE(Operator):
    """Log 'test' to the console"""
    bl_idname = "object.outline"
    bl_label = "Add OutLine"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.report({'INFO'}, "test")
        print("Add_OutLine")
        for obj in bpy.context.selected_objects:
            add_Outline(obj, "Normal_edge")  # Replace "NodeGroupName" with the actual node group name
        return {'FINISHED'}


class OBJECT_OT_add_solidify(bpy.types.Operator):
    bl_idname = "object.add_solidify_modifier"
    bl_label = "InkEdge"
    bl_description = "Add inkedge to Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not context.selected_objects:
            self.report({'WARNING'}, "No objects selected")
            return {'CANCELLED'}

        for obj in context.selected_objects:
            add_edge_modifier(obj, "inkedge")

        self.report({'INFO'}, "Solidify modifiers added")
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
    if not context.scene.use_nodes:
        context.scene.use_nodes = True

    # 加载 'paper_fx' 节点组
    with bpy.data.libraries.load(PRESET_FILE_PATH, link=False) as (data_from, data_to):

        if "paper_fx" in data_from.node_groups:
            data_to.node_groups = ["paper_fx"]
        else:
            self.report({'WARNING'}, "Paper FX node group not found")
            return {'CANCELLED'}

    # 获取合成节点树并添加 'paper_fx' 节点
    tree = context.scene.node_tree
    paper_fx_node = tree.nodes.new('CompositorNodeGroup')
    paper_fx_node.node_tree = bpy.data.node_groups['paper_fx']

    # ... 连接节点的逻辑 ...
    # 通过节点类型查找 Render Layers 节点和 Composite 节点
    render_layers_node = next((node for node in tree.nodes if node.type == 'R_LAYERS'), None)
    composite_node = next((node for node in tree.nodes if node.type == 'COMPOSITE'), None)

    # 如果找不到这些节点，报告错误
    if not render_layers_node or not composite_node:
        self.report({'ERROR'}, "Required nodes not found")
        return {'CANCELLED'}
    # 连接 Render Layers 到 paper_fx，然后连接到 Composite
    tree.links.new(render_layers_node.outputs[0], paper_fx_node.inputs[0])
    tree.links.new(paper_fx_node.outputs[0], composite_node.inputs[0])

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
        layout.operator("object.add_solidify_modifier")

def register():
    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.utils.register_class(OBJECT_OT_OUTLINE)
    bpy.utils.register_class(VIEW3D_PT_NPRtoolkit)
    bpy.utils.register_class(OBJECT_OT_SHADER)
    bpy.utils.register_class(OBJECT_OT_COMPOSITION)
    bpy.utils.register_class(OBJECT_OT_add_solidify)



def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.utils.unregister_class(OBJECT_OT_OUTLINE)
    bpy.utils.unregister_class(VIEW3D_PT_NPRtoolkit)
    bpy.utils.register_class(OBJECT_OT_SHADER)
    bpy.utils.register_class(OBJECT_OT_COMPOSITION)
    bpy.utils.register_class(OBJECT_OT_add_solidify)


if __name__ == "__main__":
    register()