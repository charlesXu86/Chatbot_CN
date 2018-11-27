"""
This module provides authorization generator described in http://gollum.baidu.com/IamApiServiceGuide
Author: dengxiaochao@baidu.com
"""
import datetime
import hashlib
import hmac
import urllib
import json
import uuid
import logging

class BceSigner(object):
    """
    Utility class which adds allows a request to be signed with an BCE signature
    """

    def __init__(self, access_key, secret_key, logger=None):
        self.access_key = access_key.encode()
        self.secret_key = secret_key.encode()
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger()
            self.logger.addHandler(logging.StreamHandler())
            self.logger.setLevel(logging.DEBUG)

    def gen_authorization(self, request, timestamp=None, expire_period=1800):
        """
        generate authorization string
        if not specify timestamp, then use current time;
        """
        signedheaders = []
        if "headers" in request:
            signedheaders = list(key.lower() for key in request["headers"].keys() if key != '')
            signedheaders.sort()
        authorization = build_authorization(self.access_key,
                signedheaders, expire_period, timestamp)
        signingkey = self._calc_signingkey(authorization)
        self.logger.debug("SigningKey: %(signingkey)s", {"signingkey": signingkey})
        signature = self._calc_signature(signingkey, request, signedheaders)
        authorization["signature"] = signature
        return serialize_authorization(authorization)

    def authenticate(self, authorization, request):
        """
        autenticate a request.
        calcaulate request signature, and compare with authorization
        """
        signingkey = self._calc_signingkey(authorization)
        self.logger.debug("SigningKey: %(signingkey)s", {"signingkey": signingkey})
        signature = self._calc_signature(signingkey, request, authorization["signedheaders"])
        return signature == authorization["signature"]

    @staticmethod
    def get_utf8_value(value):
        """
        Get the UTF8-encoded version of a value.
        """
        if not isinstance(value, str):
            value = str(value)
        if isinstance(value):
            return value.encode('utf-8')
        else:
            return value

    @staticmethod
    def canonical_qs(params):
        """
        Construct a sorted, correctly encoded query string
        """
        keys = list(params)
        pairs = []
        for key in keys:
            if key == "authorization":
                continue
            vals = params[key]
            nkey = urllib.quote(key, safe='')
            if isinstance(vals, list):
                if len(vals) != 0:
                    for item in vals:
                        val = BceSigner.normalized(item)
                        pairs.append(nkey + '=' + val)
                else:
                    pairs.append(nkey + '=')
            else:
                val = BceSigner.normalized(vals)
                pairs.append(nkey + '=' + val)
        pairs.sort()
        qs = '&'.join(pairs)
        return qs

    @staticmethod
    def canonical_header_str(headers, signedheaders=None):
        """
        calculate canonicalized header string
        """
        headers_norm_lower = dict()
        for (k, v) in headers.iteritems():
            if v is None:
                err_msg = "%s has a null value" % (k)
                raise ValidationError(err_msg)
            key_norm_lower = BceSigner.normalized(k.lower())
            value_norm_lower = BceSigner.normalized(v.strip())
            headers_norm_lower[key_norm_lower] = value_norm_lower
        keys = list(headers_norm_lower)
        keys.sort()
        if "host" not in keys:
            raise MissingHeaderError()
        header_list = []
        default_signed = ("host", "content-length", "content-type", "content-md5")
        if signedheaders:
            for key in signedheaders:
                key = BceSigner.normalized(key.lower())
                if key not in keys:
                    raise MissingHeaderError()
                if headers_norm_lower[key]:
                    header_list.append(key + ":" + headers_norm_lower[key])
        else:
            for key in keys:
                if key.startswith("x-bce-") or key in default_signed:
                    header_list.append(key + ":" + headers_norm_lower[key])
        return '\n'.join(header_list)

    @staticmethod
    def normalized_uri(uri):
        """
        Construct a normalized(except slash '/') uri
        eg. /json-api/v1/example/ ==> /json-api/v1/example/
        """
        return urllib.quote(BceSigner.get_utf8_value(uri), safe='-_.~/')

    @staticmethod
    def normalized(msg):
        """
        Construct a normalized uri
        """
        return urllib.quote(BceSigner.get_utf8_value(msg), safe='-_.~')

    def _calc_signingkey(self, auth):
        """ Get a a signing key """
        string_to_sign = "/".join((auth['version'], auth['access'],
            auth['timestamp'], auth['period']))
        signingkey = hmac.new(self.secret_key, self.get_utf8_value(string_to_sign),
                             hashlib.sha256).hexdigest()
        return signingkey

    def _calc_signature(self, key, request, signedheaders):
        """Generate BCE signature string."""
        if not request.get('method'):
            raise EmptyMethodError()
        if not request.get('uri'):
            raise EmptyURIError()
        # Create canonical request
        params = {}
        headers = {}
        if "params" in request: params = request['params']
        if "headers" in request: headers = request['headers']
        cr = "\n".join((request['method'].upper(),
                        self.normalized_uri(request['uri']),
                        self.canonical_qs(params),
                        BceSigner.canonical_header_str(headers, signedheaders)))
        self.logger.debug("CanonicalRequest: %(request)s", {"request": cr})
        signature = hmac.new(key, cr, hashlib.sha256).hexdigest()
        self.logger.debug("Signature: %(signature)s", {"signature": signature})
        return signature


def load_authorization(auth_str):
    """ return a dict contains version, access, timestamp, period
        param: auth: Authorization string
    """
    auth_split = auth_str.split('/')
    if len(auth_split) != 6:
        raise InvalidAuthorizationError()
    version = auth_split[0]
    access = auth_split[1]
    timestamp = auth_split[2]
    period = auth_split[3]
    signedheaders = []
    if auth_split[4]:
        signedheaders = auth_split[4].split(';')
    signature = auth_split[5]

    if version != "bce-auth-v1":
        raise InvalidAuthorizationError()
    if not is_utc_timestamp(timestamp):
        raise InvalidAuthorizationError()
    if not is_integer(period):
        raise InvalidAuthorizationError()
    
    request_datetime = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    now_datetime = datetime.datetime.utcnow()
    if int(period) != -1 and \
            now_datetime - request_datetime > datetime.timedelta(seconds=int(period)):
        raise RequestExpiredError()

    auth = {}
    auth['version'] = version
    auth['access'] = access
    auth['timestamp'] = timestamp
    auth['period'] = period
    auth['signedheaders'] = signedheaders
    auth['signature'] = signature
    return auth


def serialize_authorization(auth):
    """
    serialize Authorization object to authorization string
    """
    val = "/".join((auth['version'], auth['access'], auth['timestamp'], auth['period'],
            ";".join(auth['signedheaders']), auth['signature']))
    return BceSigner.get_utf8_value(val)


def build_authorization(accesskey, signedheaders, period=1800, timestamp=None):
    """
    build Authorization object
    """
    auth = {}
    auth['version'] = "bce-auth-v1"
    auth['access'] = accesskey
    if not timestamp:
        auth['timestamp'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    else:
        auth['timestamp'] = timestamp
    auth['period'] = str(period)
    auth['signedheaders'] = signedheaders
    return auth


def is_utc_timestamp(timestamp):
    """
    check if timestamp is with utc format
    """
    try:
        datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
        return True
    except ValueError:
        return False


def is_integer(value):
    """
    check if value is an interger
    """
    try:
        v = int(value)
        return True
    except ValueError:
        return False


class ValidationError(Exception):
    """
    base Error class
    """
    def __init__(self, message):
        self.message = message
        super(ValidationError, self).__init__(message)


class MissingHeaderError(ValidationError):
    """
    missing required headers
    """
    def __init__(self):
        self.message = "missing signing headers"
        super(MissingHeaderError, self).__init__(self.message)


class EmptyMethodError(ValidationError):
    """
    method is empty
    """
    def __init__(self):
        self.message = "method is empty"
        super(EmptyMethodError, self).__init__(self.message)


class EmptyURIError(ValidationError):
    """
    uri is empty
    """
    def __init__(self):
        self.message = "uri is empty"
        super(EmptyURIError, self).__init__(self.message)


class InvalidAuthorizationError(ValidationError):
    """
    invalid authorization string
    """
    def __init__(self):
        self.message = "invalid authorization string"
        super(InvalidAuthorizationError, self).__init__(self.message)
        

class RequestExpiredError(ValidationError):
    """
    request has expired
    """
    def __init__(self):
        self.message = "Request Expired"
        super(RequestExpiredError, self).__init__(self.message)
    

if __name__ == '__main__':
    accesskey = uuid.uuid4().hex  # use your real accesskey id
    secretkey = uuid.uuid4().hex  # use your real corresponding sceretkey id
    accesskey = "2ae1b4fa12a54bdab6d03d4fd85980fd"
    secretkey = "0ccb6a9a47f74f8ba98bbe965bc08297"
    request = {
            'method': 'GET',
            'uri': '/client/request/uri',
            'params': {
                'param1': '',
                'param2': 'test',
                'multi_value': [
                    'value1',
                    'value2',
                    'value3'
                ]
                },
            'headers': {
                'Host': "tc-fiji.epc:8581"
                }
            }

    signer = BceSigner(accesskey, secretkey)
    auth = signer.gen_authorization(request)
    print("request:", json.dumps(request))
    print("authorization:", auth)
