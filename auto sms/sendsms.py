__author__  =  'FWJ' 
__time__  =  '2018-10-26 09:41:58' 
from twilio.rest import Client
from datetime import datetime
import time

def sendmessage():
    reservetime()
    # my account sid and auth token
    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)


    message = client.messages.create(
        body = "hello,FWJ",
        from_='', # 发送号码
        to=''  # 接送号码
    )

    print(message.sid)


def reservetime():
    # 预约发送
    # days = input('')
    while 1:
        # 预约时间
        dt = datetime.strptime('2018-10-26 16:41:00', '%Y-%m-%d %H:%M:%S')
        # 当前时间
        dtnow = datetime.now()

        b = (dt-dtnow).total_seconds()
        print(b)
        time.sleep(b)
        print('匹配成功')
        break

    


def timeedsending():
    # 定时发送
    a = str(datetime.today()).split(" ")[1].split(".")[0]
    print(a)
    


sendmessage()
# timeedsending()


