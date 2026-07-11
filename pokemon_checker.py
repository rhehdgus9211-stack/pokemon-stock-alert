import requests
import json
import os


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

    try:
        response = requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=message.encode("utf-8"),
            headers={
                "Title": "Pokemon Card Alert",
                "Priority": "high",
                "Tags": "tada"
            },
            timeout=10
        )

        print(
            "ntfy 전송:",
            response.status_code
        )

    except Exception as e:
        print(
            "ntfy 오류:",
            e
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



def check_product(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=15
    )

    text = response.text


    # 구매 가능 상태
    if "구매하기" in text:
        return "available"


    # 구매불가 상태
    return "soldout"



old_status = load_status()

new_status = {}



for name, url in PRODUCTS.items():

    try:

        current = check_product(url)

        new_status[name] = current


        before = old_status.get(
            name,
            "soldout"
        )


        print(
            name,
            current
        )


        # 구매불가 -> 구매가능 변경 감지

        if before == "soldout" and current == "available":

            send_ntfy(
                f"🔥 포켓몬 카드 재입고 감지!\n\n"
                f"{name}\n\n"
                f"{url}"
            )


    except Exception as e:

        print(
            name,
            "오류:",
            e
        )



save_status(new_status)
