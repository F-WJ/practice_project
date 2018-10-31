__author__  =  'FWJ' 
__time__  =  '2018-10-28 09:08:43' 
from twilio.rest import Client
from datetime import datetime
import time

# my account sid and auth token
account_sid = ''     
auth_token = ''

def send_sms(to, text, tw_mobile=''):
    # tw_mobile: 接收号码
    client=Client(account_sid, auth_token)
    try:
        message=client.messages.create(
            body=text,
            from_=tw_mobile,
            to=to
        )
        print('message status:', message.status)
        return True
    except Exception as e:
        print(e)
        return False

if __name__=='__main__':
    greetings={'9':'早上好，该起床了', '12':'中午好，该吃中饭啦',
    '15':'下午好，可以吃个水果', '23':'晚上好，该睡觉啦'}

    print('Script running!')
    while True:
        now=datetime.now()
        print('time:', now)
        for key in greetings.keys():
            if now.hour==int(key):
                message=greetings.get(key,'This is a test message')
                res = send_sms(to='',text=message)   # to='':发送号码
                if res:
                    print('Message send ok at:',
                    datetime.strftime(now, '%Y-%m-%d %H:%M:%S'))
                    time.sleep(60*60)
                else:
                    print('Message send failed')

        time.sleep(5)