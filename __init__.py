import site
import sys
if site.getusersitepackages() not in sys.path:
    sys.path.append(site.getusersitepackages())

from . import async_loop
from . import link_notify_op
from . import ui
from . import link_imitation_watch_op


import bpy
from bpy.app.handlers import persistent

bl_info = {
    "name": "Link Tool",
    "author": "xVanTuring(@foxmail.com)",
    "blender": (2, 80, 0),
    "version": (1, 0, 0),
    "description": "An Addon For link",
    "category": "Scene"
}


@persistent
def save_handler(dummy):
    if bpy.context.scene.genuine:
        bpy.ops.link_tool.genuine_update_notify()


@persistent
def load_handler(dummy):
    print("Post Load")
    if bpy.context.scene.imitation:
        bpy.ops.link_tool.imitation_watch()


def register():
    async_loop.register()
    link_notify_op.register()
    link_imitation_watch_op.register()
    ui.register()

    bpy.app.handlers.save_post.append(save_handler)
    bpy.app.handlers.load_post.append(load_handler)
    bpy.types.Scene.genuine = bpy.props.BoolProperty(name="Genuine")
    bpy.types.Scene.imitation = bpy.props.BoolProperty(name="Imitation")


def unregister():
    ui.unregister()
    link_imitation_watch_op.unregister()
    link_notify_op.unregister()
    async_loop.unregister()
