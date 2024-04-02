import smtplib
import time

SMTP_SERVER = "https://wx.mail.qq.com"
SMTP_PORT = 587
SMTP_ACCT = "1365840492@qq.com"
SMTP_PASSWORD = ""
TGT_ACCTS = ["tim@elsewhere.com"]

def plain_email(subject:bytes,contents:bytes)->None:
    ''''''
    message = f"Subject: {subject.decode()}\nFrom: {SMTP_ACCT}\n"
    message += f"To: {TGT_ACCTS}\n\n{contents.decode()}"
    server = smtplib.SMTP(SMTP_SERVER,SMTP_PORT)
    server.starttls
    server.login(SMTP_ACCT,SMTP_PASSWORD)
    server.set_debuglevel(1)
    server.sendmail(SMTP_ACCT,TGT_ACCTS,message)
    time.sleep(1)
    server.quit()

if __name__ == "__main__":
    plain_email(b"HelloWorld!",b"attack!")