import re
import json
import datetime
from aiohttp import web
from MCRcon import MCRcon
from Setting import WebServerSetting
from getServerStatus import getStatus
from Encryption import decrypt, encrypt

routes = web.RouteTableDef()


async def rcon(address, port, password, command):
    try:
        with MCRcon(address, password, port) as mcr:
            r = mcr.command(command)
        r = re.sub('§[0-9a-fk-or]', '', r, re.IGNORECASE)
        return r
    except Exception:
        return 'RCON执行遇到错误'


@routes.get('/')
async def get_handler(request):
    return web.Response(text='Python Robot Server is running')


@routes.post('/rcon')
async def post_handler(request):
    data = await request.text()
    print('[{}] rcon command executed'.format(datetime.datetime.now().strftime('%m-%d %H:%M:%S')), end='  ')
    try:
        json_source = await decrypt(data)
        json_data = json.loads(json_source)
    except Exception:
        print('Decryption Error')
        return web.Response(text='Decryption Error', status=500)
    if 'address' not in json_data:
        print('address Missing')
        return web.Response(text='address Missing', status=500)
    elif 'port' not in json_data:
        print('port Missing')
        return web.Response(text='port Missing', status=500)
    elif 'password' not in json_data:
        print('password Missing')
        return web.Response(text='password Missing', status=500)
    elif 'command' not in json_data:
        print('command Missing')
        return web.Response(text='command Missing', status=500)

    result = await rcon(
        json_data['address'],
        json_data['port'],
        json_data['password'],
        json_data['command']
    )

    result = await encrypt(str(result))

    print('')

    return web.Response(text=result)


@routes.post('/list')
async def post_handler(request):
    data = await request.text()
    print('[{}] list command executed'.format(datetime.datetime.now().strftime('%m-%d %H:%M:%S')), end='  ')
    try:
        json_source = await decrypt(data)
        json_data = json.loads(json_source)
    except Exception:
        print('Decryption Error')
        return web.Response(text='Decryption Error', status=500)

    try:
        for i in json_data.values():
            if ('ip' not in i) or ('port' not in i) or ('type' not in i):
                return web.Response(text='Missing Data', status=500)
    except Exception:
        return web.Response(text='Missing Data', status=500)

    result = await getStatus(json_data)
    result = await encrypt(str(result))

    print('')

    return web.Response(text=result)


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host=WebServerSetting['host'], port=WebServerSetting['port'])
