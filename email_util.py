import re
import os
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import parseaddr, formataddr

"""
目前支持 163、qq 邮箱, 126邮箱未测试
使用前请先设置，发送邮箱及密码
"""

defaults = {
    'sender': '',
    'password': '',
    'nickname': ''
}


class SendEmailUtil:

    __smtp_server_map = {
        '126': 'smtp.126.com',
        '163': 'smtp.163.com',
        'qq': 'smtp.qq.com'
    }

    __re_email = re.compile(r'^\w+@(\w+)\.com$')

    @classmethod
    def __format_addr(cls, s: str):
        """
        s example: "Hugh <example@163.com>"
        """
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    @classmethod
    def __get_smtp_server(cls, sender: str):
        re_res = cls.__re_email.match(sender)
        if re_res:
            smtp_server = cls.__smtp_server_map.get(re_res.group(1))
            if smtp_server:
                return smtp_server
            raise ValueError(f'暂不支持 {re_res.group(1)} 邮箱!!!')
        raise ValueError(f'{sender} 不符合Email格式!!!')
    
    @classmethod
    def __login(cls, smtp, sender, password):
        smtp.login(sender, password)

    @classmethod
    def _email_att(cls, enclosure):
        base_types = ['.png', 'gif', '.jpg', '.jpeg']
        file_type = os.path.splitext(enclosure)[-1]
        filename = os.path.basename(enclosure)
        if file_type in base_types:
            with open(enclosure, 'rb') as fp:
                mime = MIMEBase('image', os.path.splitext(enclosure)[-1][1:], filename=filename)
                mime.add_header('Content-Disposition', 'attachment', filename=filename)
                mime.add_header('Content-ID', '<0>')
                mime.add_header('X-Attachment-Id', '0')
                mime.set_payload(fp.read())
                encoders.encode_base64(mime)
                return mime
        else:
            with open(enclosure, 'r', encoding='utf-8') as f:
                mime = MIMEText(f.read(), 'base64', 'utf-8')
                mime['Content-Type'] = "application/octet-stream"
                mime['Content-Disposition'] = f'attachment; filename={filename}'
                return mime

    @classmethod
    def __email_info(cls, sender, receiver, subject, body, body_type='plain', enclosures=None, nickname=''):
        msg = MIMEMultipart()
        msg.attach(MIMEText(body, body_type, 'utf-8'))
        msg['from'] = cls.__format_addr(f'{nickname} <{sender}>')
        msg['to'] = receiver
        msg['subject'] = subject
        if enclosures:
            for enclosure in enclosures:
                msg.attach(cls._email_att(enclosure))
        return msg

    @classmethod
    def run(cls, receiver, subject, body, enclosures=None,
            sender=defaults['sender'], password=defaults['password'], nickname=defaults.get('nickname', '')):
        msg = cls.__email_info(sender, receiver, subject, body, enclosures=enclosures, nickname=nickname)
        smtp = smtplib.SMTP(cls.__get_smtp_server(sender))
        try:
            cls.__login(smtp, sender, password)
            smtp.sendmail(sender, receiver, msg.as_string())
        except smtplib.SMTPAuthenticationError:
            print(f'认证失败!!! --> "{sender}" "{password}"')
        finally:
            smtp.quit()


if __name__ == '__main__':
    SendEmailUtil.run('example@gmail.com', '测试主题', '测试内容')
