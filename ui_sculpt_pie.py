import bpy
from bpy.types import Menu

class VIEW3D_PIE_sculpt(Menu):
    
    bl_label = "Sculpt Menu"
    bl_idname = "sculpt.brush_pie"
    
    #Draw the pie menu...
    
    def draw(self, context):
        
        #define the pie menu from the LAYOUT
        layout = self.layout
        pie = layout.menu_pie()
        
        #Define the column.
        col = pie.column(align=True)
        col.label("Brushes")
        
        #define the first row -- make them buttons without spaces (alignment expand).
        row = col.row(align=True)
        row.alignment='EXPAND'
        
        #iterate through all the brushes...
        i = 0
        for brush in bpy.data.brushes:
            #if there are more than 3, enter a new line.
            if i <= 2:
                #each row attaches a brush operation based on current iteration
                row.operator(
                    "paint.brush_select"
                    , text = brush.name
                    #, icon = 'BRUSH_'+brush.sculpt_tool
                ).sculpt_tool = brush.sculpt_tool
                i = i + 1
            else:
                #do the next row.
                row = col.row(align=True)
                row.alignment = 'EXPAND'
                i = 0
                
def register():
    bpy.utils.register_class(VIEW3D_PIE_sculpt)
    
    #Bind X in SCULPT MODE to call the pie menu.
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Sculpt')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'X', 'PRESS')
    kmi.properties.name = "sculpt.brush_pie"
    
def unregister():
    bpy.utils.unregister_class(VIEW3D_PIE_sculpt)
     
if __name__ == "__main__":
    register()
    
    
    '''
        # Trash....
        # ... for the future!
        
        row = col.row(align=True)
        row.alignment = 'EXPAND'
        
        
        pie.operator("paint.brush_select", text='Simplify').sculpt_tool='SIMPLIFY'
        
        col = pie.column()
        row = col.row()
        row.operator("paint.brush_select", text="Crease", icon='BRUSH_CREASE').sculpt_tool='CREASE'
        
        row = col.row()
        row.operator("paint.brush_select", text="Clay", icon='BRUSH_CLAY').sculpt_tool='CLAY'
        row.operator("paint.brush_select", text='Flatten', icon='BRUSH_FLATTEN').sculpt_tool='FLATTEN'
        row.operator("paint.brush_select", text='Brush', icon='BRUSH_SCULPT_DRAW').sculpt_tool='DRAW'
        
        row = col.row()
        row.operator("paint.brush_select", text='Inflate', icon='BRUSH_INFLATE').sculpt_tool='INFLATE'
        row.operator("paint.brush_select", text='Grab', icon='BRUSH_GRAB').sculpt_tool='GRAB'
        row.operator("paint.brush_select", text='Simplify', icon='BRUSH_DATA').sculpt_tool='SIMPLIFY'
        
        row.operator("paint.brush_select", text='Inflate', icon='BRUSH_INFLATE').sculpt_tool='INFLATE'
        row.operator("paint.brush_select", text='Grab', icon='BRUSH_GRAB').sculpt_tool='GRAB'
        row.operator("paint.brush_select", text='Simplify', icon='BRUSH_DATA').sculpt_tool='SIMPLIFY'
        
        brushes = [
            ['SculptDraw'],
            ['Clay']
        ]
        
        row.operator("paint.brush_select", text='Draw', icon='BRUSH_DRAW').sculpt_tool='DRAW'
        row.operator("paint.brush_select", text='Grab', icon='BRUSH_GRAB').sculpt_tool='GRAB'
        row.operator("paint.brush_select", text='Simplify', icon='BRUSH_DATA').sculpt_tool='SIMPLIFY'
        
        #-- future reference --#
        #box = col.box()
        #bpy.ops.wm.call_menu_pie(name="sculpt.brush_pie")
        #row.prop(mesh, "auto_smooth_angle", text="angle", slider=True)
        '''