import asyncio
from utils import get_title_from_nats, get_nats_connection

URLS = [
    "https://google.com",
    "https://www.ynet.co.il/home/0,7340,L-8,00.html",
    "https://bbc.com/",
]


async def main():
    nc = await get_nats_connection()

    for url in URLS:
        title = await get_title_from_nats(nc, url)
        print(f"{url} title is {title}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print("bye...")
