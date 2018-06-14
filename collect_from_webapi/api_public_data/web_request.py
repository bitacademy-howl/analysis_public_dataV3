# web request
from urllib.request import Request, urlopen
from datetime import datetime
import sys
import json

def html_request(url='',
                 encoding='utf-8',
                 success=None):
    try:
        request = Request(url)
        resp = urlopen(request)
        html = resp.read().decode()

        # Request 성공 시 URL 및 디코딩 결과를 로그로 남김
        print('%s : SUCCESS FOR REQUEST[%s]' % (datetime.now(), url))

        if callable(success) is False:
            return html
        else:
            return success(html)

    except Exception as e:
        print(e, file=sys.stderr)