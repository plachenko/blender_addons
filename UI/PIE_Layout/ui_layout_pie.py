import bpy
from bpy.types import Menu

class custom_view(bpy.types.Operator):
    bl_idname = "object.view_menu"
    bl_label = "view mode"
    variable = bpy.props.StringProperty()
    
    @classmethod
    def poll(cls, context):
        return true
    
    def execute(self, context):
        bpy.context.area.type = self.variable
        return {'FINISHED'}

class custom_pie(Menu):
    bl_idname = "window.pie_layout"
    bl_label = "Select Label"
    
    def draw(self, context):
        layout = self.layout
        
        pie = layout.menu_pie()
        
        #LEFT
        pie.operator("object.view_menu", text="Timeline", icon="TIME").variable = "TIMELINE"
        #RIGHT
        pie.operator("object.view_menu", text="Text", icon="TEXT").variable = "TEXT_EDITOR"
        #BOTTOM
        pie.operator("object.view_menu", text="Text", icon="VIEW3D").variable = "VIEW_3D"
        #TOP
        pie.operator("object.view_menu", text="Text", icon="TEXT").variable = "TEXT_EDITOR"
        #TOP RIGHT
        pie.operator("object.view_menu", text="Text", icon="TEXT").variable = "TEXT_EDITOR"
        #TOP LEFT
        pie.operator("object.view_menu", text="Text", icon="TEXT").variable = "TEXT_EDITOR"
        #BOT RIGHT
        pie.operator("object.view_menu", text="Text", icon="TEXT").variable = "TEXT_EDITOR"
        #BOT LEFT

def register():
    bpy.utils.register_class(custom_view)
    bpy.utils.register_class(custom_pie)
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name="Window")
    kmi = km.keymap_items.new("wm.call_menu_pie", "SPACE", "PRESS", shift=True, ctrl = True).properties.name = "window.pie_layout"
    
def unregister():
    bpy.utils.unregister_class(custom_pie)    

if __name__ == "__main__":
    register()