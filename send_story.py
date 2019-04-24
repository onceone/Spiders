#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：onceone time:2019/4/23
import requests
import time
import random
import smtplib
from bs4 import BeautifulSoup
from email.mime.text import MIMEText

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
url_list = []  # 每个故事的链接
name_list = []  # 每个故事的名字


def get_html(url):
    ''' 获取原网页链接'''
    try:
        res = requests.get(url, headers=headers, timeout=30)
        res.raise_for_status()  # 如果状态不是200，引发HTTPerror异常
        # t1 = res.encoding  # 从HTTP header中猜测响应内容编码方式
        # t2 = res.apparent_encoding # 从内容分析出响应编码方式
        res.encoding = res.apparent_encoding  # 根据网页内容分析出编码方式
        # res.encoding='utf-8'  # 转码
        # print(t1,t2)

        return res.text

    except:
        return '产生异常'


def get_all_story_link(html):
    '''获取每页中故事的名称及链接，存在列表中'''
    url_based = 'http://www.tom61.com/'
    soup = BeautifulSoup(html, 'lxml')
    html_part = soup.find(class_='txt_box')  # 获取一页中故事的标签
    # print(html_part)
    a_tag = html_part.find_all(name='a')  # 获取所有故事链接标签，存在列表中
    # print('-'*100)
    # print(a_tag)

    # 循环遍历存储链接和故事名
    for temp in a_tag:
        url_list.append(url_based + temp.get('href'))  # 提取每个故事的链接，追加到列表中
        name_list.append(temp.get('title'))  # 提取每个故事的名称，追加到列表中


def packaging(story_name, story_url):
    '''打包'''
    package_name_link = list(zip(story_name, story_url))
    print('查看打包')
    print(package_name_link)

    return package_name_link


def send_story_to_email(story_name, url):
    '''发送故事到指定邮件'''

    msg_from = '1301016428@qq.com'  # 发送方邮箱
    passwd = ''  # 填送发送方邮箱授权码,此处可百度查询如何获得授权码
    receivers = ['2904389420@qq.com']  # 收件人邮箱

    subject = '今日的睡前故事--->>>{}'.format(story_name)  # 主题

    # 获得故事原网页
    html_story = get_html(url)

    # 提取故事的文字内容
    content = get_story_content(html_story)

    # 以下为发送
    msg = MIMEText(content)  # 发送内容
    msg['Subject'] = subject  # 主题
    msg['From'] = msg_from  # 发送方
    msg['To'] = ','.join(receivers)

    try:

        s = smtplib.SMTP_SSL('smtp.qq.com', 465)  # 邮件服务器及端口号
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg['To'].split(','), msg.as_string())

        print('邮件发送成功')
    except:
        print('发送失败')
    finally:
        s.quit()


def get_story_content(html):
    '''获取故事的文字内容'''
    text = []  # 故事内容
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find(class_='t_news_txt')  # 整个故事“块”
    # print(div)
    for temp in div.find_all('p'):
        text.append(temp.text)
    # print(text)
    content = '\n'.join(text)  # 每段分开

    return content


def main():
    for i in range(1, 11):  # 爬取页数范围
        if i == 1:
            url = 'http://www.tom61.com/ertongwenxue/shuiqiangushi/index.html'
        else:
            url = 'http://www.tom61.com/ertongwenxue/shuiqiangushi/index_{}.html'.format(i)

        print('正在爬取第{}页的故事'.format(i))

        # 提取一个网页html
        html = get_html(url)

        # 获取一页网页中所有故事的名称及链接
        get_all_story_link(html)
        time.sleep(0.15)

    # 所有链接爬去完成，打个包
    package_name_link = packaging(name_list, url_list)

    print('--->>>>>>>>爬取完成啦---------发邮件咯------------')
    random_choice_name_link = random.choice(package_name_link)  # 随机选择故事链接

    name_random_choice = random_choice_name_link[0]
    url_random_choice = random_choice_name_link[1]
    print('发送的故事名和链接:')
    print(name_random_choice)
    print(url_random_choice)

    # 发送故事
    send_story_to_email(name_random_choice, url_random_choice)


if __name__ == '__main__':
    main()
