import requests

NTFY_TOPIC = "pokemoncard-7a92kf381"

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
            "Title": "포켓몬스토어 재입고 알림",
            "Priority": "high",
            "Tags": "tada"
        }
    )


def check_product(name, url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=15
    )

    text = response.text

    if "구매불가" in text:
        return False

    return True


for name, url in PRODUCTS.items():

    try:

        available = check_product(
            name,
            url
        )

        if available:
            send_ntfy(
                f"🔥 구매 가능 상태 감지!\n\n{name}\n{url}"
            )

    except Exception as e:
        print(
            name,
            e
        )
