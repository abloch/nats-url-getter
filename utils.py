from os import environ
import aiohttp
import json
import nats
from logging import getLogger, basicConfig, DEBUG
from bs4 import BeautifulSoup

basicConfig(level=DEBUG)
logger = getLogger(__name__)
logger.info("starting")


async def get_nats_connection():
    NATS_HOST = environ.get("NATS_SERVER", "nats://demo.nats.io:4222")
    return await nats.connect(NATS_HOST)


async def http_get(url: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                ret = await response.text()
                logger.info(f"url {url} returned {ret[0:15]}...")
                return ret
    except Exception as e:
        logger.exception(e)


def parse_title(html):
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find("title")
    return title.text


async def get_title_from_nats(nc, url):
    payload = json.dumps({"method": "GET", "url": url})
    resp = await nc.request("url_getter", payload.encode(), timeout=15)
    return parse_title(resp.data)
