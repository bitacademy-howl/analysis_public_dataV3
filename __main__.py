import collect_from_webapi
from collect_from_webapi import crawlling_tourspot_visitor, crawlling_foreign_visitor, pd_fetch_tourspot_visitor, pd_fetch_foreign_visitor
from collect_from_webapi import pd_set_parameters
import collect_from_webapi.api_public_data as pdapi

if __name__ == '__main__':
    items = [
        {'district': '서울특별시', 'start_year': 2017, 'end_year': 2017}
    ]

    # 데이터 수집 (collect)
    for item in items:
        crawlling_tourspot_visitor(**item)



    for country in [('중국', 112), ('일본', 130), ('미국', 275)]:
    # for country in [('중국', 112)]:
        crawlling_foreign_visitor(country, 2017, 2017)

    # collect
