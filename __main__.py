from collect_from_webapi import crawlling_tourspot_visitor, pd_fetch_tourspot_visitor
from collect_from_webapi import pd_set_parameters

if __name__ == '__main__':

    items = [
        {'district': '서울특별시', 'start_year': 2017, 'end_year': 2017}
    ]

    # 데이터 수집 (collect)
    for item in items:
        crawlling_tourspot_visitor(**item)

