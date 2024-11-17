import bpy
import bpy.utils.previews
import os
import webbrowser

translations_dict = {
    "en_US": {
        ("*", "InkTool by Wutianqing"): "InkTool 1.2 Wutianqing",
        ("*", "Inking"): "Inking",
        ("*", "InkBrush"): "InkBrush",
        ("*", "InkEdge"): "InkEdge",
        ("*","InkTexture"):"InkTexture",
        ("*","InkShadow"):"InkShadow",
        ("*", "Debris"): "Debris",
        ("*", "Distress"): "Distress",
        ("*","PaperBackground"):"PaperBg",
        ("*","Toggle Distress"):"Toggle Distress",
        ("*", "Add One"): "Add One",
        ("*", "Generators"): "Generators",
        ("*", "FX"): "Filter",
        ("*", "mylink"): "Tutorial",
    },
    'zh_HANS': {
        ("*", "InkTool by Wutianqing"): "InkTool 1.2 五天晴",
        ("*", "Inking"): "着墨",
        ("*", "InkBrush"): "笔触",
        ("*", "InkEdge"): "勾边",
        ("*","InkTexture"):"墨色",
        ("*","InkShadow"):"阴影",
        ("*", "Debris"): "点缀",
        ("*", "Distress"): "做旧",
        ("*","PaperBackground"):"宣纸背景",
        ("*","Toggle Distress"):"开关做旧",
        ("*", "Add One"): "添加",
        ("*", "Generators"): "生成器",
        ("*", "FX"): "展纸",
        ("*", "mylink"): "教程",
    },
}


bl_info = {
    "name": "InkTool",
    "author": "Wutianqing",
    "version": (1, 2),
    "blender": (4, 0, 0),
    "description": "Inking Objects",
    "category": "Object",
}

# 获取当前脚本文件的目录
current_dir = os.path.dirname(__file__)

# 构建预设文件的完整路径
PRESET_FILE_PATH = os.path.join(current_dir, "file/inkbrush.blend")
PROPS_FILE_PATH = os.path.join(current_dir, "props")
GENES_FILE_PATH = os.path.join(current_dir, "generators")
# 全局变量来存储预览集合
preview_props = {}
preview_generators = {}
# 全局变量来存储缓存的枚举项
cached_enum_props = None
cached_enum_genes = None
# 全局计数器
enum_props_counter = 0
enum_genes_counter = 0


def load_thumbnails(FILE_PATH,preview):
    print("Loading thumbnails...")
    pcoll = bpy.utils.previews.new()
    preview["main"] = pcoll

    if os.path.exists(FILE_PATH):
        for filename in os.listdir(FILE_PATH):
            if filename.endswith(".blend"):
                thumbnail_path = os.path.splitext(filename)[0] + ".png"
                print(thumbnail_path)
                thumbnail_full_path = os.path.join(FILE_PATH, thumbnail_path)
                if os.path.exists(thumbnail_full_path):
                    thumb = pcoll.load(thumbnail_path, thumbnail_full_path, 'IMAGE')
                else:
                    thumb = pcoll.load("default.png", FILE_PATH, 'IMAGE')
                print(f"Loaded {filename} with icon_id {thumb.icon_id}")
    #print(pcoll)
    return pcoll


def get_blend_props(self, context):
    global cached_enum_props
    global enum_props_counter

    # 检查缓存的枚举项是否存在
    if cached_enum_props is not None:
        return cached_enum_props
    
    pcoll = preview_props["main"]

    items = []
    if os.path.exists(PROPS_FILE_PATH):
        for filename in os.listdir(PROPS_FILE_PATH):
            if filename.endswith(".blend"):
                display_name = filename.replace('.blend', '')
                identifier = filename  # 或者任何唯一的字符串
                if display_name + ".png" in pcoll:
                    icon_id = pcoll[display_name + ".png"].icon_id
                else:
                    icon_id = 0  # 或者某个默认图标的ID
                print(f"Enum item: {display_name}, icon_id: {icon_id}")
                items.append((identifier, display_name, "", icon_id, enum_props_counter))
                #items.append((identifier, display_name, "", enum_props_counter))
                enum_props_counter += 1
    # 更新缓存
    cached_enum_props = items
    
    print(items)
    return items

def get_blend_genes(self, context):
    global cached_enum_genes
    global enum_genes_counter

    # 检查缓存的枚举项是否存在
    if cached_enum_genes is not None:
        return cached_enum_genes
    
    pcoll = preview_generators["main"]

    items = []
    if os.path.exists(GENES_FILE_PATH):
        for filename in os.listdir(GENES_FILE_PATH):
            if filename.endswith(".blend"):
                display_name = filename.replace('.blend', '')
                identifier = filename  # 或者任何唯一的字符串
                if display_name + ".png" in pcoll:
                    icon_id = pcoll[display_name + ".png"].icon_id
                else:
                    icon_id = 0  # 或者某个默认图标的ID
                print(f"Enum item: {display_name}, icon_id: {icon_id}")
                items.append((identifier, display_name, "", icon_id, enum_genes_counter))
                #items.append((identifier, display_name, "", enum_props_counter))
                enum_genes_counter += 1
    # 更新缓存
    cached_enum_genes = items
    print(items)
    return items


def update_enum_items_cache():
    global cached_enum_props
    global cached_enum_genes
    cached_enum_props = None  # 清空缓存，强制下一次调用重新生成
    cached_enum_genes = None

#NODE_GROUP_NAME = "inkbrush"


def add_geometry_nodes_modifier(obj, node_group_name):
    # 选中物体并转换为曲线
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.convert(target='CURVE')

    # 创建 Geometry Nodes Modifier
    modifier = obj.modifiers.new(name="GeometryNodes", type='NODES')

    # 加载预设文件中的节点组
    with bpy.data.libraries.load(PRESET_FILE_PATH, link=False) as (data_from, data_to):
        data_to.node_groups = [node_group_name]

    # 链接节点组到 Modifier
    modifier.node_group = bpy.data.node_groups[node_group_name]

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
    """
    为指定物体的网格数据添加一个顶点颜色层，并设置默认颜色。
    
    :param obj: 要修改的物体，必须是一个网格对象。
    :param color_layer_name: 新顶点颜色层的名称。
    :param color_value: 顶点颜色层的默认颜色值，格式为(R, G, B, A)。
    """
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



def insert_inktex_node_to_material(obj):
    # 确保物体有材质槽
    insert_color_attribute(obj, "inkmask0", (1.0, 1.0, 1.0, 1.0))
    
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
    
    
    #加载节点
    with bpy.data.libraries.load(PRESET_FILE_PATH, link=False) as (data_from, data_to):
        if "inktex" in data_from.node_groups:
            data_to.node_groups = ["inktex"]
        else:
            print("Inktex node group not found in the file.")
            return None

    # 将 inktex 节点插入到节点树中
    inktex_node = nodes.new('ShaderNodeGroup')  # 创建一个新的节点组实例
    inktex_node.node_tree = bpy.data.node_groups.get("inktex", None)  # 设置为 inktex 节点组

    # 创建连接
    if principled and image_tex:
        links.new(image_tex.outputs[0], inktex_node.inputs[0])
        links.new(inktex_node.outputs[0], material_output.inputs['Surface'])
    else:
        links.new(inktex_node.outputs[0], material_output.inputs['Surface'])



def insert_inkshadow_node_to_material(obj):
    insert_color_attribute(obj, "shadowmask0", (1.0, 1.0, 1.0, 1.0))

    # 确保物体有材质槽
    if not obj.material_slots:
        obj.data.materials.append(None)

    material = obj.material_slots[0].material
    if not material or not material.use_nodes:
        material = bpy.data.materials.new(name="New_Material")
        obj.material_slots[0].material = material
    
    material.use_nodes = True
    material.blend_method = 'HASHED'  # 设置透明度混合方式为 HASHED

    nodes = material.node_tree.nodes
    links = material.node_tree.links

     # 查找 Principled BSDF 和 Image Texture 节点
    principled = next((node for node in nodes if node.type == 'BSDF_PRINCIPLED'), None)
    image_tex = next((node for node in nodes if node.type == 'TEX_IMAGE'), None)
    material_output = next((node for node in nodes if node.type == 'OUTPUT_MATERIAL'), None)
    
    
    #加载节点
    with bpy.data.libraries.load(PRESET_FILE_PATH, link=False) as (data_from, data_to):
        if "inktex" in data_from.node_groups:
            data_to.node_groups = ["ShadowObj"]
        else:
            print("ShadowObj node group not found in the file.")
            return None

    # 将 inktex 节点插入到节点树中
    inktex_node = nodes.new('ShaderNodeGroup')  # 创建一个新的节点组实例
    inktex_node.node_tree = bpy.data.node_groups.get("ShadowObj", None)  # 设置为 inktex 节点组

    # 创建连接
    if principled and image_tex:
        links.new(image_tex.outputs[0], inktex_node.inputs[0])
        links.new(inktex_node.outputs[0], material_output.inputs['Surface'])
    else:
        links.new(inktex_node.outputs[0], material_output.inputs['Surface'])




class MyPropsProperties(bpy.types.PropertyGroup):
    # 返回了items
    props_files: bpy.props.EnumProperty(
        name="Blend Files",
        description="List of blend files",
        items=get_blend_props
    )

class MyGenesProperties(bpy.types.PropertyGroup):
    # 返回了items
    genes_files: bpy.props.EnumProperty(
        name="Blend Files",
        description="List of blend files",
        items=get_blend_genes
    )

class OBJECT_OT_load_props_object(bpy.types.Operator):
    bl_idname = "object.load_props_object"
    bl_label = "Add One"

    def execute(self, context):
        selected_file = context.scene.my_addon_props.props_files
        blend_file_path = os.path.join(PROPS_FILE_PATH, selected_file)

          # 加载选定的 .blend 文件
        with bpy.data.libraries.load(blend_file_path, link=False) as (data_from, data_to):
            data_to.objects = data_from.objects  # 加载所有物体

        # 将对象链接到当前场景
        for obj in data_to.objects:
            bpy.context.collection.objects.link(obj)
            obj.select_set(True)

        return {'FINISHED'}

class OBJECT_OT_load_genes_object(bpy.types.Operator):
    bl_idname = "object.load_genes_object"
    bl_label = "Add One"

    def execute(self, context):
        selected_file = context.scene.my_addon_genes.genes_files
        blend_file_path = os.path.join(GENES_FILE_PATH, selected_file)

        # 假设selected_file的格式为"collection_name.blend"，去除扩展名以匹配集合名称
        target_collection_name = os.path.splitext(selected_file)[0]

        # 加载选定的 .blend 文件，同时加载其中的对象和集合
        with bpy.data.libraries.load(blend_file_path, link=False) as (data_from, data_to):
            # 只加载名称与selected_file匹配的集合
            #data_to.objects = data_from.objects  # 加载所有物体
            data_to.collections = data_from.collections
            #data_to.collections = [name for name in data_from.collections if name == target_collection_name]

        # 将对象链接到当前场景
        for coll in data_to.collections:
            linked_coll = bpy.context.scene.collection.children.link(coll)
            # 在视图层中查找对应的LayerCollection
            layer_coll = find_layer_collection(bpy.context.view_layer.layer_collection, coll.name)
            if layer_coll and target_collection_name in coll.name:
                # 如果找到LayerCollection且其名称包含目标名称，则将其排除
                layer_coll.exclude = True

        return {'FINISHED'}

def find_layer_collection(layer_collection, collection_name):
    """递归搜索匹配名称的LayerCollection"""
    if layer_collection.name == collection_name:
        return layer_collection
    for child in layer_collection.children:
        result = find_layer_collection(child, collection_name)
        if result:
            return result
    return None



class OBJECT_OT_add_modifier(bpy.types.Operator):
    bl_idname = "object.add_geometry_nodes_modifier"
    bl_label = "InkBrush"
    bl_description = "Add Inkbrush to line or curve"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not context.selected_objects:
            self.report({'WARNING'}, "No objects selected")
            return {'CANCELLED'}
        
        for obj in context.selected_objects:
            add_geometry_nodes_modifier(obj, "inkbrush1")

        self.report({'INFO'}, "Modifiers added to selected objects")
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
    
class OBJECT_OT_add_inktex(bpy.types.Operator):
    bl_idname = "object.add_inktex_node"
    bl_label = "InkTexture"
    bl_description = "Add inktex to Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        obj = context.active_object
        if obj and obj.type == 'MESH':
            insert_inktex_node_to_material(obj)
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "No suitable object selected.")
            return {'CANCELLED'}

class OBJECT_OT_add_inkshadow(bpy.types.Operator):
    bl_idname = "object.add_inkshadow_node"
    bl_label = "InkShadow"
    bl_description = "Add inktex to Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        obj = context.active_object
        if obj and obj.type == 'MESH':
            insert_inkshadow_node_to_material(obj)
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "No suitable object selected.")
            return {'CANCELLED'}
        

class OBJECT_OT_load_paper_fx(bpy.types.Operator):
    bl_idname = "object.load_paper_fx"
    bl_label = "Distress"

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


class OBJECT_OT_load_bg_fx(bpy.types.Operator):
    bl_idname = "object.load_bg_fx"
    bl_label = "paperbg"

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
    
class OBJECT_OT_toggle_compositor(bpy.types.Operator):
    bl_idname = "object.toggle_compositor"
    bl_label = "Toggle Compositor"

    def execute(self, context):
        space_data = bpy.context.space_data

        # 检查是否是 3D 视图并且有 shading 属性
        if space_data and hasattr(space_data, 'shading'):
            # 根据当前值切换 use_compositor 设置
            if space_data.shading.use_compositor == 'ALWAYS':
                space_data.shading.use_compositor = 'DISABLED'
            else:
                space_data.shading.use_compositor = 'ALWAYS'
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "Not in 3D view or shading not found")
            return {'CANCELLED'}



class OBJECT_PT_custom_panel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_custom_panel"
    bl_label = "InkTool by Wutianqing"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "InkTool"

    def draw(self, context):
        layout = self.layout
        my_props = context.scene.my_addon_props
        my_genes = context.scene.my_addon_genes

        box = layout.box()
        box.label(text="Inking")
        box.operator(OBJECT_OT_add_modifier.bl_idname,  text=bpy.app.translations.pgettext("InkBrush"),icon='BRUSHES_ALL')

        box.operator(OBJECT_OT_add_solidify.bl_idname, text=bpy.app.translations.pgettext("InkEdge"), icon='MOD_EDGESPLIT')

        box.operator(OBJECT_OT_add_inktex.bl_idname, text=bpy.app.translations.pgettext("InkTexture"), icon='NODE_TEXTURE')

        box.operator(OBJECT_OT_add_inkshadow.bl_idname,  text=bpy.app.translations.pgettext("InkShadow"),icon='SHADING_RENDERED')

        box = layout.box()
        box.label(text="FX")
        box.operator(OBJECT_OT_load_bg_fx.bl_idname, text=bpy.app.translations.pgettext("PaperBackground"),icon='SEQ_PREVIEW')
        box.operator(OBJECT_OT_load_paper_fx.bl_idname,text=bpy.app.translations.pgettext("Distress"),icon='NODE_COMPOSITING')
        box.operator(OBJECT_OT_toggle_compositor.bl_idname, text=bpy.app.translations.pgettext("Toggle Distress"), icon='RESTRICT_VIEW_OFF')

        box = layout.box()
        box.label(text="Debris")
        box.template_icon_view(my_props, "props_files", show_labels=True, scale=5, scale_popup=5)
        box.operator(OBJECT_OT_load_props_object.bl_idname, text=bpy.app.translations.pgettext("Add One"))  # 假设这是新的操作符

        box = layout.box()
        box.label(text="Generators")
        box.template_icon_view(my_genes, "genes_files", show_labels=True, scale=5, scale_popup=5)
        box.operator(OBJECT_OT_load_genes_object.bl_idname, text=bpy.app.translations.pgettext("Add One"))  # 假设这是新的操作符

        box = layout.box()
        box.label(text=bpy.app.translations.pgettext("mylink"))
        box.operator("wm.open_webpage", text="b站").url = "https://www.bilibili.com/video/BV13A4m137Gq/?spm_id_from=333.788&vd_source=da64a9499307e2a8227253690b80cde6"
        box.operator("wm.open_webpage", text="youtube").url = "https://www.youtube.com/@wutianqing"

class OpenWebPageOperator(bpy.types.Operator):
    """打开外部网站"""
    bl_idname = "wm.open_webpage"
    bl_label = "打开外部网站"

    url: bpy.props.StringProperty()  # 定义一个字符串属性来存储URL

    def execute(self, context):
        webbrowser.open(self.url)  # 使用webbrowser打开URL
        return {'FINISHED'}
    

def register():
    print("Registering plugin...")
    bpy.app.translations.register(__name__, translations_dict)

    load_thumbnails(PROPS_FILE_PATH,preview_props)
    load_thumbnails(GENES_FILE_PATH,preview_generators)
    bpy.utils.register_class(MyPropsProperties)
    bpy.types.Scene.my_addon_props = bpy.props.PointerProperty(type=MyPropsProperties)
    bpy.utils.register_class(MyGenesProperties)
    bpy.types.Scene.my_addon_genes = bpy.props.PointerProperty(type=MyGenesProperties)

    bpy.utils.register_class(OBJECT_OT_load_props_object)
    bpy.utils.register_class(OBJECT_OT_add_inkshadow)
    bpy.utils.register_class(OBJECT_OT_load_bg_fx)
    
    bpy.utils.register_class(OBJECT_OT_load_genes_object)
    bpy.utils.register_class(OBJECT_OT_add_modifier)
    bpy.utils.register_class(OBJECT_OT_add_solidify)
    bpy.utils.register_class(OBJECT_OT_add_inktex)
    bpy.utils.register_class(OBJECT_OT_load_paper_fx)
    bpy.utils.register_class(OBJECT_OT_toggle_compositor)
    bpy.utils.register_class(OBJECT_PT_custom_panel)
    bpy.utils.register_class(OpenWebPageOperator)
    


def unregister():
    bpy.app.translations.unregister(__name__)
    del bpy.types.Scene.my_addon_props
    del bpy.types.Scene.my_addon_genes
    for pcoll in preview_props.values():
        bpy.utils.previews.remove(pcoll)
    preview_props.clear()
    for pcoll in preview_generators.values():
        bpy.utils.previews.remove(pcoll)
    preview_generators.clear()
    print('clear...')

    bpy.utils.unregister_class(MyPropsProperties)
    bpy.utils.unregister_class(MyGenesProperties)
    bpy.utils.unregister_class(OBJECT_OT_load_bg_fx)
    bpy.utils.unregister_class(OBJECT_OT_load_props_object)
    bpy.utils.unregister_class(OBJECT_OT_load_genes_object)
    bpy.utils.unregister_class(OBJECT_OT_add_modifier)
    bpy.utils.unregister_class(OBJECT_OT_add_solidify)
    bpy.utils.unregister_class(OBJECT_OT_add_inktex)
    bpy.utils.unregister_class(OBJECT_OT_add_inkshadow)
    bpy.utils.unregister_class(OBJECT_OT_load_paper_fx)
    bpy.utils.unregister_class(OBJECT_OT_toggle_compositor)
    bpy.utils.unregister_class(OBJECT_PT_custom_panel)
    bpy.utils.unregister_class(OpenWebPageOperator)
    update_enum_items_cache()
    
    


if __name__ == "__main__":
    register()
    #unregister()