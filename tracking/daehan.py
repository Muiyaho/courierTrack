import re
import requests
from com.reg import patterns
from bs4 import BeautifulSoup
from db.db import get_post_info_from_db  # 함수를 여기서 임포트합니다.


def get_delivery_info(invoice_number):
    for post_id, pattern in patterns.items():
        if re.match(pattern, invoice_number):
            #운송장 패턴에 맞는 택배사 id로 조회
            post_info = get_post_info_from_db(post_id)
            return post_info
    return None

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
