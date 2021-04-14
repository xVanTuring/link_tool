import bpy
from bpy.types import Operator
from . import async_loop
from . import common
import socketio

sio = socketio.AsyncClient()


@sio.event
async def connect():
    genuine_files = []
    for lib in bpy.data.libraries:
        genuine_files.append(bpy.path.abspath(lib.filepath))
    await sio.emit('genuine_update', {'file_path': bpy.data.filepath})


async def notify():
    if not sio.connected:
        await sio.connect(common.server_url)
        await sio.wait()
    else:
        await sio.emit('genuine_update', {'file_path': bpy.data.filepath})


class NotifyGenuineUpdate_Async(async_loop.AsyncModalOperatorMixin, Operator):
    bl_idname = "link_tool.genuine_update_notify"
    bl_label = "Notify Update"
    bl_description = "1"

    async def async_execute(self, context):
        context.scene.genuine = True
        await notify()


class NotifyGenuineUpdateStop_Async(async_loop.AsyncModalOperatorMixin, Operator):
    bl_idname = "link_tool.genuine_update_notify_stop"
    bl_label = "Stop Notify"
    bl_description = "Stop to notify"

    async def async_execute(self, context):
        context.scene.genuine = False
        await sio.disconnect()


def register():
    bpy.utils.register_class(NotifyGenuineUpdate_Async)
    bpy.utils.register_class(NotifyGenuineUpdateStop_Async)


def unregister():
    bpy.utils.unregister_class(NotifyGenuineUpdate_Async)
    bpy.utils.unregister_class(NotifyGenuineUpdateStop_Async)
