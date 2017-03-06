import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

from emotion.config import cfg


class MailsUtil(object):
    def __init__(self, smtp_server=cfg.get('mail', 'smtp_server'),
                 from_addr=cfg.get('mail', 'from_addr'), password=cfg.get('mail', 'password'),
                 to_addr=cfg.get('mail', 'to_addr')):
        self.smtp_server = smtp_server
        self.from_addr = from_addr
        self.password = password
        self.to_addr = to_addr
        self.server = smtplib.SMTP(self.smtp_server, 25)
        self.server.set_debuglevel(1)

    def send_mail(self, content):
        msg = MIMEText(content, 'html', 'utf-8')
        msg['From'] = self._format_addr('观测者 <%s>' % self.from_addr)
        msg['To'] = self._format_addr('一个神奇的地方 <%s>' % self.to_addr)
        msg['Subject'] = Header('你的观测者为你带来了一条神奇的消息……', 'utf-8').encode()
        self.server.login(self.from_addr, self.password)
        self.server.sendmail(self.from_addr, [self.to_addr], msg.as_string())
        self.server.quit()

    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))


