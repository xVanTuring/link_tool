import common
from aiohttp import web
import socketio

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

room_list = []


async def index(request):
    """Serve the client-side application."""
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


@sio.event
def connect(sid, environ):
    print("connect ", sid)


@sio.event
async def register_imitation(sid, data):
    rooms = sio.rooms(sid)
    genuine_files = data['genuine_files']

    for room_id in rooms:
        if room_id != sid and room_id not in genuine_files:
            sio.leave_room(sid, room_id)
    for file_path in genuine_files:
        sio.enter_room(sid, file_path)


@sio.event
async def genuine_update(sid, data):
    file_path = data['file_path']
    print("genuine_update ", file_path)
    await sio.emit("genuine_update", {'file_path': file_path}, room=file_path)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app, port=common.port)
