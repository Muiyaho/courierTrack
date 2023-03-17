import re
import requests
from bs4 import BeautifulSoup


patterns = {
    1: r"^\d{13}$|^\d{6}[-_]\d{7}$",
    2: r"^\d{11}$|^\d{3}[-_]\d{4}[-_]\d{4}$",
    3: r"^\d{10}$|^\d{12}$",
    4: r"^[A-Z]{2}\d{9}[A-Z]{2}$",
    5: r"^\d{10}$"
}


def get_delivery_info(invoice_number):
    for post_id, pattern in patterns.items():
        if re.match(pattern, invoice_number):
            # 여기서 DB에서 해당 post_id에 해당하는 택배사 정보를 가져옵니다.
            post_info = get_post_info_from_db(post_id)
            # 그리고 post_info를 반환합니다.
            return post_info
    return None


def get_post_info_from_db(post_id):
    # 여기에 DB에서 post_id에 해당하는 택배사 정보를 가져오는 코드를 작성해주세요.
    pass


def get_tracking_info(invoice_number):
    delivery_info = get_delivery_info(invoice_number)

    if not delivery_info:
        return None

    url = delivery_info["url"]
    soup_class = delivery_info["soup"]

    response = requests.get(url)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    tracking_table = soup.find("table", {"class": soup_class})

    if tracking_table:
        tracking_data = []
        rows = tracking_table.find_all("tr")

        for row in rows:
            cols = row.find_all("td")
            cols = [col.text.strip() for col in cols]
            tracking_data.append(cols)

        return tracking_data
    else:
        return None


# 예시 송장 번호로 테스트
invoice_number = "1234567890123"
tracking_info = get_tracking_info(invoice_number)
print(tracking_info)
