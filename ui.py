from . import common
import bpy
from bpy.types import AddonPreferences


class LinkToolPanel(bpy.types.Panel):
    bl_idname = "VIEW_3D_PT_link_tool"
    bl_label = "NSS Link Tool"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "NSS Toolbox"

    def draw(self, context):
        text = "Update Watch" if context.scene.imitation else "Start Watch"
        self.layout.operator("link_tool.imitation_watch", text=text)

        self.layout.operator("link_tool.genuine_update_notify")
        self.layout.separator()
        if context.scene.imitation:
            self.layout.operator("link_tool.imitation_watch_stop")
        if context.scene.genuine:
            self.layout.operator("link_tool.genuine_update_notify_stop")


class LinkToolPreferences(AddonPreferences):
    bl_idname = __package__

    server_url: bpy.props.StringProperty(
        name="Server URL", default=common.server_url)

    def draw(self, _):
        self.layout.prop(self, "server_url")


def register():
    bpy.utils.register_class(LinkToolPanel)
    bpy.utils.register_class(LinkToolPreferences)


def unregister():
    bpy.utils.unregister_class(LinkToolPanel)
    bpy.utils.unregister_class(LinkToolPreferences)
