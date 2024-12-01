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
import random

####设置初始化参数####
current_dir = os.path.dirname(__file__)
#current_dir = os.getcwd()
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


def insert_color_attribute(obj, color_layer_name, color_value):
    # 确保物体是一个网格对象
    if obj.type != 'MESH':
        print("Selected object is not a mesh")
        return

    mesh = obj.data

    # 检查是否已存在名为 color_layer_name 的颜色层，如果不存在则创建
    if color_layer_name not in mesh.vertex_colors:
        color_layer = mesh.vertex_colors.new(name=color_layer_name)
    else:
        color_layer = mesh.vertex_colors[color_layer_name]

    # 为颜色层中的每个顶点循环（Loop）设置颜色值
    for loop_index, loop in enumerate(mesh.loops):
        color_layer.data[loop_index].color = color_value


def insert_shader_node_to_material(obj):
    # 确保物体有材质槽
    insert_color_attribute(obj, "mask0", (1.0, 1.0, 1.0, 1.0))

    if not obj.material_slots:
        obj.data.materials.append(None)

    material = obj.material_slots[0].material
    if not material or not material.use_nodes:
        material = bpy.data.materials.new(name="New_Material")
        obj.material_slots[0].material = material

    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links

    # 查找 Principled BSDF 和 Image Texture 节点
    principled = next((node for node in nodes if node.type == 'BSDF_PRINCIPLED'), None)
    image_tex = next((node for node in nodes if node.type == 'TEX_IMAGE'), None)
    material_output = next((node for node in nodes if node.type == 'OUTPUT_MATERIAL'), None)

    # 加载节点
    with bpy.data.libraries.load(PRESET_FILE_PATH, link=False) as (data_from, data_to):
        if "ShaderNode" in data_from.node_groups:
            data_to.node_groups = ["ShaderNode"]
        else:
            print("ShaderNode group not found in the file.")
            return None

    # 将 ShadeNode 节点插入到节点树中
    inktex_node = nodes.new('ShaderNodeGroup')  # 创建一个新的节点组实例
    inktex_node.node_tree = bpy.data.node_groups.get("inktex", None)

    # 创建连接
    if principled and image_tex:
        links.new(image_tex.outputs[0], inktex_node.inputs[0])
        links.new(inktex_node.outputs[0], material_output.inputs['Surface'])
    else:
        links.new(inktex_node.outputs[0], material_output.inputs['Surface'])

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

class OBJECT_OT_add_shader(bpy.types.Operator):
    bl_idname = "object.add_shader_node"
    bl_label = "ShaderNode"
    bl_description = "Add ShaderNode to Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if obj and obj.type == 'MESH':
            insert_shader_node_to_material(obj)
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "No suitable object selected.")
            return {'CANCELLED'}
class OBJECT_OT_load_bg_fx(bpy.types.Operator):
    bl_idname = "object.load_bg_fx"
    bl_label = "Pure Background"

    def execute(self, context):
        # 确保世界使用节点
        world = context.scene.world
        if not world.use_nodes:
            world.use_nodes = True

        # 加载 'bg' 节点组
        with bpy.data.libraries.load(PRESET_FILE_PATH, link=False) as (data_from, data_to):
            if "bg" in data_from.node_groups:
                data_to.node_groups = ["bg"]
            else:
                self.report({'WARNING'}, "BG FX node group not found")
                return {'CANCELLED'}

        # 获取世界材质的节点树并添加 'bg' 节点组
        tree = world.node_tree
        bg_node = tree.nodes.new('ShaderNodeGroup')
        bg_node.node_tree = bpy.data.node_groups['bg']

        # 查找 World Output 节点
        world_output_node = next((node for node in tree.nodes if node.type == 'OUTPUT_WORLD'), None)
        if not world_output_node:
            self.report({'ERROR'}, "World Output node not found")
            return {'CANCELLED'}

        # 连接 'bg' 节点到 World Output
        # 假设 'bg' 节点组有一个名为 'Background' 的输出，且 World Output 节点有一个名为 'Surface' 的输入
        if 'Shader' in bg_node.outputs and 'Surface' in world_output_node.inputs:
            tree.links.new(bg_node.outputs['Shader'], world_output_node.inputs['Surface'])
        else:
            self.report({'ERROR'}, "Correct inputs/outputs not found for linking")
            return {'CANCELLED'}

        space_data = bpy.context.space_data
        if space_data and hasattr(space_data, 'shading'):
            # 根据当前值切换 use_compositor 设置
            space_data.shading.use_compositor = 'ALWAYS'

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

class MESH_OT_generate_random_rock(bpy.types.Operator):
    """Generate a random rock"""
    bl_idname = "mesh.generate_random_rock"
    bl_label = "Generate Random Rock"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        rock_size = context.scene.rock_size
        random_amount = context.scene.random_amount
        subdivisions = context.scene.subdivisions

        bpy.ops.mesh.primitive_uv_sphere_add(radius=rock_size, segments=12, ring_count=6)
        obj = context.object
        mesh = obj.data

        bm = bmesh.new()
        bm.from_mesh(mesh)
        for _ in range(subdivisions):
            bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=1, use_grid_fill=True)

        for vert in bm.verts:
            vert.co.x += random.uniform(-random_amount, random_amount)
            vert.co.y += random.uniform(-random_amount, random_amount)
            vert.co.z += random.uniform(-random_amount, random_amount)

        bm.to_mesh(mesh)
        bm.free()

        obj.name = "Random Rock"
        self.report({'INFO'}, "Generated a random rock")
        return {'FINISHED'}

class MESH_OT_advanced_randomize_vertices(bpy.types.Operator):
    """Randomly move vertices of the selected mesh objects"""
    bl_idname = "mesh.advanced_randomize_vertices"
    bl_label = "Advanced Vertex Randomizer"
    bl_options = {'REGISTER', 'UNDO'}

    amount: bpy.props.FloatProperty(
        name="Random Amount",
        description="Strength of the random displacement",
        default=0.1,
        min=0.0,
        max=10.0,
    )

    random_seed: bpy.props.IntProperty(
        name="Random Seed",
        description="Seed for the random generator (0 for random)",
        default=0,
        min=0,
    )

    def execute(self, context):
        random.seed(self.random_seed if self.random_seed != 0 else None)

        selected_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
        if not selected_objects:
            self.report({'WARNING'}, "No mesh objects selected")
            return {'CANCELLED'}

        for obj in selected_objects:
            mesh = obj.data
            bm = bmesh.new()
            bm.from_mesh(mesh)

            for vert in bm.verts:
                vert.co.x += random.uniform(-self.amount, self.amount)
                vert.co.y += random.uniform(-self.amount, self.amount)
                vert.co.z += random.uniform(-self.amount, self.amount)

            bm.to_mesh(mesh)
            bm.free()

        self.report({'INFO'}, f"Vertices randomized with strength {self.amount}")
        return {'FINISHED'}

class VIEW3D_PT_vertex_rock_tools(bpy.types.Panel):
    """Tools for Vertex Randomization and Rock Generation"""
    bl_label = "Vertex & Rock Tools"
    bl_idname = "VIEW3D_PT_vertex_rock_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Vertex Tools"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Randomize Vertices:")
        layout.operator("mesh.advanced_randomize_vertices")
        layout.separator()

        layout.label(text="Generate Random Rock:")
        col = layout.column(align=True)
        col.prop(context.scene, "rock_size")
        col.prop(context.scene, "random_amount")
        col.prop(context.scene, "subdivisions")
        layout.operator("mesh.generate_random_rock", text="Create Random Rock")



class VIEW3D_PT_NPRtoolkit(Panel):
    bl_label = "NPRtoolkit"
    bl_idname = "VIEW3D_PT_NPRtoolkit"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'NPRtoolkit'

    def draw(self, context):
        layout = self.layout
        layout.label(text="Test")
        layout.operator("mesh.add_object")
        layout.label(text="Render")
        layout.operator("object.add_solidify_modifier")
        layout.operator("object.outline")
        layout.operator("object.add_shader_node")
        layout.label(text="Compositing")
        layout.operator("object.composition")
        layout.operator("object.load_bg_fx")
        layout.label(text="rock")
        layout.operator("mesh.generate_random_rock")
        layout.operator("mesh.advanced_randomize_vertices")
        layout.operator("VIEW3D_PT_vertex_rock_tools")

def register():
    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.utils.register_class(OBJECT_OT_OUTLINE)
    bpy.utils.register_class(VIEW3D_PT_NPRtoolkit)
    bpy.utils.register_class(OBJECT_OT_SHADER)
    bpy.utils.register_class(OBJECT_OT_COMPOSITION)
    bpy.utils.register_class(OBJECT_OT_add_solidify)
    bpy.utils.register_class(OBJECT_OT_load_bg_fx)
    bpy.utils.register_class(OBJECT_OT_add_shader)



def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.utils.unregister_class(OBJECT_OT_OUTLINE)
    bpy.utils.unregister_class(VIEW3D_PT_NPRtoolkit)
    bpy.utils.unregister_class(OBJECT_OT_SHADER)
    bpy.utils.unregister_class(OBJECT_OT_COMPOSITION)
    bpy.utils.unregister_class(OBJECT_OT_add_solidify)
    bpy.utils.unregister_class(OBJECT_OT_load_bg_fx)
    bpy.utils.unregister_class(OBJECT_OT_add_shader)



if __name__ == "__main__":
    register()