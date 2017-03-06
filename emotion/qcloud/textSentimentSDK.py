import binascii
import hashlib
import hmac
import json
import random
import time
import urllib
from urllib import request

from emotion.config import cfg


class TextSentimentResult(object):

    def __init__(self):
        pass

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    @property
    def codeDesc(self):
        return self._codeDesc

    @codeDesc.setter
    def codeDesc(self, value):
        self._codeDesc = value

    @property
    def positive(self):
        return self._positive

    @positive.setter
    def positive(self, value):
        self._positive = value

    @property
    def negative(self):
        return self._negative

    @positive.setter
    def negative(self, value):
        self._negative = value

class TextSentimentSDK(object):
    def __init__(self):
        self.api_url = ""
        self.base_url = "wenzhi.api.qcloud.com"
        self.request_uri = "/v2/index.php"
        self.action = "TextSentiment"
        self.nonce = ""
        self.region = "sz"
        self.secretId = cfg.get('qcloud', 'appId')
        self.secretKey = cfg.get('qcloud', 'appSecret')
        self.timestamp = ""
        self.signature = ""
        self.method = "GET"
        self.content = ""

    def request_api(self, content):
        self.content = content
        self.init_api_url()
        encodeContent = urllib.parse.quote(content)
        url = self.api_url.replace('CONTENT', encodeContent)
        #print(url)
        response = request.urlopen(url)
        respStr = response.read().decode("UTF-8")
        return json.loads(respStr)


    def init_api_url(self):
        self.timestamp = str(time.time())[0:10]
        self.nonce = str(random.randint(10000, 99999))
        self.signature = self.sign()
        self.signature = urllib.parse.quote(self.signature)
        self.api_url = 'https://{0}{1}?Action={2}&Nonce={3}&Region={4}&SecretId={5}&Timestamp={6}&Signature={7}&content=CONTENT'.format(
            self.base_url, self.request_uri, self.action, self.nonce, self.region, self.secretId, self.timestamp,
            self.signature)

    def sign(self):
        params = {'Action':self.action,
                  'Nonce':self.nonce,
                  'Region':self.region,
                  'SecretId':self.secretId,
                  'Timestamp':self.timestamp,
                  'content':self.content
                  }
        #print(params)
        paramStr = "&".join(k.replace("_",".") + "=" + str(params[k]) for k in sorted(params.keys()))
        #print(paramStr)
        srcStr = self.method + self.base_url + self.request_uri + "?" + paramStr
        #print(srcStr)
        signStr = hmac.new(self.secretKey.encode("utf8"), srcStr.encode("utf8"), hashlib.sha1).digest()
        #print(signStr)
        finalStr =  binascii.b2a_base64(signStr)[:-1].decode()
        #print(finalStr)
        return finalStr


if __name__ == "__main__":
    sdk = TextSentimentSDK()
    sdk.request_api("不舒服")
