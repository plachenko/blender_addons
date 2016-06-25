import bpy
from bpy.types import Menu

bl_info = {
    "name": "Layout Pie Menu",
    "author": "Denis Perchenko",
    "blender": (2, 77, 0),
    "description": "Enable Layout Menu",
    "category": "User Interface",
}

class custom_view(bpy.types.Operator):
    bl_idname = "object.view_menu"
    bl_label = "view mode"
    variable = bpy.props.StringProperty()
    
    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        bpy.context.area.type = self.variable
        return {'FINISHED'}

class custom_pie(Menu):
    bl_idname = "window.pie_layout"
    bl_label = ""
    
    def draw(self, context):
        layout = self.layout
        
        pie = layout.menu_pie()
        
        #LEFT
        col = pie.column()
        row = col.row(align=True)
        
        row.operator("object.view_menu", text=" ", icon="NLA").variable = "DOPESHEET_EDITOR"
        row.operator("object.view_menu", text=" ", icon="ACTION").variable = "DOPESHEET_EDITOR"
        row.operator("object.view_menu", text=" ", icon="IPO").variable = "GRAPH_EDITOR"
        
        row = col.row(align=True)
        row.operator("object.view_menu", text="  ", icon="TIME").variable = "TIMELINE"
         
        #RIGHT
        col = pie.column()
        row = col.row(align=True)
        row.operator("object.view_menu", text=" ", icon="IMAGE_COL").variable = "IMAGE_EDITOR"
        row.operator("object.view_menu", text=" ", icon="SEQUENCE").variable = "SEQUENCE_EDITOR"
        row.operator("object.view_menu", text=" ", icon="CLIP").variable = "CLIP_EDITOR"
        
        row = col.row(align=True)
        row.operator("object.view_menu", text=" ", icon="TEXT").variable = "TEXT_EDITOR"
        row.operator("object.view_menu", text=" ", icon="NODETREE").variable = "NODE_EDITOR"
        row.operator("object.view_menu", text=" ", icon="LOGIC").variable = "LOGIC_EDITOR"
        
        #TOP RIGHT
        col = pie.column()
        row = col.row(align=True)
        row.operator("object.view_menu", text=" ", icon="BUTS").variable = "PROPERTIES"
        row.operator("object.view_menu", text=" ", icon="OOPS").variable = "OUTLINER"
        row.operator("object.view_menu", text=" ", icon="PREFERENCES").variable = "USER_PREFERENCES"
        
        row = col.row(align=True)
        row.alignment = "EXPAND"
        row.operator("object.view_menu", text="  ", icon="INFO").variable = "INFO"
        
        #TOP LEFT
        col = pie.column()
        row = col.row(align=True)
        
        row.operator("object.view_menu", text=" ", icon="FILESEL").variable = "FILE_BROWSER"
        row.operator("object.view_menu", text=" ", icon="VIEW3D").variable = "VIEW_3D"
        row.operator("object.view_menu", text=" ", icon="CONSOLE").variable = "CONSOLE"

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