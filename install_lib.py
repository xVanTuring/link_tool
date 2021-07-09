"""
Code Adopted from Radeon ProRender
"""
import bpy
import platform
import site
import subprocess
import sys

OS = platform.system()
IS_WIN = OS == 'Windows'
IS_MAC = OS == 'Darwin'
IS_LINUX = OS == 'Linux'
python_path = sys.executable
if bpy.app.version[2] < 90:
    python_path = bpy.app.binary_path_python

# adding user site-packages path to sys.path
if site.getusersitepackages() not in sys.path:
    sys.path.append(site.getusersitepackages())


def run_module_call(*args):
    """Run Blender Python with arguments on user access level"""
    module_args = ('-m', *args, '--user')
    subprocess.check_call([python_path, *module_args], timeout=60.0)


def run_pip(*args):
    """Run 'pip install' with current user access level"""
    return run_module_call('pip', 'install', *args)


def has_libs():
    try:
        import socketio
        import aiohttp
        return socketio is not None and aiohttp is not None
    except ImportError:
        return False


def ensure_libs():
    try:
        import socketio
        import aiohttp
        return socketio is not None and aiohttp is not None
    except ImportError:
        try:
            if IS_MAC or IS_LINUX:
                run_module_call("ensurepip", '--upgrade')
            run_pip("--upgrade", "pip")
            run_pip("wheel")
            run_pip("python-socketio")
            run_pip("aiohttp")
            return True
        except subprocess.SubprocessError as e:
            print("Something went wrong, unable to install py7zr", e)
        return False


deps_status = False
display_restart = False
