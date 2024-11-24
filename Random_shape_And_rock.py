
import bpy
import bmesh
import random


# Random Vertex
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


# Create random rock
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


# Set property
def register_properties():
    bpy.types.Scene.rock_size = bpy.props.FloatProperty(
        name="Rock Size",
        description="Base size of the rock",
        default=1.0,
        min=0.1,
        max=2,
    )
    bpy.types.Scene.random_amount = bpy.props.FloatProperty(
        name="Random Amount",
        description="Amount of random displacement",
        default=0.1,
        min=0.05,
        max=0.15,
    )
    bpy.types.Scene.subdivisions = bpy.props.IntProperty(
        name="Subdivisions",
        description="Number of subdivisions for the base sphere",
        default=1,
        min=1,
        max=2,
    )


def unregister_properties():
    del bpy.types.Scene.rock_size
    del bpy.types.Scene.random_amount
    del bpy.types.Scene.subdivisions


def register():
    bpy.utils.register_class(MESH_OT_advanced_randomize_vertices)
    bpy.utils.register_class(MESH_OT_generate_random_rock)
    bpy.utils.register_class(VIEW3D_PT_vertex_rock_tools)
    register_properties()


def unregister():
    bpy.utils.unregister_class(MESH_OT_advanced_randomize_vertices)
    bpy.utils.unregister_class(MESH_OT_generate_random_rock)
    bpy.utils.unregister_class(VIEW3D_PT_vertex_rock_tools)
    unregister_properties()


if __name__ == "__main__":
    register()
