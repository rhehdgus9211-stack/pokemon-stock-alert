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

        print("ntfy 전송 결과:", response.status_code)

    except Exception as e:
        print("ntfy 오류:", e)


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

    # 현재 품절 상태
    if "구매불가" in text:
        return False

    # 구매 가능 상태
    return True



# =========================
# 테스트 알림
# (테스트 후 삭제 예정)
# =========================

send_ntfy(
    "🔥 포켓몬스토어 알림 테스트 성공!"
)


# =========================
# 상품 확인
# =========================

for name, url in PRODUCTS.items():

    try:

        available = check_product(
            name,
            url
        )

        print(
            name,
            "구매가능" if available else "구매불가"
        )


        if available:

            send_ntfy(
                f"🔥 구매 가능 상태 감지!\n\n"
                f"{name}\n\n"
                f"{url}"
            )


    except Exception as e:

        print(
            name,
            "확인 오류:",
            e
        )
