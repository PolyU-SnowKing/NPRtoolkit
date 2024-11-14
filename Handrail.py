import bpy
import bmesh
from mathutils import Vector

def create_cylinders_and_fence(context, radius=0.1, depth=1.0, offset=0.2, lift=0.2):
    bpy.ops.object.mode_set(mode='OBJECT')
    
    obj = context.active_object
    if obj is None or obj.type != 'MESH':
        print("Please select a mesh first")
        return
    
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    
    # Get vertex 
    selected_verts = [v for v in bm.verts if v.select]
    if not selected_verts:
        print("No vertex selected, select some to generate")
        bm.free()
        return

    cylinder_locations = []

    # Spawn Cylinder
    for vert in selected_verts:

        location = obj.matrix_world @ vert.co
        offset_location = location - (vert.normal * offset)   
        lift_location = offset_location + Vector((0, 0, lift)) 
        
        bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=lift_location)
        
        cylinder_locations.append(lift_location)
    
    # Spawn Fence
    for i in range(1, len(cylinder_locations)):

        loc1 = cylinder_locations[i - 1]
        loc2 = cylinder_locations[i]
        
        mid_location = (loc1 + loc2) / 2
        
        # Size
        distance = (loc2 - loc1).length
        box_width = distance
        box_height = depth / 1.5
        box_depth = 0.05 
        
        bpy.ops.mesh.primitive_cube_add(size=1, location=mid_location)
        box = context.active_object
        box.scale = (box_width, box_depth, box_height)
        
        # rotation
        direction = loc2 - loc1
        rotation = direction.to_track_quat('X', 'Z')
        box.rotation_euler = rotation.to_euler()

    bm.free()

# UI
class MESH_OT_create_cylinders_and_fence(bpy.types.Operator):
    """Create Handrail based on vertex"""
    bl_idname = "mesh.create_cylinders_and_fence"
    bl_label = "Create Cylinders and Fence at Vertices"
    bl_options = {'REGISTER', 'UNDO'}
    
    # modify setting
    radius: bpy.props.FloatProperty(name="Radius", default=0.1, min=0.01, max=10.0)
    depth: bpy.props.FloatProperty(name="Depth", default=1.0, min=0.01, max=10.0)
    offset: bpy.props.FloatProperty(name="Offset", default=0.2, min=0.001, max=1.0)
    lift: bpy.props.FloatProperty(name="Lift", default=0.2, min=0.001, max=1.0)
    
    def execute(self, context):
        create_cylinders_and_fence(context, self.radius, self.depth, self.offset, self.lift)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class VIEW3D_PT_create_cylinders_panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Create Cylinders and Fence at Vertices"
    bl_idname = "VIEW3D_PT_create_cylinders_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Vertex Tools'

    def draw(self, context):
        layout = self.layout
        layout.operator("mesh.create_cylinders_and_fence", text="Create Handrail on vertex")

def register():
    bpy.utils.register_class(MESH_OT_create_cylinders_and_fence)
    bpy.utils.register_class(VIEW3D_PT_create_cylinders_panel)

def unregister():
    bpy.utils.unregister_class(MESH_OT_create_cylinders_and_fence)
    bpy.utils.unregister_class(VIEW3D_PT_create_cylinders_panel)

if __name__ == "__main__":
    register()
