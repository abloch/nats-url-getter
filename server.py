import asyncio
import nats
import json
import aiohttp
from logging import getLogger, basicConfig, DEBUG
from nats.errors import ConnectionClosedError, TimeoutError, NoServersError

basicConfig(level=DEBUG)
logger = getLogger(__name__)
logger.info("starting")

async def url_getter(url: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                ret = await response.text()
                logger.info(f"url {url} returned {ret[0:15]}...")
                return ret
    except Exception as e:
        logger.exception(e)

async def message_handler(msg):
    try:
        req = json.loads(msg.data.decode())
        url = req['url']
        logger.info("getting url: " + url)
        resp = await url_getter(url)
        logger.info("got url: " + url)
        await msg.respond(resp.encode())
        logger.info("reponse sent")
    except Exception as e:
        logger.exception(e)
        await msg.respond(b'error:' + str(e).encode())

async def main():
    # It is very likely that the demo server will see traffic from clients other than yours.
    # To avoid this, start your own locally and modify the example to use it.
    nc = await nats.connect("nats://demo.nats.io:4222")

    # You can also use the following for TLS against the demo server.
    #
    # nc = await nats.connect("tls://demo.nats.io:4443")


    # Simple publisher and async subscriber via coroutine.
    sub = await nc.subscribe("url_getter", cb=message_handler)
    logger.info("Listening for messages on 'url_getter' subject")
    while True:
        try:
            await asyncio.sleep(1)
        except KeyboardInterrupt:
            break
    # try:
    #     async for msg in sub.messages:
    #         print(f"Received a message on '{msg.subject} {msg.reply}': {msg.data.decode()}")
    #         # await sub.unsubscribe()
    # except Exception as e:
    #     pass
   

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()
    