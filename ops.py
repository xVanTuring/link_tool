import bpy
from bpy.types import Operator

from . import install_lib


def ShowMessageBox(message="", title="Message Box", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


def refresh_panel(context):
    if context.area is not None:
        for region in context.area.regions:
            if region.type == "UI":
                region.tag_redraw()
                break
    else:
        print("Context.Area is None, Forcing updating all VIEW_3D-UI")
        for window in context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    for region in area.regions:
                        if region.type == "UI":
                            region.tag_redraw()
                            break
                    break


class LinkToolOTInstallDeps(Operator):
    bl_idname = "link_tool.install_deps"
    bl_label = "Install Dependencies"
    bl_description = "Install Dependencies"

    def execute(self, context):
        state = install_lib.ensure_libs()
        refresh_panel(context)
        if state:
            install_lib.display_restart = True
        else:
            ShowMessageBox(
                "Something went wrong! Please contact the developer.")
        return {'FINISHED'}


def register():

    bpy.utils.register_class(LinkToolOTInstallDeps)


def unregister():
    bpy.utils.unregister_class(LinkToolOTInstallDeps)