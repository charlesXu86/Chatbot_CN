from urllib.parse import urlparse
from baidu import bcesigner
import datetime

host = "trends.baidubce.com"
access_key = "bf7509e669df46759624770b424eba46"
secret_key = "da2c20be3a0148e98500cf54d9d6853f"
api_key = "MAgY5KObFySpBmrHddhb17pI"
api_secret = "ZXGZOkpsgyyixxZeNrWqUH81KwD4EGTX"

def gen_authorization(method, url):
    """
    normal case
    """
    utc_time = datetime.datetime.utcnow()
    utc_time_str = utc_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    url_parse_ret = urlparse.urlparse(url)
    query = url_parse_ret.query
    request = {
            'method': method,
            'uri': url_parse_ret.path,
            'params': dict([(k,v[0]) for k,v in urlparse.parse_qs(query).items()]),
            'headers': {
                'Host': url_parse_ret.hostname
                }
            }

    signer = bcesigner.BceSigner(access_key, secret_key)
    auth = signer.gen_authorization(request, timestamp=utc_time_str)
    return auth
