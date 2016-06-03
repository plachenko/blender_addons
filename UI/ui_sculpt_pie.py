import bpy
from bpy.types import Menu

bl_info = {
    "name": "Sculpt Pie Menu",
    "author": "Denis Perchenko",
    "blender": (2, 77, 0),
    "description": "Enable Pie Menu in Sculpt mode",
    "category": "User Interface",
}

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
        
        #define the first row -- make them buttons without spaces (alignment expand).
        row = col.row(align=True)
        row.alignment='EXPAND'
        
        def draw_mask_row():
            
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
        
        #iterate through all the brushes...
        i = 0
        for brush in bpy.data.brushes:
            if(brush.use_paint_sculpt):
                #if there are more than 3, enter a new line.
                if brush.name == 'Mask':
                    draw_mask_row()
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
      
        print(list(bpy.context.space_data.matcap_icon))
        
        for i in range(1, 10):
            if i%3 == 1:
                view_row = view_col.row(align=True)
                view_row.alignment = "EXPAND"
                view_row.prop_enum(bpy.context.space_data, "matcap_icon", "0"+str(i), icon="MATCAP_0"+str(i))
            else:
                view_row.prop_enum(bpy.context.space_data, "matcap_icon", "0"+str(i), icon="MATCAP_0"+str(i))
                
            #view_row.prop(view, "matcap_icon", "0"+str(i), icon="MATCAP_0"+str(i))


        sculpt = context.tool_settings.sculpt
        view_row = view_col.row(align=True)
        view_row.operator("sculpt.dynamic_topology_toggle", text="Dynamic Topology")
        
        view_row = view_col.row(align=True)
        view_row.alignment = "EXPAND"
        if(len(context.object.modifiers)<1):
            view_row.operator("object.modifier_add", text="Multi-Res", icon='MOD_MULTIRES').type='MULTIRES'
        else:
            view_row.operator("object.multires_subdivide", text="Subdivide").modifier = "Multires"
            view_row.operator("object.modifier_remove", text="Remove subdivide").modifier = "Multires"
        
        bot = pie.column(align=True)
 
        bot_row = bot.row(align=True)
        bot_row.alignment = "EXPAND"
        bot_row.prop(sculpt, "lock_z", text="lock Z", toggle=True)
        bot_row.prop(sculpt, "use_symmetry_z", text="mirror Z", toggle=True)
        bot_row.prop(sculpt, "tile_z", text="tile Z", toggle=True)
        
        bot_row = bot.row(align=True)
        bot_row.alignment = "EXPAND"
        bot_row.prop(sculpt, "lock_x", text="lock X", toggle=True)
        bot_row.prop(sculpt, "use_symmetry_x", text="mirror X", toggle=True)
        bot_row.prop(sculpt, "tile_x", text="tile X", toggle=True)
        
        bot_row = bot.row(align=True)
        bot_row.alignment = "EXPAND"
        bot_row.prop(sculpt, "lock_y", text="lock Y", toggle=True)
        bot_row.prop(sculpt, "use_symmetry_y", text="mirror Y", toggle=True)
        bot_row.prop(sculpt, "tile_y", text="tile Y", toggle=True)
        
        bot_row = bot.row(align=True)
        
        bot_row = bot.row(align=True)
        bot_row.alignment = "EXPAND"
        bot.prop(sculpt, "radial_symmetry", text="Radial")
        bot_row = bot.row(align=True)
        bot.prop(sculpt, "use_symmetry_feather", text="Feather")

        '''
        bot.prop(sculpt, "radial_symmetry", text="Radial")
        bot_row = bot.row(align=True)
        bot.prop(sculpt, "use_symmetry_feather", text="Feather")

        
        bot_row = bot.row(align=True)
        bot_row.label("lock")
        '''
        
        #bot_row = bot.row(align=True)
        #bot_row.label("tile_offset")
        #bot_row.prop(sculpt, "tile_z", text="Z", toggle=True)
        
        #bot_row = bot.row(align=True)
        #bot_row.prop(sculpt, "tile_offset", text="Tile Offset")

       
        top = pie.column(align=True)
        top_row = top.row(align=True)
        top_row.operator("screen.screen_full_area", text="FullScreen").use_hide_panels = True
        
        top_row = top.row(align=True)
        top_row.operator("view3d.view_center_cursor", text="View From Cursor")
        
        top_row = top.row(align=True)
        top_row.operator("view3d.view_selected", text="View Last Selected")
        
        
        top_right = pie.column(align=False)
        topR_row = top_right.row(align=True)
        
        top_left = pie.column(align=False)
        topL_row = top_left.row(align=True)
        
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