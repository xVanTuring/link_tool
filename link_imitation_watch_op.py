import os
from bpy.types import Operator
import bpy
from . import async_loop
import socketio

sio = socketio.AsyncClient()


async def register_imitation():
    # TODO update `rooms` auto
    genuine_files = []
    for lib in bpy.data.libraries:
        genuine_files.append(os.path.abspath(bpy.path.abspath(lib.filepath)))
    print("Watching Files: ", genuine_files)
    await sio.emit('register_imitation', {'genuine_files': genuine_files})


@sio.event
async def connect():
    await register_imitation()


@sio.event
async def genuine_update(data):
    print('genuine updated ', data['file_path'])
    print('reloading now')
    for lib in bpy.data.libraries:
        if os.path.abspath(bpy.path.abspath(lib.filepath)) == data['file_path']:
            lib.reload()


@sio.event
async def disconnect():
    await sio.disconnect()


async def start_watch(server_url):
    if not sio.connected:
        await sio.connect(server_url)
        print("Start to wait now")
        await sio.wait()
    else:
        await register_imitation()


class ImitationWatch_Async(async_loop.AsyncModalOperatorMixin, Operator):
    bl_idname = "link_tool.imitation_watch"
    bl_label = "Watch Update"
    bl_description = "Start to watch linked files"

    async def async_execute(self, context):
        context.scene.imitation = True
        server_url = context.preferences.addons[__package__].preferences.server_url
        await start_watch(server_url)


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
