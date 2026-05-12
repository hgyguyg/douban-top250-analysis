from logging import exception

import pandas as pd
import pymysql
import re

#读取数据库
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='DB_PASSWORD',
    db='scrapy',
    charset='utf8mb4',
)
df = pd.read_sql('select * from douban_movies', connection)
connection.close()

#数据清洗
df['attrs'] = df['attrs'].str.replace("/...",'')
df['attrs'] = df['attrs'].str.replace("/ ...",'')
df['attrs'] = df['attrs'].str.replace("...",'')
df['attrs'] = df['attrs'].str.replace(":",'')
df['attrs'] = df['attrs'].fillna('未知').str.strip()

df['director'] = df['director'].str.replace("...",'')
df['director'] = df['director'].str.replace('\u00a0','')
df['director'] = df['director'].str.replace('\xa0','')
df['director'] = df['director'].str.replace('&nbsp;','')
df['director'] = df['director'].str.replace('&nbsp;','')

df['date'] = df['date'].str.extract(r'(\d{4})')
df['date'] = df['date'].fillna('0000') #0000代表未知

df['director'] = df['director'].fillna('未知').str.strip()

df['rating_num'] = pd.to_numeric(df['rating_num'], errors='coerce').fillna(0)
df['rating_people'] = pd.to_numeric(df['rating_people'], errors='coerce').fillna(0)

#将清洗后的数据写入数据库
sql = '''create table if not exists douban_movies_cleaned \
(
    `rank` int not null,
    title varchar(100) not null,
    director varchar (100) not null,
    attrs varchar (100) not null,
    `date` year not null,
    rating_num float not null,
    rating_people int not null
    );
'''
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='DB_PASSWORD',
    db='scrapy',
    charset='utf8mb4',
)
cursor = connection.cursor()
try:
    cursor.execute(sql)
except Exception as e:
    print(f"建表错误：{e}")

sql = '''
          insert into douban_movies_cleaned
              (`rank`, title, director, attrs, `date`, rating_num, rating_people)
          values (%s, %s, %s, %s, %s, %s, %s) ;
          '''
for id,row in df.iterrows():
    data = (
        int(row['rank']),
        row['title'],
        row['director'],
        row['attrs'],
        int(row['date']),
        float(row['rating_num']),
        int(row['rating_people'])
    )
    try:
        cursor.execute(sql, data)
        connection.commit()
    except Exception as e:
        print(f"写入第{row['rank']}条记录时发生错误：{e}")
print(f"写入结束，共写入{len(df)}条记录")
if cursor:
    cursor.close()
if connection:
    connection.close()