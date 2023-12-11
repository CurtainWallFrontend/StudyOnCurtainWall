import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header


def sendemail(code, destination):
    # 1. 连接邮箱服务器
    con = smtplib.SMTP_SSL('smtp.tongji.edu.cn', 465)

    # 2. 登录邮箱
    con.login('2154177@tongji.edu.cn', '342838221Hyh')

    # 2. 准备数据
    # 创建邮件对象
    msg = MIMEMultipart()

    # 设置邮件主题
    subject = Header('幕墙系统注册验证码', 'utf-8').encode()
    msg['Subject'] = subject

    # 设置邮件发送者
    msg['From'] = '2154177@tongji.edu.cn <granthe@tongji.edu.cn>'

    # 设置邮件接受者
    msg['To'] = destination

    # 验证码内容
    text = MIMEText('注册验证码是：'+code, 'plain', 'utf-8')
    msg.attach(text)

    # 3.发送邮件
    con.sendmail('2154177@tongji.edu.cn', destination, msg.as_string())
    con.quit()


if __name__ == "__main__":
    sendemail("4578", "1796954825@qq.com")
