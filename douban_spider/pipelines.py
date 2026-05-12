# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import pymysql

#按json格式输出
class DoubanMoviePipeline:
    def __init__(self):
        self.items = []

    def open_spider(self, spider=None):
        print("开始爬取...")

    def process_item(self, item, spider=None):
        item_copy = dict(item)
        self.items.append(item_copy)
        print(f"本次爬取电影：{item_copy['title']}（排名：{item_copy['rank']}）")
        return item

    def close_spider(self, spider=None):
        print(f"爬取结束，共收集 {len(self.items)} 条数据，开始排序并写入...")
        try:
            self.items.sort(key=lambda x: int(x['rank']))
        except Exception as e:
            print(f"排序失败: {e}，按爬取顺序写入")

        output_file = 'douban_top250.json'

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, ensure_ascii=False, indent=2)
        
        print(f"写入完成，共写入 {len(self.items)} 条数据到 {output_file}")

#按MySQL输出
class Doubanmovie_mysql:
    def __init__(self):
        self.items = []
        self.conn = None
        self.cursor = None

    def open_spider(self, spider=None):
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='DB_PASSWORD',
            db = 'scrapy',
            charset='utf8mb4',
            use_unicode=True,
        )
        self.cursor = self.conn.cursor()
        sql = '''CREATE TABLE IF NOT EXISTS douban_movies (
            `rank` INT PRIMARY KEY,
            title VARCHAR(100),
            director VARCHAR(200),
            attrs TEXT,
            `date` VARCHAR(20),
            rating_num FLOAT,
            rating_people INT
        ) CHARACTER SET utf8mb4;
        '''
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(f"建表错误：{e}")

    def process_item(self, item, spider=None):
        item_copy = dict(item)
        self.items.append(item_copy)
        print(f"本次爬取电影：{item_copy['title']}（排名：{item_copy['rank']}）")
        return item

    def close_spider(self, spider=None):
        try:
            self.items.sort(key=lambda x: int(x['rank']))
        except Exception as e:
            print(f"排序失败: {e}，按爬取顺序写入")
        for item in self.items:
            sql = '''
            insert into douban_movies
                (`rank`,title,director,attrs,`date`,rating_num,rating_people)
            values
                (%s,%s,%s,%s,%s,%s,%s)
            '''

            data = (
                item['rank'],
                item['title'],
                item['director'],
                item['attrs'],
                item['date'],
                item['rating_num'],
                item['rating_people']
            )
            try:
                self.cursor.execute(sql, data)
                self.conn.commit()
            except Exception as e:
                self.conn.rollback()
                print(f"写入错误：{e}")
        print(f"爬取结束，共收集 {len(self.items)} 条数据，开始排序并写入...")
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


