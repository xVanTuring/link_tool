import bpy
from bpy.types import Operator

from . import install_lib
from . import async_loop
import subprocess
import sys
import os
from . import utils


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


class LinkToolShutdownServer_Async(async_loop.AsyncModalOperatorMixin,
                                   Operator):
    bl_idname = "link_tool.shutdown"
    bl_label = "Shutdown Server"
    bl_description = "Start to notify"

    async def async_execute(self, context):
        import psutil
        pid = utils.server_pid()
        print("Killing PID", pid)
        if pid:
            p = psutil.Process(pid)
            # p.terminate()
            p.kill()
            print("Killing Done!")


class LinkToolStartServer(Operator):

    bl_idname = "link_tool.start_server"
    bl_label = "Start Server"
    bl_description = "Start server"

    def execute(self, context):
        python_path = sys.executable
        if bpy.app.version[1] < 90:
            python_path = bpy.app.binary_path_python

        ADDON_DIR = os.path.join(os.path.dirname(__file__))
        if os.name == "nt":
            CREATE_NEW_PROCESS_GROUP = 0x00000200
            DETACHED_PROCESS = 0x00000008
            p = subprocess.Popen([python_path, 'server.py'],
                                 cwd=os.path.join(ADDON_DIR, "./server"),
                                 stdin=None,
                                 stdout=None,
                                 stderr=None,
                                 shell=True,
                                 creationflags=DETACHED_PROCESS
                                 | CREATE_NEW_PROCESS_GROUP)
        else:
            print(os.path.join(ADDON_DIR, "server", "server.py"))
            p = subprocess.Popen([
                "nohup", python_path,
                os.path.join(ADDON_DIR, "server", "server.py")
            ], )
        print("Server started: ", p.pid)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(LinkToolOTInstallDeps)
    bpy.utils.register_class(LinkToolShutdownServer_Async)
    bpy.utils.register_class(LinkToolStartServer)


def unregister():
    bpy.utils.unregister_class(LinkToolStartServer)
    bpy.utils.unregister_class(LinkToolOTInstallDeps)
    bpy.utils.unregister_class(LinkToolShutdownServer_Async)