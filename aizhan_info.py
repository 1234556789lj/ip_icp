import re
import requests
import random

# 随机ua
def get_ua():
    first_num = random.randint(55, 62)
    third_num = random.randint(0, 3200)
    fourth_num = random.randint(0, 140)
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)',
        '(Macintosh; Intel Mac OS X 10_12_6)'
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

    ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                  )
    return ua


def aizhan_info(domain, timeout=5):
    """
    利用爱站接口查询权重信息
    """
    header = {
        "Host": "www.aizhan.com",
        "User-Agent": get_ua(),
        "Content-Type": "application/x-www-form-urlencoded",
    }
    #爱站查rank和ipc
    aizhan_Result = {"code": 1, "rank": 0,"domain":domain, "Name": "", "Type": "", "ICP": ""}
    par_rank = r'<img src="//statics.aizhan.com/images/br/(.*?).png" alt=.*?>'
    par_name = r'<span id="icp_company">(.*?)</span>'
    par_type = r'<span id="icp_type">(.*?)</span>'
    par_icp = r'<a target="_blank" href=.*? id="icp_icp">(.*?)</a>'

    try:
        rep = requests.get(url=f"https://www.aizhan.com/cha/{domain}/", headers=header, timeout=timeout)
        #print(rep.text)
        try:
            aizhan_Result["rank"] = int(re.search(par_rank, rep.text).group(1))
        except:
            pass
        try:
            aizhan_Result["Name"] = re.search(par_name, rep.text).group(1)
        except:
            pass
        try:
            aizhan_Result["Type"] = re.search(par_type, rep.text).group(1)
        except:
            pass
        try:
            aizhan_Result["ICP"] = re.search(par_icp, rep.text).group(1)
        except:
            pass
        return aizhan_Result
    except:
        aizhan_Result["code"] = -1
        return aizhan_Result

if __name__ == '__main__':
    #查rank和icp
    result = aizhan_info("gzu.edu.cn", 3)
    # 打印查询结果的各个字段
    for i in result.values():
        print(i)

