from urllib.parse import urlparse
from baidu import bcesigner
import datetime

host = "trends.baidubce.com"
access_key = "please put your access key here"
secret_key = "please put your secret access key here"
api_key = 'To get API key, please send an apply email to cloud-martech-support@baidu.com'
api_secret = 'To get API secret, please send an apply email to cloud-martech-support@baidu.com'

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
