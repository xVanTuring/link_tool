import bpy
from bpy.types import AddonPreferences
from bpy.props import StringProperty, BoolProperty
from . import install_lib


class LinkToolPreferences(AddonPreferences):
    bl_idname = __package__
    server_url: StringProperty(name="Server Url",
                               default="http://127.0.0.1:8173")
    auto_start_server: BoolProperty(name="Auto Start Server", default=False)

    def draw(self, _):
        layout = self.layout
        if not install_lib.deps_status:
            draw_install_deps(layout)
            return
        self.layout.prop(self, "server_url")
        self.layout.prop(self, "auto_start_server")


def draw_install_deps(layout):
    box = layout.box()
    if install_lib.display_restart:
        box.label(text="Installation completed! Please restart blender")
        box.operator("wm.quit_blender")
    else:
        box.label(text="Install Dependencies and restart blender afterwards.")
        box.operator("link_tool.install_deps")


def register():
    bpy.utils.register_class(LinkToolPreferences)


def unregister():
    bpy.utils.unregister_class(LinkToolPreferences)