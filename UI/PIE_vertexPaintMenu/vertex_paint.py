import bpy
from bpy.types import Menu

# spawn an edit mode selection pie (run while object is in edit mode to get a valid output)



class VIEW3D_PIE_template(Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "Select Mode"
    
    @staticmethod
    def prop_unified_color_picker(parent, context, brush, prop_name, value_slider=True):
        ups = context.tool_settings.unified_paint_settings
        ptr = ups if ups.use_unified_color else brush
        parent.template_color_picker(ptr, prop_name, value_slider=value_slider)
    
    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        col = pie.column()
        # operator_enum will just spread all available options
        # for the type enum of the operator on the pie
        #pie.operator_enum("mesh.select_mode", "type")
        
        brush = bpy.data.brushes['Draw']
        
        col.template_color_picker(brush, "color")
        #col.template_palette(brush.paint_settings(context), "palette", color=True)
        col.prop(self.paint_settings(context), "vertext_tool")
        

def register():
    bpy.utils.register_class(VIEW3D_PIE_template)


def unregister():
    bpy.utils.unregister_class(VIEW3D_PIE_template)


if __name__ == "__main__":
    register()

    bpy.ops.wm.call_menu_pie(name="VIEW3D_PIE_template")
