import requests
from HandleJs import Py4Js
import pymysql


def translate(tk, content):
    if len(content) > 4891:
        print("长度超限!!!")
        return
    # 更多的userAgent组成字典, 循环读取效果更好
    headers = {
        'referer': 'https://translate.google.cn/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'
    }
    param = {'tk': tk, 'q': content}

    # 英文译德文url, 如需翻译成其他语言需要重新抓取url
    result = requests.get("""https://translate.google.cn/translate_a/single?client=t&sl=en
                            &tl=de&hl=de&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss
                            &dt=t&ie=UTF-8&oe=UTF-8&otf=1&ssel=0&tsel=0&kc=1""", headers=headers, params=param)
    # 返回值: 嵌套list, 使用list方法
    tra = result.json()[0][0][0]
    with open('word.txt', 'w', encoding='utf-8') as fp:
        fp.write(tra)


def main():
    js = Py4Js()
    conn = pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           password='****',
                           db='test',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor
                           )

    sql = "select name from data_content_728 where translated=0 order by id asc limit 1"
    cur = conn.cursor()
    cur.execute(sql)
    res = cur.fetchone()
    cur.close()
    if res:
        content = res['name']
        tk = js.getTk(content)
        translate(tk, content)
    else:
        print('Not data...')


if __name__ == "__main__":
    main()
