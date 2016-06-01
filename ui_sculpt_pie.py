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
            if(brush.use_paint_sculpt):
                #if there are more than 3, enter a new line.
                if i % 3 == 0:
                    if brush.name == 'Mask':
                        #this is a hack, Probably should be in a seperate function...
                        col.row().separator()
                        mask_row = col.row(align=True)    
                        
                        mask = mask_row.operator(
                            "paint.mask_flood_fill"
                            , text = "Clear Mask"
                        )
                        mask.mode = "VALUE"
                        mask.value = 0
                        
                        mask_row.operator(
                            "paint.mask_flood_fill"
                            , text = "Invert Mask"
                        ).mode = "INVERT"
                            
                        mask_row.operator(
                            "paint.brush_select"
                            , text = brush.name
                            , icon_value = layout.icon(brush)
                        ).sculpt_tool = brush.sculpt_tool
                        col.row().separator()
                    else:
                        
                        row = col.row(align=True)
                        row.alignment = 'EXPAND'
                
                #each row attaches a brush operation based on current iteration
                        row.operator(
                            "paint.brush_select"
                            , text = brush.name
                            , icon_value = layout.icon(brush)
                        ).sculpt_tool = brush.sculpt_tool
                        i = i + 1
                else:
                        row.operator(
                            "paint.brush_select"
                            , text = brush.name
                            , icon_value = layout.icon(brush)
                        ).sculpt_tool = brush.sculpt_tool
                        i = i + 1
        view = context.space_data
        view_col = pie.column(align=True)
        view_col.label("View Options:")
        view_row = view_col.row(align=True)
        view_row.prop(view, "use_matcap")
        #view_row.operator("SpaceView3d.matcap_icon")
       
        bot = pie.column(align=True)
        bot.label("")
        bot_row = bot.row(align=True)
       
        top = pie.column(align=True)
        top_row = top.row(align=True)
        top_row.operator("screen.screen_full_area", text="FullScreen").use_hide_panels = True
        top_row.operator("view3d.view_center_cursor", text="View")
        
        
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