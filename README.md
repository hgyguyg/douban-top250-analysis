# 豆瓣电影 Top250 数据分析

基于 Scrapy 爬取豆瓣电影 Top250 数据，经 Pandas 清洗分析后写入 MySQL，并通过 Matplotlib 生成多维度可视化报告的完整数据分析项目。

## 项目结构

```
douban_movie_analysis/
├── clean_and_analysis/              # 数据清洗与分析
│   ├── analysis.ipynb               # Jupyter 数据分析笔记本
│   └── clean_mysql.py               # MySQL 数据清洗脚本
├── douban_spider/                   # Scrapy 爬虫项目
│   ├── spiders/
│   │   ├── __init__.py
│   │   └── douban_top250.py         # 核心爬虫
│   ├── __init__.py
│   ├── items.py                     # 数据模型
│   ├── middlewares.py               # 中间件
│   ├── pipelines.py                 # 数据管道
│   ├── scrapy.cfg                   # Scrapy 配置
│   └── settings.py                  # 爬虫设置
├── sql/
│   └── analysis                     # SQL 分析文件
├── douban_top250.json               # 原始爬取数据
├── douban_top250_analysis.csv       # 清洗后数据
├── douban_top250_analysis.json      # 分析结果 JSON
├── douban_top250_analysis.png       # 可视化报告
├── scrapy.cfg                       # Scrapy 配置（根目录）
├── README.md
└── .gitignore
```

## 技术栈

- Python 3 + Scrapy 爬虫框架
- MySQL 数据库存储
- Pandas 数据清洗
- Matplotlib/Seaborn 数据可视化
- Jupyter Notebook 分析报告

## 使用方法

### 1. 安装依赖

```bash
pip install scrapy pymysql pandas matplotlib seaborn jupyter
```

### 2. 配置数据库

在 MySQL 中创建数据库：

```sql
CREATE DATABASE douban CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

修改 `clean_and_analysis/clean_mysql.py` 中的数据库连接信息。

### 3. 运行爬虫

```bash
cd douban_spider
scrapy crawl douban_top250
```

### 4. 数据清洗与分析

```bash
python clean_and_analysis/clean_mysql.py
```

或使用 Jupyter Notebook：

```bash
jupyter notebook clean_and_analysis/analysis.ipynb
```

## 数据说明

- `douban_top250.json` - 原始爬取数据（250条）
- `douban_top250_analysis.csv` - 清洗后结构化数据
- `douban_top250_analysis.png` - 可视化分析报告

## 注意事项

本项目仅用于学习目的，爬取频率已控制，请勿频繁运行爬虫。
