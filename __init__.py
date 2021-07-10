bl_info = {
    "name": "Link Tool",
    "author": "xVanTuring(@foxmail.com)",
    "blender": (2, 80, 0),
    "version": (1, 0, 0),
    "location": "View3D > Properties > Link Tool",
    "description": "An Addon For link",
    "category": "Scene"
}
import site
import sys
import os
from . import install_lib
from . import utils
if site.getusersitepackages() not in sys.path:
    sys.path.append(site.getusersitepackages())

import bpy
from bpy.app.handlers import persistent


@persistent
def save_handler(dummy):
    if install_lib.has_libs():
        if bpy.context.scene.genuine:
            bpy.ops.link_tool.genuine_update_notify()


@persistent
def load_handler(dummy):
    if install_lib.has_libs():
        auto_start_server = bpy.context.preferences.addons[
            __package__].preferences.auto_start_server
        if auto_start_server and not utils.has_server():
            bpy.ops.linkt_tool.start_server()
            # TODO: Sleep

        if bpy.context.scene.imitation:
            bpy.ops.link_tool.imitation_watch()


def register():
    from . import async_loop
    from . import ops
    from . import preference
    async_loop.register()
    if install_lib.has_libs():
        from . import ui
        from . import link_notify_op
        from . import link_imitation_watch_op
        link_notify_op.register()
        link_imitation_watch_op.register()
        ui.register()
        install_lib.deps_status = True
    preference.register()
    ops.register()

    bpy.app.handlers.save_post.append(save_handler)
    bpy.app.handlers.load_post.append(load_handler)
    bpy.types.Scene.genuine = bpy.props.BoolProperty(name="Genuine")
    bpy.types.Scene.imitation = bpy.props.BoolProperty(name="Imitation")


def unregister():
    from . import async_loop
    from . import ops
    from . import preference
    ops.unregister()
    if "socketio" in globals():
        from . import link_notify_op
        from . import link_imitation_watch_op
        from . import ui
        ui.unregister()
        link_imitation_watch_op.unregister()
        link_notify_op.unregister()
    async_loop.unregister()
    preference.unregister()
