import os
import json

from collect_from_webapi.api_public_data import pd_fetch_tourspot_visitor

RESULT_DIRECTORY = '__result__/crawling'

def preprocess_post(post):

        post['count_locals'] = post.pop('csNatCnt')
        post['count_foreigner'] = post.pop('csForCnt')
        post['tourist_spot'] = post.pop('resNm')
        post['date'] = post.pop('ym')
        post['city'] = post.pop('sido')
        post['restrict'] = post.pop('gungu')
        del post["rnum"]
        del post["addrCd"]

def crawlling_tourspot_visitor(district, start_year, end_year):

    results = []
    filename = '%s/%s_tourinstspot_%s_%s.json' % (RESULT_DIRECTORY, district, start_year, end_year)

    # 1년 12달, 음력/윤년 고려 안함
    for searchingyear in range(start_year, end_year+1):
        for searchingmonth in range(1, 13):
            for posts in pd_fetch_tourspot_visitor(district, year=searchingyear, month=searchingmonth):
                for post in posts:
                    preprocess_post(post)
                results.extend(posts)

                # save results to file (저장/적재)
                with open(filename, 'w', encoding='utf-8') as outfile:
                    json_String = json.dumps(results, indent=4, sort_keys=True, ensure_ascii=False)
                    outfile.write(json_String)

if os.path.exists(RESULT_DIRECTORY) is False:
    os.makedirs(RESULT_DIRECTORY)