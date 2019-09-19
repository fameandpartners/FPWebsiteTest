# -*- coding: UTF-8 -*-
# 发送邮件
import datetime
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from testframework.source.configs.readini import ConfigIni
from testframework.source.construct_project.get_project_path import PathExistProject
from testframework.source.utils.logclass.logconfig import Logger


current_path = os.path.dirname(__file__)
source_log_path = os.path.join(os.path.dirname(os.path.dirname(current_path)), 'logs/')
source_log_object = Logger(log_path=source_log_path)


class Email:

    def __init__(self, project_name, message=None):

        self.project_name = project_name
        self.logger = source_log_object
        self.ini = ConfigIni(log_obj=source_log_object)

        self.server = self.ini.get_str(section='SMTP', option='server')
        self.port = 25
        self.SSL_port = 465

        self.pe = PathExistProject(project_name, source_log_object)
        self.path_data = self.pe.return_path()

        if not message:
            self._message = "Hi!\nHow are you?\nHere is the Report about Automated test\nPlease remember to check"
        else:
            self._message = message

    def get_new_file(self):
        dir_path = self.path_data["report_path"]
        in_dir_list = os.listdir(dir_path)
        if not in_dir_list:
            return None, None

        # 对文件修改时间进行升序排列
        in_dir_list.sort(key=lambda _file: os.path.getmtime(dir_path + _file))
        filetime = datetime.datetime.fromtimestamp(os.path.getmtime(dir_path + in_dir_list[-1]))

        file_path = os.path.join(dir_path, in_dir_list[-1])
        file_name = in_dir_list[-1]
        self.logger.log("  *最新修改的文件(夹)：" + in_dir_list[-1])
        self.logger.log("  *文件生成时间：" + filetime.strftime('%Y-%m-%d %H:%M:%S'))

        return file_path, file_name

    def send_email(self):
        email_switch = self.ini.get_bool(section='TIMER', option='switch')
        if not email_switch:
            self.logger.warning("Email service has been closed, will not send email")
            return

        user = self.ini.get_str(section='SMTP', option='user')
        password = self.ini.get_str(section='SMTP', option='password')
        sender = self.ini.get_str(section='SMTP', option='sender')
        receiver = self.ini.get_str(section='SMTP', option='receiver')
        if receiver:
            receiver = receiver.split(',')

        if not all([user, password, sender, receiver]):
            self.logger.info('  *Please configure the email information first')
            return

        msg = MIMEMultipart('related')  # related mixed alternative

        # 构造文字内容
        text = self._message
        text_plain = MIMEText(text, 'plain', 'utf-8')
        msg.attach(text_plain)

        msg['Subject'] = self.project_name.upper() + ' - 自动化测试报告'
        msg['from'] = sender
        msg['to'] = ','.join(receiver)

        # 附件加载
        send_file_path, file_name = self.get_new_file()
        if send_file_path and file_name:
            sendfile = open(send_file_path, 'rb').read()
            att = MIMEText(sendfile, 'html', 'utf-8')
            att['Content-Type'] = 'application/octet-stream'
            att['Content-Disposition'] = 'attachment; filename=' + file_name
            msg.attach(att)
        else:
            self.logger.info('  *can not find everything about report file, Email will not be carried in the attachment')

        smtp = None
        res = True
        try:
            # smtp = smtplib.SMTP_SSL(self.smtpserver, self.SSL_port)  # 使用SSL协议
            smtp = smtplib.SMTP()
            smtp.connect(self.server, self.port)
            smtp.login(user, password)
            smtp.sendmail(sender, msg['to'].split(','), msg.as_string())
        except Exception as e:
            self.logger.log(e)
            res = False
        finally:
            smtp.quit()

        if res:
            self.logger.log('  *Email-Report send successfully')
        else:
            self.logger.log('  *Email-Report failed to send')

    def send_email_again(self):
        pass


if __name__ == '__main__':
    project_name = 'FPWebsite'
    em = Email(project_name)
    # em.send_email()
