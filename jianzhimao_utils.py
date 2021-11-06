import pymysql
import logging
import settings as s
from hashlib import sha1
import datetime

connection = pymysql.connect(**s.MYSQL)
cursor = connection.cursor()


def format_date(date_str):
    """转换时间"""
    now_date = datetime.datetime.now()
    if date_str == "刚刚" or "前" in date_str:
        return now_date.strftime("%Y-%m-%d")
    if date_str == "昨天":
        return (now_date + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
    if date_str == "前天":
        return (now_date + datetime.timedelta(days=-2)).strftime("%Y-%m-%d")
    return date_str


def hash_key(data):
    """生成字符串的hash值"""
    return sha1(data.encode("utf8")).hexdigest()


class MysqlUtil(object):

    @staticmethod
    def create(sql):
        """创建表格"""
        try:
            cursor.execute(sql)
        except Exception as e:
            logging.error(f"创建表格报错，e:{e},sql:{sql}")
            connection.rollback()

    @staticmethod
    def modity(sql):
        """插入数据/修改数据"""
        try:
            cursor.execute(sql)
            connection.commit()
        except Exception as e:
            logging.error(f"插入数据/修改数据报错，e:{e},sql:{sql}")
            connection.rollback()
            return s.FUNC_CODE_ERROR

    @staticmethod
    def query(sql):
        """查询数据"""
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            logging.error(f"查询数据报错，e:{e},sql:{sql}")
            connection.rollback()


if __name__ == '__main__':
    util = MysqlUtil()
    # print(util.query("select * from citys"))
    print(format_date("4小时前"))
