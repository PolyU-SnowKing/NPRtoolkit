import bpy
import random

#Random Spread Objects
class OBJECT_OT_random_place(bpy.types.Operator):
    """Randomly place objects in a defined range"""
    bl_idname = "object.random_place"
    bl_label = "Random Place Objects"
    bl_options = {'REGISTER', 'UNDO'}

    count: bpy.props.IntProperty(name="Number of Copies", default=10, min=1)
    min_x: bpy.props.FloatProperty(name="Min X", default=-10.0)
    max_x: bpy.props.FloatProperty(name="Max X", default=10.0)
    min_y: bpy.props.FloatProperty(name="Min Y", default=-10.0)
    max_y: bpy.props.FloatProperty(name="Max Y", default=10.0)
    min_z: bpy.props.FloatProperty(name="Min Z", default=0.0)
    max_z: bpy.props.FloatProperty(name="Max Z", default=5.0)

    def execute(self, context):
        props = context.scene.random_place_props  
        selected_objects = context.selected_objects
        if not selected_objects:
            self.report({'WARNING'}, "No objects selected!")
            return {'CANCELLED'}
        
        for _ in range(props.count):
            obj = random.choice(selected_objects)
            new_obj = obj.copy()
            new_obj.location = (
                random.uniform(props.min_x, props.max_x),
                random.uniform(props.min_y, props.max_y),
                random.uniform(props.min_z, props.max_z)
            )
            context.collection.objects.link(new_obj)
        
        return {'FINISHED'}

#Adjustment setting
class RandomPlaceProperties(bpy.types.PropertyGroup):
    count: bpy.props.IntProperty(name="Number of Copies", default=10, min=1)
    min_x: bpy.props.FloatProperty(name="Min X", default=-10.0)
    max_x: bpy.props.FloatProperty(name="Max X", default=10.0)
    min_y: bpy.props.FloatProperty(name="Min Y", default=-10.0)
    max_y: bpy.props.FloatProperty(name="Max Y", default=10.0)
    min_z: bpy.props.FloatProperty(name="Min Z", default=0.0)
    max_z: bpy.props.FloatProperty(name="Max Z", default=5.0)

#UI
class OBJECT_PT_random_place_panel(bpy.types.Panel):
    """Panel for Random Object Placer"""
    bl_label = "Random Object Placer"
    bl_idname = "OBJECT_PT_random_place_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Custom"

    def draw(self, context):
        layout = self.layout
        props = context.scene.random_place_props 
        
        layout.label(text="Random Placement Tool")
        layout.prop(props, "count")
        layout.prop(props, "min_x")
        layout.prop(props, "max_x")
        layout.prop(props, "min_y")
        layout.prop(props, "max_y")
        layout.prop(props, "min_z")
        layout.prop(props, "max_z")
        
        layout.operator("object.random_place", text="Random Place Objects")

def register():
    bpy.utils.register_class(OBJECT_OT_random_place)
    bpy.utils.register_class(RandomPlaceProperties)
    bpy.utils.register_class(OBJECT_PT_random_place_panel)
    bpy.types.Scene.random_place_props = bpy.props.PointerProperty(type=RandomPlaceProperties)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_random_place)
    bpy.utils.unregister_class(RandomPlaceProperties)
    bpy.utils.unregister_class(OBJECT_PT_random_place_panel)
    del bpy.types.Scene.random_place_props

if __name__ == "__main__":
    register()
