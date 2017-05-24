# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import logging
import cx_Oracle
from scrapy.exceptions import DropItem
from customs_stat_monthly.items import (
    CrawlLogItem,
    CustomsStatTable1aItem,
    CustomsStatTable1bItem,
    CustomsStatTable2Item,
    CustomsStatTable3Item,
    CustomsStatTable4Item,
    CustomsStatTable5Item,
    CustomsStatTable6Item,
    CustomsStatTable7Item,
    CustomsStatTable8Item,
    CustomsStatTable9Item,
    CustomsStatTable10Item,
    CustomsStatTable11Item,
    CustomsStatTable12Item,
    CustomsStatTable13Item,
    CustomsStatTable14Item,
    CustomsStatTable15Item,
    CustomsStatTable16Item,
)

TABLE_MAP = {
    CrawlLogItem: 'DET_CSM_LOG',
    CustomsStatTable1aItem: 'DET_CSM_1A',
    CustomsStatTable1bItem: 'DET_CSM_1B',
    CustomsStatTable2Item: 'DET_CSM_2',
    CustomsStatTable3Item: 'DET_CSM_3',
    CustomsStatTable4Item: 'DET_CSM_4',
    CustomsStatTable5Item: 'DET_CSM_5',
    CustomsStatTable6Item: 'DET_CSM_6',
    CustomsStatTable7Item: 'DET_CSM_7',
    CustomsStatTable8Item: 'DET_CSM_8',
    CustomsStatTable9Item: 'DET_CSM_9',
    CustomsStatTable10Item: 'DET_CSM_10',
    CustomsStatTable11Item: 'DET_CSM_11',
    CustomsStatTable12Item: 'DET_CSM_12',
    CustomsStatTable13Item: 'DET_CSM_13',
    CustomsStatTable14Item: 'DET_CSM_14',
    CustomsStatTable15Item: 'DET_CSM_15',
    CustomsStatTable16Item: 'DET_CSM_16'
}


class OracleCsmPipeline(object):

    def __init__(self, connstr):
        self.connstr = connstr

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            connstr=crawler.settings.get('ORACLE_CONNSTR'),
        )

    def open_spider(self, spider):
        os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'
        self.conn = cx_Oracle.connect(self.connstr)
        self.cursor = self.conn.cursor()
        self.check_tables()

    def check_tables(self):
        command = 'SELECT TABLE_NAME FROM user_tables'
        self.cursor.execute(command)
        r = self.cursor.fetchall()
        table_names = [row[0].upper() for row in r]
        for item_type, table_name in TABLE_MAP.items():
            if table_name.upper() not in table_names:
                field_names = list(item_type.fields.keys())
                self.create_table(table_name, field_names)

    def create_table(self, table_name, field_names):
        try:
            field_names.remove('hid')
        except ValueError:
            pass
        fields = [field_name + ' nvarchar2(500)'
                  for field_name in field_names]
        fields.append('hid varchar2(32) not null primary key')
        fields.append('create_time date default sysdate')
        field_str = ','.join(fields)
        command = 'CREATE TABLE {}({})'.format(table_name, field_str)
        self.cursor.execute(command)
        self.conn.commit()

        logging.info('Created database "%s"', table_name)

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        self.insert_item(item)
        spider.logger.info('Item saved to database')
        return item

    def insert_item(self, item):
        item_type = type(item)
        table_name = TABLE_MAP[item_type]
        field_names = item.keys()
        values = [item[field_name] for field_name in field_names]

        field_str = ','.join(field_names)
        value_str = ','.join([':%d' % (i + 1) for i in range(len(values))])
        command = 'INSERT INTO {} ({}) VALUES ({})'.format(
            table_name, field_str, value_str)

        self.cursor.execute(command, values)
        self.conn.commit()


class DuplicatesPipeline(object):

    command = 'SELECT count(*) FROM {} WHERE hid=:1'

    def __init__(self, oracle_connstr):
        self.oracle_connstr = oracle_connstr

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            oracle_connstr=crawler.settings.get('ORACLE_CONNSTR'),
        )

    def open_spider(self, spider):
        os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'
        self.conn = cx_Oracle.connect(self.oracle_connstr)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        item_type = type(item)
        table_name = TABLE_MAP[item_type]

        self.cursor.execute(self.command.format(table_name), (item['hid'],))
        count = self.cursor.fetchone()[0]
        if count == 0:
            return item
        else:
            raise DropItem("Duplicate item found: %s" % item)
