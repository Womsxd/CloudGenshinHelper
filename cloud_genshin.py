import time
import httpx

def Next_time() -> int:
    now_time = int(time.time())
    nextday_time = now_time - now_time % 86400 + time.timezone + 39600
    if int(time.time()) > nextday_time:
        nextday_time += 14400
    if int(time.time()) > nextday_time:
        nextday_time += 14400
    if int(time.time()) > (nextday_time + 10):
        print("今天好像已经没机会了")
        exit()
    return nextday_time

headers = {
    'x-rpc-combo_token': '',
    'x-rpc-client_type': '2',
    'x-rpc-app_version': '1.0.0',
    'x-rpc-sys_version': '',
    'x-rpc-channel': 'mihoyo',
    'x-rpc-device_id': '',
    'x-rpc-device_name': '',
    'x-rpc-device_model': '',
    'x-rpc-app_id': '',
    'Referer': 'https://app.mihoyo.com',
    'Content-Length': '0',
    'Host': 'api-cloudgame.mihoyo.com',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'okhttp/3.14.9'
}

print("Go")
may_start_time = Next_time()
may_end_time = Next_time() + 5
if int(time.time()) < may_start_time:
    time.sleep(may_start_time - int(time.time()) - 0.015)
for i in range(0,40):
    try:
        req = httpx.post(url="https://api-cloudgame.mihoyo.com/hk4e_cg_cn/gamer/api/login",headers=headers,data="")
        data = req.json()
    except:
        continue
    if i > 25 and int(time.time()) > may_end_time:
        print("已经没机会了，凉凉 r.i.p")
        break
    elif data["retcode"] == -100005 or data["retcode"] == -100003:
        time.sleep(1.9)
        continue
    elif int(time.time()) > may_end_time:
        print("来晚了没机会了，等待明天吧")
        break
    elif data["retcode"] == 0:
        print("抢位 or 登入成功！")
        time.sleep(1)
        try:
            req2 = httpx.post(url="https://api-cloudgame.mihoyo.com/hk4e_cg_cn/gamer/api/onceActiveDone",headers=headers,data="")
            data2 = req2.json()
        except:
            print("尝试领取新人奖励失败")
            break
        if data2["data"] != "":
            msg = str(data2["data"]["sends"][0]["msg"])
            msg.replace("赠送%免费","赠送{}分钟免费".format(str(data2["data"]["sends"][0]["num"])))
            print(msg)
        else:
            print("已领取过新人奖励")
        try:
            req3 = httpx.get(url="https://api-cloudgame.mihoyo.com/hk4e_cg_cn/wallet/wallet/get",headers=headers)
            data3 = req3.json()
        except:
            print("尝试签到失败")
            break
        if data3["retcode"] == 0:
            if int(data3["data"]["free_time"]["send_freetime"]) != 0:
                print("签到成功？已经获得{}分钟免费时长(总时长：{}分钟)".format(
                    data3["data"]["free_time"]["send_freetime"],
                    data3["data"]["free_time"]["free_time"]
                ))
            else:
                print("未获得免费时长，账号已经签到过了？(总时长：{}分钟)".format(
                    data3["data"]["free_time"]["free_time"]
                ))
        else:
            print("尝试签到失败")
        break
    elif data["retcode"] == -100:
        print(data["message"])
        break