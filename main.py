# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from time import sleep
from time import time
import csv
from aizhan_info import aizhan_info
from ip_to_domain import searchDomain
import threadpool

url_list=[]

# def write_targets(url, domain, rank, name, unit_type, icp, filename):
#     with open(filename, "a+", encoding="utf-8") as f:
#         # 将字节对象解码为字符串
#         info = f'ip：{url}, 域名：{domain}, rank：{rank}, 名称：{name}, 性质：{unit_type}, icp：{icp}'
#         f.write(info + "\n")

def write_targets_to_csv(url, domain, rank, name, unit_type, icp, filename):
    # 创建或打开 CSV 文件，并指定编码为 UTF-8
    with open(filename, mode='a+', newline='', encoding='utf-8-sig') as file:
        # 创建 CSV writer 对象
        writer = csv.writer(file)
        # 创建要写入的数据行
        data_row = [url, domain, rank, name, unit_type, icp]
        # 使用 writerow 方法将数据行写入 CSV 文件
        writer.writerow(data_row)

def ip_info(url):
    #查询域名
    check_result=searchDomain(url)
    if check_result['code']==1:
        for domain in check_result['domainList']:
            continue
    elif check_result['code']==0:
        print(f'\033[31mip：{url}查不到域名\033[0m')
    else:
        print("域名查询发生异常，-1")

    #利用爱站查rank和ICP
    if check_result['code']==1:
        for domain in check_result['domainList']:
            aizhan_result = aizhan_info(domain)
            # 使用字符串格式化控制输出宽度，例如使用 {:<20} 来确保字段宽度为 20 个字符并左对齐
            if aizhan_result["rank"]>=1:
                output = f'\033[32murl：{url:<20}   域名：{aizhan_result["domain"]:<20}\033[0m    \033[31mrank：{aizhan_result["rank"]:<5}\033[0m    \033[32m名称：{aizhan_result["Name"]:<20}  性质：{aizhan_result["Type"]:<20}  icp：{aizhan_result["ICP"]}\033[0m'
            else:
                output = f'\033[32murl：{url:<20}   域名：{aizhan_result["domain"]:<20}    rank：{aizhan_result["rank"]:<5}    名称：{aizhan_result["Name"]:<20}  性质：{aizhan_result["Type"]:<10}  icp：{aizhan_result["ICP"]}\033[0m'
            print(output)
            # 调用函数，将相关信息写入文件
            #write_targets(url, aizhan_result["domain"], aizhan_result["rank"], aizhan_result["Name"], aizhan_result["Type"], aizhan_result["ICP"],"output.txt")
            write_targets_to_csv(url, aizhan_result["domain"], aizhan_result["rank"], aizhan_result["Name"], aizhan_result["Type"], aizhan_result["ICP"],"output.csv")
    elif check_result['code']==0:
        print(f'\033[31mip：{url}查不到域名\033[0m')
    else:
        print("ICP查询发生异常，-1")
    sleep(3)
    #print("3秒结束")


#多线程
def multithreading(url_list, pools=5):
    works = []
    for i in url_list:
        # works.append((func_params, None))
        works.append(i)
    # print(works)
    pool = threadpool.ThreadPool(pools)
    reqs = threadpool.makeRequests(ip_info, works)
    [pool.putRequest(req) for req in reqs]
    pool.wait()

if __name__ == '__main__':
    # ip_info('59.51.42.147')
    # ip_info('gzu.edu.cn')
    # ip_info('110.164.188.26')

    show = r'''
    ip反查域名和ICP信息
	'''
    print(show + '\n')
    arg = ArgumentParser(description='ip反查域名和ICP信息')
    arg.add_argument("-u",
                     "--url",
                     help="Target URL; Example:python3 test.py -u http://ip:port")
    arg.add_argument("-f",
                     "--file",
                     help="Target URL; Example:python3 test.py -f url.txt")
    args = arg.parse_args()
    url = args.url
    filename = args.file
    print("[+]任务开始.....")
    start = time()
    if url != None and filename == None:
        ip_info(url)
    elif url == None and filename != None:
        for i in open(filename):
            i = i.replace('\n', '')
            url_list.append(i)
        multithreading(url_list, 5)
    end = time()
    print('任务完成,用时%ds.' % (end - start))