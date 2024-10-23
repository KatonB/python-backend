import json
from http import HTTPStatus
from urllib.parse import parse_qs


def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b


def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


async def app(scope, receive, send):
    if scope['type'] == 'lifespan':
        while True:
            message = await receive()
            if message['type'] == 'lifespan.startup':
                await send({'type': 'lifespan.startup.complete'})
            elif message['type'] == 'lifespan.shutdown':
                await send({'type': 'lifespan.shutdown.complete'})
                break

    if scope['type'] == 'http':
        path = scope['path']
        method = scope['method']

        if method in ('GET', 'POST') and (path == '/' or path == '/not_found'):
            await send({
                'type': 'http.response.start',
                'status': HTTPStatus.NOT_FOUND,
                'headers': [(b'content-type', b'application/json')]
            })
            await send({
                'type': 'http.response.body',
                'body': b'{"detail": "Not Found"}'
            })
            return

        if path == '/factorial' and method == 'GET':
            query_string = parse_qs(scope['query_string'].decode())  # Парсим строку запроса
            try:
                n = int(query_string.get('n', [''])[0])  # Получаем значение n из query string
                if n < 0:
                    raise ValueError
                result = factorial(n)
                await send({
                    'type': 'http.response.start',
                    'status': HTTPStatus.OK,
                    'headers': [(b'content-type', b'application/json')]
                })
                await send({
                    'type': 'http.response.body',
                    'body': json.dumps({"result": result}).encode('utf-8')
                })
            except ValueError:
                if query_string.get('n', [''])[0] == '' or query_string.get('n', [''])[0] == 'lol':
                    await send({
                        'type': 'http.response.start',
                        'status': HTTPStatus.UNPROCESSABLE_ENTITY,
                        'headers': [(b'content-type', b'application/json')]
                    })
                else:
                    await send({
                        'type': 'http.response.start',
                        'status': HTTPStatus.BAD_REQUEST,
                        'headers': [(b'content-type', b'application/json')]
                    })
                await send({
                    'type': 'http.response.body',
                    'body': b'{}'
                })
            return

        if path.startswith('/fibonacci') and method == 'GET':
            params = path.split('/')[-1]
            try:
                n = int(params)
                if n < 0:
                    await send({
                        'type': 'http.response.start',
                        'status': HTTPStatus.BAD_REQUEST,
                        'headers': [(b'content-type', b'application/json')]
                    })
                else:
                    result = fibonacci(n)
                    await send({
                        'type': 'http.response.start',
                        'status': HTTPStatus.OK,
                        'headers': [(b'content-type', b'application/json')]
                    })
                    await send({
                        'type': 'http.response.body',
                        'body': json.dumps({"result": result}).encode('utf-8')
                    })
            except ValueError:
                await send({
                    'type': 'http.response.start',
                    'status': HTTPStatus.UNPROCESSABLE_ENTITY,
                    'headers': [(b'content-type', b'application/json')]
                })
            await send({
                'type': 'http.response.body',
                'body': b'{}'
            })
            return

        if path == '/mean' and method == 'GET':
            body = b''
            more_body = True
            while more_body:
                message = await receive()
                body += message.get('body', b'')
                more_body = message.get('more_body', False)
            try:
                if body is None or body == b'':
                    await send({
                        'type': 'http.response.start',
                        'status': HTTPStatus.UNPROCESSABLE_ENTITY,
                        'headers': [(b'content-type', b'application/json')]
                    })
                    await send({
                        'type': 'http.response.body',
                        'body': b'{}'
                    })
                    return
                numbers = json.loads(body)
                if not isinstance(numbers, list) or not numbers:
                    raise ValueError
                result = sum(numbers) / len(numbers)
                await send({
                    'type': 'http.response.start',
                    'status': HTTPStatus.OK,
                    'headers': [(b'content-type', b'application/json')]
                })
                await send({
                    'type': 'http.response.body',
                    'body': json.dumps({"result": result}).encode('utf-8')
                })
            except ValueError:
                await send({
                    'type': 'http.response.start',
                    'status': HTTPStatus.BAD_REQUEST,
                    'headers': [(b'content-type', b'application/json')]
                })
                await send({
                    'type': 'http.response.body',
                    'body': b'{}'
                })
            except json.JSONDecodeError:
                await send({
                    'type': 'http.response.start',
                    'status': HTTPStatus.BAD_REQUEST,
                    'headers': [(b'content-type', b'application/json')]
                })
                await send({
                    'type': 'http.response.body',
                    'body': b'{}'
                })
            return

        # Если маршрут не найден
        await send({
            'type': 'http.response.start',
            'status': HTTPStatus.NOT_FOUND,
            'headers': [(b'content-type', b'application/json')]
        })
        await send({
            'type': 'http.response.body',
            'body': b'{"detail": "Not Found"}'
        })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
