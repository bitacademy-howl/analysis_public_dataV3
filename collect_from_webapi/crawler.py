import os
import json

from .api_public_data import pd_fetch_tourspot_visitor, pd_fetch_foreign_visitor

RESULT_DIRECTORY = '__result__/crawling'

def preprocess_tourspot_visitor(post):

        post['count_locals'] = post.pop('csNatCnt')
        post['count_foreigner'] = post.pop('csForCnt')
        post['tourist_spot'] = post.pop('resNm')
        post['date'] = post.pop('ym')
        post['city'] = post.pop('sido')
        post['restrict'] = post.pop('gungu')
        del post["rnum"]
        del post["addrCd"]

def crawlling_tourspot_visitor(district, start_year, end_year):

    filename = '%s/%s_tourinstspot_%s_%s.json' % (RESULT_DIRECTORY, district, start_year, end_year)

    # 문제 :
    # result를 크롤링 함수의 지역변수로 지정하게 되면(Version 1의 경우)
    # 크롤링 중 메모리에 모든 자료를 다 올리게 되고, 방대한 데이터를 크롤링 하는 경우 버퍼(or스택) 오버플로우 발생 가능
    # 일련의 단위별로 저장하는 방법이 필요
    # step 1:
    # 아래서는 파일을 함수내에서 열어서 쓰지만
    # 프로그램 리셋 시 이전에 기록한 데이터가 지워지는 단점
    # DB 엑세싱이라면 값을 테이블에 추가하고 데이터가 유지되지만
    # 아래와 같이 파일 입출력의 경우
    # step 2:
    # 기존에 있는 파일에 이어서 데이터를 기록하여야 함
    # step 3: DB 엑세싱에 관한 방법도 찾아볼 것!
    with open(filename, 'w', encoding='utf-8') as outfile:
        # 1년 12달, 음력/윤년 고려 안함
        for searchingyear in range(start_year, end_year+1):
            for searchingmonth in range(1, 13):
                for posts in pd_fetch_tourspot_visitor(district, year=searchingyear, month=searchingmonth):
                    for post in posts:
                        preprocess_tourspot_visitor(post)
                    # save results to file (저장/적재)
                    json_String = json.dumps(posts, indent=4, sort_keys=True, ensure_ascii=False)
                    outfile.write(json_String)

def preprocess_foreign_visitor(data):

    del data['ed']
    del data['edCd']
    del data['rnum']

    # 나라 코드
    data['country_code'] = data.pop('natKorNm').replace(' ', '')
    data['visit_count'] = data.pop('num')
    if 'ym' not in data:
        data['date'] = 0
    else:
        data['date'] = data.pop('ym')


def crawlling_foreign_visitor(country, start_year, end_year):
    results = []
    for year in range(start_year, end_year+1):
        for month in range(1, 13):
            data = pd_fetch_foreign_visitor(country[1], year=year, month=month)
            if data is None:
                continue
            else:
                preprocess_foreign_visitor(data)
                results.append(data)

    print(results)
    filename = '%s/%s(%s)_foreign_visitor_%s_%s.json' % (RESULT_DIRECTORY, country[0], country[1], start_year, end_year)

    # 아래와 같이 파일 오픈 시 outfile을 꼭 close 해야 한다.
    # outfile = open(filename, 'w', encoding='utf-8')
    # but with open 으로 열 경우는 블럭이 끝날때 자동으로 파일 클로징 해준다.

    with open(filename, 'w', encoding='utf-8') as outfile:
        json_String = json.dumps(results, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(json_String)

if os.path.exists(RESULT_DIRECTORY) is False:
    os.makedirs(RESULT_DIRECTORY)