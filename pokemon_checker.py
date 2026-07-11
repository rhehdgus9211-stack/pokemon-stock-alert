import json
import os
import asyncio
from playwright.async_api import async_playwright
import requests


NTFY_TOPIC = "pokemoncard-7a92kf381"

STATUS_FILE = "status.json"


PRODUCTS = {
    "카드박스1": "https://www.pokemonstore.co.kr/pages/product/product-detail.html?productNo=114169373",
    "카드박스2": "https://www.pokemonstore.co.kr/pages/product/product-detail.html?productNo=124381031",
    "카드박스3": "https://www.pokemonstore.co.kr/pages/product/product-detail.html?productNo=116178963",
    "카드박스4": "https://www.pokemonstore.co.kr/pages/product/product-detail.html?productNo=114165789",
    "카드박스5": "https://www.pokemonstore.co.kr/pages/product/product-detail.html?productNo=114167543",
}



def send_ntfy(message):

    requests.post(
        f"https://ntfy.sh/{NTFY_TOPIC}",
        data=message.encode("utf-8"),
        headers={
            "Title": "Pokemon Card Alert",
            "Priority": "high",
            "Tags": "tada"
        }
    )



def load_status():

    if os.path.exists(STATUS_FILE):

        with open(
            STATUS_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    return {}



def save_status(status):

    with open(
        STATUS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            status,
            f,
            ensure_ascii=False,
            indent=2
        )



async def check_product(page, url):

    await page.goto(
        url,
        wait_until="networkidle",
        timeout=60000
    )

    await page.wait_for_timeout(3000)


    text = await page.locator(
        "body"
    ).inner_text()


    if "구매불가" in text:

        return "soldout"


    return "available"



async def main():

    old_status = load_status()

    new_status = {}


    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True
        )


        page = await browser.new_page()


        for name, url in PRODUCTS.items():

            try:

                current = await check_product(
                    page,
                    url
                )


                new_status[name] = current


                before = old_status.get(
                    name,
                    "soldout"
                )


                print(
                    name,
                    current
                )


                if before == "soldout" and current == "available":

                    send_ntfy(
                        f"🔥 포켓몬 카드 재입고 감지!\n\n{name}\n\n{url}"
                    )


            except Exception as e:

                print(
                    name,
                    e
                )


        await browser.close()


    save_status(new_status)



asyncio.run(main())
