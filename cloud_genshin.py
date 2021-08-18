import time
import httpx

def Next_time() -> int:
    now_time = int(time.time())
    #这里获取上午11点整的时间戳
    next_time = now_time - now_time % 86400 + time.timezone + 39600
    if int(time.time()) > next_time:
        next_time += 14400
    elif int(time.time()) > next_time:
        next_time += 14400
    return next_time

api_url = ""

headers = {
    'x-rpc-combo_token': '',
    'x-rpc-client_type': '',
    'x-rpc-app_version': '',
    'x-rpc-sys_version': '',
    'x-rpc-channel': 'mihoyo',
    'x-rpc-device_id': '',
    'x-rpc-device_name': '',
    'x-rpc-device_model': '',
    'x-rpc-app_id': '',
    'Referer': 'https://app.mihoyo.com',
    'Content-Length': '0',
    'Host': '',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'okhttp/3.14.9'
}

print("Go")
may_start_time = Next_time()
may_end_time = Next_time() + 3
if int(time.time()) < may_start_time:
    time.sleep(may_start_time - int(time.time()))
for i in range(0,30):
    try:
        req = httpx.post(url=f"{api_url}gamer/api/login",headers=headers,data="")
        data = req.json()
    except:
        time.sleep(0.1)
        continue
    if i > 15 and int(time.time()) > may_end_time:
        print("已经没机会了，凉凉 r.i.p")
        break
    elif data["retcode"] == -100005 or -100003:
        time.sleep(2)
        continue
    elif int(time.time()) > may_end_time:
        print("这场已经没机会了，凉凉 r.i.p")
        break
    elif data["retcode"] == 0:
        print("抢位 or 登入成功！")
        time.sleep(1)
        try:
            req2 = httpx.get(url=f"{api_url}wallet/wallet/get",headers=headers)
        except:
            print("尝试签到失败")
            break
        data2 = req2.json()
        if data2["retcode"] == 0:
            if int(data2["data"]["free_time"]["send_freetime"]) != 0:
                print("签到成功？已经获得{}分钟免费时长(总时长：{}分钟)".format(
                    data2["data"]["free_time"]["send_freetime"],
                    data2["data"]["free_time"]["free_time"]
                ))
            else:
                print("未获得免费时长，账号已经签到过了？(总时长：{}分钟)".format(
                    data2["data"]["free_time"]["free_time"]
                ))
        else:
            print("尝试签到失败")
        break
    elif data["retcode"] == -100:
        print(data["message"])
        break