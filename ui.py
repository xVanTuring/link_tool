import bpy


class NSSUpdateToolPanel(bpy.types.Panel):
    bl_idname = "VIEW_3D_PT_link_tool"
    bl_label = "NSS Link Tool"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "NSS Addon Manager"

    def draw(self, context):
        text = "Update Watch" if context.scene.imitation else "Start Watch"
        self.layout.operator("link_tool.imitation_watch", text=text)

        self.layout.operator("link_tool.genuine_update_notify")
        self.layout.separator()
        if context.scene.imitation:
            self.layout.operator("link_tool.imitation_watch_stop")
        if context.scene.genuine:
            self.layout.operator("link_tool.genuine_update_notify_stop")


def register():
    bpy.utils.register_class(NSSUpdateToolPanel)


def unregister():
    bpy.utils.unregister_class(NSSUpdateToolPanel)
