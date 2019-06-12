from aiohttp import web
import socketio

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)

@sio.on('data')
async def message(sid, data):
    fi = open('./tmp.txt', 'r')
    if(fi.read()!=data):
        fo = open('./tmp.txt', 'w')
        fo.write(data)
        fo.close()
        await sio.emit('reply', data)

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    web.run_app(app)