import re
import tldextract
import requests
import aizhan_info

def searchDomain(ip, timeout=5):
    # 初始化一个空的主域名列表
    mainDomainNameList = []
    # 初始化一个用于存储查询结果的字典，初始状态为未查询到结果（code=0）
    searchDomainResult = {"code": 0, "ip": ip, "domainList": []}

    # 设置HTTP请求头，包括User-Agent
    headers = {"user-agent": aizhan_info.get_ua()}

    try:
        # 发送GET请求到指定API，查询与给定IP地址相关的域名信息
        rep = requests.get(url=f"http://api.webscan.cc/?action=query&ip={ip}", headers=headers, timeout=timeout)

        # 如果API响应不是 "null"，则表示有查询结果
        if rep.text != "null":
            # 解析JSON响应
            results = rep.json()

            # 遍历查询结果
            for result in results:
                domainName = result["domain"]

                # 使用正则表达式检查域名是否为IP地址格式，如果是则跳过
                if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", domainName):
                    continue

                # 如果域名已经在主域名列表中，跳过
                if domainName in mainDomainNameList:
                    continue

                # 从域名中提取主域名（例如，从 www.example.com 提取 example.com）
                val = tldextract.extract(domainName)

                # 如果主域名不在主域名列表中，添加到列表中
                if f"{val.domain}.{val.suffix}" not in mainDomainNameList:
                    mainDomainNameList.append(f"{val.domain}.{val.suffix}")

            # 设置查询结果的状态为成功（code=1）并存储主域名列表
            searchDomainResult["code"] = 1
            searchDomainResult["domainList"] = mainDomainNameList
        else:
            # 如果API响应是 "null"，表示未查询到结果，设置查询结果的状态为未找到结果（code=0）
            searchDomainResult["code"] = 0
    except:
        # 发生异常时，设置查询结果的状态为错误（code=-1）
        searchDomainResult["code"] = -1

    # 返回查询结果
    return searchDomainResult

if __name__ == "__main__":
    s = searchDomain("59.51.42.147", 5)
    if s["code"] == 1:
        for i in s["domainList"]:
            print(f"{s['ip']}  {i}")