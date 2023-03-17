import requests
from bs4 import BeautifulSoup

def get_daehan_tracking_details(tracking_number):
    url = f"https://www.doortodoor.co.kr/parcel/doortodoor.do?fsp_action=PARC_ACT_002&fsp_cmd=retrieveInvNoACT&invc_no={tracking_number}"
    response = requests.get(url)

    if response.status_code != 200:
        return False, None

    soup = BeautifulSoup(response.text, "html.parser")
    tracking_details = []

    #택배별 class name 알아야함!
    tracking_table = soup.find("table", {"class": "ptb10 mb15"})

    if tracking_table is None:
        return False, None

    for row in tracking_table.find_all("tr")[1:]:
        cells = row.find_all("td")
        tracking_status = cells[2].text.strip()
        tracking_time = cells[0].text.strip() + " " + cells[1].text.strip()
        tracking_location = cells[3].text.strip()

        tracking_details.append({
            "time": tracking_time,
            "location": tracking_location,
            "status": tracking_status
        })

    return True, tracking_details

#테스트 전용 로직
if __name__ == "__main__":
    tracking_number = "0000000000"  # 실제 송장번호를 입력하세요.
    is_valid, tracking_details = get_daehan_tracking_details(tracking_number)

    if is_valid:
        print("Tracking Details:")
        for detail in tracking_details:
            print(detail)
    else:
        print("Invalid tracking number or no tracking information found.")