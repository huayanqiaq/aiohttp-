# -*- coding: utf-8 -*-
import asyncio
import aiohttp
import json

# HTTp请求头部
headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}
# cookies字符串
cookie_str = "BAIDUID=655A586C051B680BED6B912A0F5FC1B9:FG=1; BIDUPSID=655A586C051B680BED6B912A0F5FC1B9; PSTM=1535010772; __cfduid=d67d1af4952159ebc5e2e6893c990e6d81536145698; BDUSS=BqN1M4WVdOQ2h1LWswVzhzem5pSFZFT1RnWXdVWi1zSmRFcThWTVM1RzFsZUpiQVFBQUFBJCQAAAAAAAAAAAEAAAAivRgzyfrLwNPrubK1xLqjvccAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALUIu1u1CLtbeT; H_PS_PSSID=26524_1435_21090_27401; delPer=0; PSINO=3; PHPSESSID=u8mis64vda5qgs8b0b741frdp1; Hm_lvt_4010fd5075fcfe46a16ec4cb65e02f04=1539418908,1541729969; Hm_lpvt_4010fd5075fcfe46a16ec4cb65e02f04=1541729969"
# 需要POST的内容
payload = {'fromdt': '1541779200', 'todt': '1541865600'}


# 把cookie字符串变成字典形式
def make_cookie(str):
    list1 = str.split(";")
    dict1 = {}
    for i in list1:
        i1 = i.rstrip()
        # print(i1)
        m = i1.split("=", maxsplit=1)
        dict1[m[0].lstrip()] = m[1].lstrip()
    print(dict1)
    return dict1


# 异步GET请求方法
async def get(url, cookies):
    session1 = aiohttp.ClientSession(headers=headers, cookies=cookies)
    response = await session1.get(url)
    result = response.status
    await session1.close()
    response.close()
    return result


# 异步POST请求方法
async def post(url, payload, cookies):
    session1 = aiohttp.ClientSession(headers=headers, cookies=cookies)
    response = await session1.post(url, data=json.dumps(payload))
    result = await response.text()
    await session1.close()
    response.close()
    return result


# 异步请求
async def request():
    cookies = make_cookie(cookie_str)
    url = "http://i.baidu.com/calendars/calendars/listInfo"
    print('Waiting for', url)
    result = await post(url, payload, cookies)  # 请求方法可以改变成POST或者GET
    # print('Get response from', url, 'Result:', result)
    print(result)


def main():
    tasks = [asyncio.ensure_future(request()) for _ in range(5)] #这里修改并发
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))


if __name__ == "__main__":
    main()
