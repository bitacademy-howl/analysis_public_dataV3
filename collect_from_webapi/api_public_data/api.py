#  FB API Wrapper Function

# 파이썬은 상수 변수의 개념이 있지 않지만 대문자로 상수임을 명시하는 관례를 따른다.
from urllib.parse import urlencode
from .web_request import html_request
import json
from datetime import datetime

BASE_URL_FB_API = 'http://openapi.tour.go.kr/openapi/service'
END_POINT = 'TourismResourceStatsService/getPchrgTrrsrtVisitorList'
SERVICEKEY = 'gHAYES1qnZH9UkUx5HTavujpoRJZdX7lUTDJCJCvuQSulnDbVFcpELiXgLDqacbIgm5fiktJKK8Y9ghVqkfcgg%3D%3D'

def pd_gen_url(
        base=BASE_URL_FB_API,
        node=END_POINT, **params
):
    url = "%s/%s?&%s" % (base, node, urlencode(params, encoding='UTF-8', safe='%'))
    # print(url)
    return url

# 실제 GET 방식에 사용될 URL 생성 - with ACCESS_TOKEN
def pd_set_token(**params):
    url = pd_gen_url(node=END_POINT, serviceKey=SERVICEKEY, **params)
    # print(params)
    return url

def pd_set_parameters(year = 0, month=0, sido='', gungu='', res_nm=''):
    url = pd_set_token(YM='{0:04d}{1:02d}'.format(year, month),
                       SIDO=sido,
                       GUNGU=gungu,
                       RES_NM=res_nm,
                       # numOfRows=10, #디폴트 값이 10
                       pageNo=1,
                       _type='json')
    return url

def pd_fetch_tourspot_visitor(district='', tourspot='', year=0, month=0):
    # 자세한 URL 생성 fields 는 data.go.kr API 문서 참조
    url = pd_set_parameters(sido=district, res_nm=tourspot, year=year, month=month)
    paging = 1

    while True:

        json_result = html_request(url=url, success=lambda x: json.loads(x))

        body = json_result.get("response").get('body')
        items = body.get("items")
        if len(items) is 0:
            break
        posts = items.get("item")
        # print(posts)

        # URL 교체 - 다음페이지로
        url = url.replace("pageNo={0}".format(paging), "pageNo={0}".format(paging + 1))
        paging += 1
        yield posts

def pd_fetch_foreign_visitor(countrycode, year, month):
    node = 'EdrcntTourismStatsService/getEdrcntTourismStatsList'
    url = pd_gen_url(node=node,
                     YM='{0:04d}{1:02d}'.format(year, month),
                     NAT_CD=countrycode,
                     ED_CD='E',
                     _type='json',
                     serviceKey=SERVICEKEY)

    json_result = html_request(url=url, success=lambda x:json.loads(x))
    # print(json_result)
    json_response = json_result.get("response")
    json_header = json_response.get("header")
    result_message = json_header.get('resultMsg')
    if 'OK' != result_message:
        print("%s Error[%s] for request %s" % datetime.now(), result_message)
        return None
    else:
        json_body = json_response.get("body")
        json_items = json_body.get("items")
        return json_items.get("item") if isinstance(json_items, dict) else None