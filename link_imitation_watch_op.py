from bpy.types import Operator
import bpy
from . import async_loop
from .import common
import socketio

sio = socketio.AsyncClient()


@sio.event
async def connect():
    # TODO update `rooms` auto
    genuine_files = []
    for lib in bpy.data.libraries:
        genuine_files.append(bpy.path.abspath(lib.filepath))
    print("Watching Files: ", genuine_files)
    await sio.emit('register_imitation', {'genuine_files': genuine_files})


@sio.event
async def genuine_update(data):
    print('genuine updated ', data['file_path'])
    print('reloading now')
    for lib in bpy.data.libraries:
        if bpy.path.abspath(lib.filepath) == data['file_path']:
            lib.reload()


@sio.event
async def disconnect():
    await sio.disconnect()


async def start_watch():
    if not sio.connected:
        await sio.connect(common.server_url)
        print("Start to wait now")
        await sio.wait()


class ImitationWatch_Async(async_loop.AsyncModalOperatorMixin, Operator):
    bl_idname = "link_tool.imitation_watch"
    bl_label = "Watch Update"
    bl_description = "Start to watch linked files"

    async def async_execute(self, context):
        context.scene.imitation = True
        await start_watch()


class ImitationWatch_Stop_Async(async_loop.AsyncModalOperatorMixin, Operator):
    bl_idname = "link_tool.imitation_watch_stop"
    bl_label = "Stop Watch"
    bl_description = "Stop to watch linked files"

    async def async_execute(self, context):
        context.scene.imitation = False
        await sio.disconnect()


def register():
    bpy.utils.register_class(ImitationWatch_Async)
    bpy.utils.register_class(ImitationWatch_Stop_Async)


def unregister():
    bpy.utils.unregister_class(ImitationWatch_Async)
    bpy.utils.unregister_class(ImitationWatch_Stop_Async)
