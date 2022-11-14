import asyncio
import nats
from nats.errors import ConnectionClosedError, TimeoutError, NoServersError
from bs4 import BeautifulSoup

from server import url_getter

def get_title(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('title')
    return title.text

async def main():
    nc = await nats.connect("nats://demo.nats.io:4222")

    resp = await nc.request("url_getter", b'{"method": "GET", "url": "https://google.com"}', timeout=15, old_style=True)
    title = get_title(resp.data)
    print(title)
    
    resp = await nc.request("url_getter", b'{"method": "GET", "url": "https://www.ynet.co.il/home/0,7340,L-8,00.html"}', timeout=15, old_style=True)
    title = get_title(resp.data)
    print(title)
    
    resp = await nc.request("url_getter", b'{"method": "GET", "url": "https://bbc.com/"}', timeout=15, old_style=True)
    title = get_title(resp.data)
    print(title)

async def ynet_getter():
    ret = await url_getter("https://www.ynet.co.il/home/0,7340,L-8,00.html")
    print(ret)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    # loop.run_until_complete(ynet_getter())
    print("bye...")
    