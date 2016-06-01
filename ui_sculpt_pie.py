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
                    if i % 2 == 0:
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
        view_row.alignment = "LEFT"
        view_row.prop(view, "use_matcap")
        view_row = view_col.row(align=True)
        view_row.alignment = "EXPAND"
        '''        
        row.prop_enum(bpy.context.space_data, "matcap_icon", "01", text="", icon="MATCAP_01")
        row.prop_enum(bpy.context.space_data, "matcap_icon", "02", text="", icon="MATCAP_02")
        row.prop_enum(bpy.context.space_data, "matcap_icon", "03", text="", icon="MATCAP_03")
        row.prop_enum(bpy.context.space_data, "matcap_icon", "04", text="", icon="MATCAP_04")
        row.prop_enum(bpy.context.space_data, "matcap_icon", "05", text="", icon="MATCAP_05")
        row.prop_enum(bpy.context.space_data, "matcap_icon", "06", text="", icon="MATCAP_06")
        row.prop_enum(bpy.context.space_data, "matcap_icon", "07", text="", icon="MATCAP_07")
        row.prop_enum(bpy.context.space_data, "matcap_icon", "08", text="", icon="MATCAP_08")
        '''
        for i in range(1, 10):
            if i%3 == 1:
                view_row = view_col.row(align=True)
                view_row.alignment = "EXPAND"
                view_row.prop_enum(bpy.context.space_data, "matcap_icon", "0"+str(i), icon="MATCAP_0"+str(i))
            else:
                view_row.prop_enum(bpy.context.space_data, "matcap_icon", "0"+str(i), icon="MATCAP_0"+str(i))
                
            #view_row.prop(view, "matcap_icon", "0"+str(i), icon="MATCAP_0"+str(i))

        sculpt = context.tool_settings.sculpt
       
        bot = pie.column(align=True)
        bot.label("res")
        bot_row = bot.row(align=True)
        bot_row.operator("sculpt.dynamic_topology_toggle", text="Dynamic Topology")
        
        bot_row = bot.row(align=True)
        bot_row.operator("object.modifier_add", text="Multi-Res", icon='MOD_MULTIRES').type='MULTIRES'
        
        bot_row = bot.row(align=True)
        bot_row.prop(sculpt, "use_symmetry_x", text="X", toggle=True)
        bot_row.prop(sculpt, "use_symmetry_y", text="Y", toggle=True)
        bot_row.prop(sculpt, "use_symmetry_z", text="Z", toggle=True)

        bot.prop(sculpt, "radial_symmetry", text="Radial")
        bot_row = bot.row(align=True)
        bot.prop(sculpt, "use_symmetry_feather", text="Feather")
        
        bot_row = bot.row(align=True)
        bot_row.label("lock")
        bot_row.prop(sculpt, "lock_x", text="X", toggle=True)
        bot_row.prop(sculpt, "lock_y", text="Y", toggle=True)
        bot_row.prop(sculpt, "lock_z", text="Z", toggle=True)

        bot_row = bot.row(align=True)
        bot_row.label("tile_offset")
        bot_row.prop(sculpt, "tile_x", text="X", toggle=True)
        bot_row.prop(sculpt, "tile_y", text="Y", toggle=True)
        bot_row.prop(sculpt, "tile_z", text="Z", toggle=True)
        
        bot_row = bot.row(align=True)
        bot_row.prop(sculpt, "tile_offset", text="Tile Offset")

       
        top = pie.column(align=True)
        top_row = top.row(align=True)
        top_row.operator("screen.screen_full_area", text="FullScreen").use_hide_panels = True
        
        top_row = top.row(align=True)
        top_row.operator("view3d.view_center_cursor", text="View From Cursor")
        
        top_row = top.row(align=True)
        top_row.operator("view3d.view_selected", text="View Last Selected")
        
        
        
def register():
    bpy.utils.register_class(VIEW3D_PIE_sculpt)
    
    #Bind S in SCULPT MODE to call the pie menu.
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Sculpt')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'S', 'PRESS')
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