# @Time    : 2020/12/28 11:30
# @Author  : Hugh
# @Email   : 609799548@qq.com

import time
import hmac
import hashlib
import base64
import urllib.parse

import requests

__all__ = ['DingDing', ]


class DingDing:
    url = 'https://oapi.dingtalk.com/robot/send'

    def generate_timestamp_sign(self):
        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode('utf8')
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return timestamp, sign

    def __init__(self, secret, access_token):
        """
        :param secret: 机器人管理，安全设置里的加签
        :param access_token: 机器人管理，Webhook中的 access_token
        """
        self.secret = secret
        self.access_token = access_token

    def send_content(self, text, *at, at_all=False):
        """
        :param text: 发送的内容
        :param at: 需要 @ 的手机号
        :param at_all: 是否需要 @ 所有人
        """
        timestamp, sign = self.generate_timestamp_sign()
        params = {'access_token': self.access_token, 'timestamp': timestamp, 'sign': sign}
        data = {"msgtype": "text", "text": {"content": text}, "at": {"atMobiles": at, "isAtAll": at_all}}
        requests.post(DingDing.url, params=params, json=data)


if __name__ == '__main__':
    # example
    c = DingDing('xxx', 'xxx')
    c.send_content('大家好，我是共产主义的接班人 --- 陈冠希')
