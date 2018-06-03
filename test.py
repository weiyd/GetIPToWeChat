# -*-coding:utf8-*-
import itchat
from urllib import request
import time, schedule


def get_ip():
    try:
        ip = request.urlopen('http://ip.42.pl/raw', timeout=10).read()
        return str(ip)[2:-1]
    except BaseException:
        print("连接错误,IP未更新")
        return IP


def get_time():
    time_array = time.localtime(time.time())
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return now_time


def send_msg(name='尔了个达'):
    global IP
    users = itchat.search_friends(name=name)
    if len(users) >= 1:
        user_name = users[0]['UserName']
        text = "更改时间：%s\n更改地址：%s" % (get_time(), IP)
        try:
            itchat.send(text, toUserName=user_name)
            print(text.replace('\n', '\t'))
        except BaseException:
            print("发送微信超时")
            TIMEOUT = True
    else:
        print("未找到用户名")


def ischanged_ip():
    global IP
    new_ip = get_ip()
    if new_ip == IP:
        if TIMEOUT:
            send_msg()
        else:
            print('IP未改变')
    else:
        IP = new_ip
        send_msg()


TIMEOUT = False # 微信发送超时 下次要重新发送至微信
IP = '114.221.159.240'
if __name__ == '__main__':
    itchat.auto_login(hotReload=True)  # 首次扫描登录后后续自动登录
    schedule.every(0.3).minutes.do(ischanged_ip)
    while True:
        schedule.run_pending()
