import asyncio
import json
from utils import http_get, get_nats_connection
from logging import getLogger, basicConfig, DEBUG

basicConfig(level=DEBUG)
logger = getLogger(__name__)


async def message_handler(msg):
    try:
        req = json.loads(msg.data.decode())
        url = req["url"]
        logger.info("getting url: " + url)
        resp = await http_get(url)
        logger.info("got url: " + url)
        await msg.respond(resp.encode())
        logger.info("reponse sent")
    except Exception as e:
        logger.exception(e)
        await msg.respond(b"error:" + str(e).encode())


async def main():
    nc = await get_nats_connection()

    await nc.subscribe("url_getter", cb=message_handler)
    logger.info("Listening for messages on 'url_getter' subject")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()
