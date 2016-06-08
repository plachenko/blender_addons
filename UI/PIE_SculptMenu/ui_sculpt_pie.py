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
        
        #local sculpt variable based on current sculpt tool
        sculpt = context.tool_settings.sculpt
        
        #define the pie menu from the LAYOUT
        layout = self.layout
        pie = layout.menu_pie()
        
        #Define the column.
        col = pie.column(align=True)
        
        #define the first row -- make them buttons without spaces (alignment expand).
        row = col.row(align=True)
        row.alignment='EXPAND'   
        
        #draw the mask row...
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
        
        #try to use buttons instead of property
        #row.prop(context.tool_settings.sculpt.brush, "sculpt_tool", icon_only = True, event = True)
        
        #v iew Menu List...
        view = context.space_data
        view_col = pie.column(align=True)
        view_col.label("View Options:")
        
        view_row = view_col.row(align=True)
        view_row.alignment = "EXPAND"
        
        view_row.operator("object.shade_smooth", text="Smooth surface")
        view_row.operator("object.shade_flat", text="Flat surface")
        
        view_row = view_col.row(align=True)
        
        # matcap options...
        if context.space_data.use_matcap:
            matcap_label = "Current: "+str(context.space_data.matcap_icon)
        else:
            matcap_label = "Matcap"
        
        view_row.alignment = "EXPAND"
        view_row.prop(view, "use_matcap", text=matcap_label)
        
        #iterate through all matcap options
        if context.space_data.use_matcap:
            for i in range(1, 25):
                view_row.prop_enum(bpy.context.space_data, "matcap_icon", str(i).zfill(2), icon="MATCAP_"+str(i).zfill(2))       
                
                if i == 6 or i == 15: 
                    view_row = view_col.row(align=True)
                    view_row.alignment = "EXPAND"
                    view_row.prop_enum(bpy.context.space_data, "matcap_icon", str(i).zfill(2), icon="MATCAP_"+str(i).zfill(2))       
 
        #toggle dynamic topology
        view_row = view_col.row(align=True)
        view_row.operator("sculpt.dynamic_topology_toggle", text="Toggle Dynamic Topology", icon="MOD_DYNAMICPAINT")
        
        view_row = view_col.row(align=True)
        view_row.alignment = "EXPAND"
        if(len(context.object.modifiers)<1):
            view_row.operator("object.modifier_add", text="Multi-Res", icon='MOD_MULTIRES').type='MULTIRES'
        else:
            view_row.operator("object.multires_subdivide", text="Add", icon="MOD_SUBSURF").modifier = "Multires"
            view_row.operator("object.multires_base_apply", text="Apply", icon="FILE_TICK").modifier = "Multires"
            view_row.operator("object.modifier_remove", text="Remove", icon="CANCEL").modifier = "Multires"
            
            # TODO: Make a method to apply the multi-resolution modifier by taking the user into object mode and applying...
            #view_row.operator("object.modifier_apply", text="Apply").modifier = "Multires"
        
        #TODO: SIMPLE SUBDIVIDE MESH
        
        bot = pie.column(align=True)
 
        bot_row = bot.row(align=True)
        bot_row.scale_x = 1
        bot_row.alignment = "CENTER"
        bot_row.prop(sculpt, "lock_z", text="lock Z", toggle=True)
        bot_row.prop(sculpt, "use_symmetry_z", text="mir Z", toggle=True)
        bot_row.prop(sculpt, "tile_z", text="tile Z", toggle=True)
        
        bot_row = bot.row(align=True)
        bot_row.scale_x = 1
        bot_row.alignment = "CENTER"
        bot_row.prop(sculpt, "lock_x", text="lock X", toggle=True)
        bot_row.prop(sculpt, "use_symmetry_x", text="mir X", toggle=True)
        bot_row.prop(sculpt, "tile_x", text="tile X", toggle=True)
        
        bot_row = bot.row(align=True)
        bot_row.scale_x = 1
        bot_row.alignment = "CENTER"
        bot_row.prop(sculpt, "lock_y", text="lock Y", toggle=True)
        bot_row.prop(sculpt, "use_symmetry_y", text="mir Y", toggle=True)
        bot_row.prop(sculpt, "tile_y", text="tile Y", toggle=True)
        
        bot_row = bot.row(align=False)
        #bot_row.scale_x = .3
        bot_row.alignment = "CENTER"
        bot.prop(sculpt, "radial_symmetry", text="Radial")
        bot_row = bot.row(align=True)
        bot.prop(sculpt, "use_symmetry_feather", text="Feather")

        bot_row = bot.row(align=False)
        #bot_row.scale_x = .4
        #bot_row = bot.row(align=True)
        bot_row.prop(sculpt, "tile_offset", text="Tile Offset")

        #bpy.ops.origin.origin_set(type='ORIGIN_CENTER_OF_MASS')
        top = pie.column(align=True)
        top_row = top.row(align=True)
        top_row.operator("screen.screen_full_area", text="FullScreen").use_hide_panels = True
        top_row.prop(view, "show_only_render")
        
        top_row = top.row(align=True)
        top_row.operator("view3d.view_center_cursor", text="Center to Cursor")
        top_row.operator("view3d.snap_cursor_to_selected", text="Recenter")
        
        top_row = top.row(align=True)
        top_row.operator("view3d.view_selected", text="Center to stroke")
        
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