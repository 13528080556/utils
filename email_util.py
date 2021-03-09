# @Date  : 2021/3/9
# @Author: Hugh
# @Email : 609799548@qq.com

"""
使用例子
e = Email(邮箱号, 授权码)
e.send([收件人邮箱], subtype='邮件正文类型', subject='邮件主题', content='邮件内容', *files)
"""

import re
import os
import smtplib
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart


class Email:

    __re = re.compile(r'^\w+@(\w+)\.com$')

    def __init__(self, from_address, password):
        name, address = parseaddr(from_address)
        self.__nickname = name
        self.__address = address
        self.__password = password
        self.server = self.__get_smtp_server()

    def __get_smtp_server(self):
        res = self.__re.match(self.__address)
        if not res:
            raise ValueError('{} 不符合 Email 格式'.format(self.__address))
        target = 'smtp.' + res.group(1) + '.com'
        print('连接 {} ...'.format(target))
        server = smtplib.SMTP(target, 25)
        # server.set_debuglevel(1)
        return server

    def __login(self):
        self.server.login(self.__address, self.__password)

    @staticmethod
    def __format_addr(string):
        name, address = parseaddr(string)
        return formataddr((Header(name, 'utf-8').encode(), address))

    def __format_from_address(self,):
        """
        from address(发件人邮箱地址):
            - format_from_address('example@qq.com')
            - format_from_address('<example@qq.com>')
            - format_from_address('Hugh <example@qq.com>')
        """
        return self.__format_addr('%s <%s>' % (self.__nickname, self.__address))

    def __format_to_address(self, addresses):
        """
        to addresses(收件人邮箱地址):
            - format_to_address(['example@qq.com', '<example@qq.com>', 'Hugh <example@qq.com>'])
        """
        return ','.join([self.__format_addr(address) for address in addresses])

    @staticmethod
    def format_subject(subject):
        """
        subject(邮件主题):
            - format_subject('邮件主题')
        """
        return Header(subject, 'utf-8').encode()

    @staticmethod
    def __attach_file(message, file_path, file_type):
        """添加附件"""
        suffix = os.path.splitext(file_path)[-1][1:]
        filename = os.path.split(file_path)[-1]
        with open(file_path, 'rb') as f:
            mime = MIMEBase(file_type, suffix, filename=filename)
            mime.add_header('Content-Disposition', 'attachment', filename=filename)
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            message.attach(mime)

    def __format_message_from_to_subject(self, message, to_addresses, subject):
        """格式化 message 的 from address、to addresses、subject"""
        message['From'] = self.__format_from_address()
        message['To'] = self.__format_to_address(to_addresses)
        message['Subject'] = self.format_subject(subject)

    def __generate_message_plain_html(self, to_addresses, subtype, subject, content):
        """生成纯文本或者纯 html 邮件"""
        message = MIMEText(content, subtype, 'utf-8')
        self.__format_message_from_to_subject(message, to_addresses, subject)
        return message

    def __generate_message_multipart(self, to_addresses, subtype, subject, content, *files):
        """生成可以携带文件的邮件"""
        message = MIMEMultipart()
        self.__format_message_from_to_subject(message, to_addresses, subject)
        message.attach(MIMEText(content, subtype, 'utf-8'))  # 邮件正文
        for _path, _type in files:
            self.__attach_file(message, _path, _type)
        return message

    def send(self, to_addresses, subtype='plain', subject='邮件主题', content='邮件内容', *files):
        """发送邮件"""
        if isinstance(to_addresses, str):
            to_addresses = [to_addresses]
        try:
            self.__login()
            message = self.__generate_message_multipart(to_addresses, subtype, subject, content, *files)
            self.server.sendmail(self.__address, to_addresses, message.as_string())
        finally:
            self.server.quit()


if __name__ == '__main__':
    e = Email('example@example.com', 'secret')
