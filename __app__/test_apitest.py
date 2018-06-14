import collect_from_webapi.api_public_data as pdapi
from collect_from_webapi import pd_fetch_tourspot_visitor

# url = pdapi.pd_gen_url("http://openapi.tour.go.kr/openapi/serviceTourismResourceStatsService/getPchrgTrrsrtVisitorList",
#                        YM='{0:04d}{1:02d}'.format(2017, 1),
#                        SIDO='서울특별시',
#                        GUNGU='',
#                        RES_NM='',
#                        numOfRows=10,
#                        _type='json',
#                        pageNo=1)


# test for pd_fetch_tourspot_visitor
for items in pd_fetch_tourspot_visitor(district='서울특별시', year=2017, month=7):
    print(items)


# test for pd_fetch_tourspot_visitor()

item = pdapi.pd_fetch_foreign_visitor(112, 2012, 7)
print(item)