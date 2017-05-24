import re
import scrapy
import logging
import hashlib
import cx_Oracle
from locale import *

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

setlocale(LC_NUMERIC, 'English_US')
# LOGGER = logging.getLogger(__name__)


class CsmSpider(scrapy.Spider):
    name = 'csm'
    allowed_domain = ['customs.gov.cn']
    start_urls = [
        'http://www.customs.gov.cn/publish/portal0/tab68101/'
    ]
    tab_names = [
        '(1)进出口商品总值表 A:年度表',
        '(1)进出口商品总值表 B:月度表',
        '(2)进出口商品国别(地区)总值表',
        '(3)进出口商品构成表',
        '(4)进出口商品类章总值表',
        '(5)进出口商品贸易方式总值表',
        '(6)出口商品贸易方式企业性质总值表',
        '(7)进口商品贸易方式企业性质总值表',
        '(8)进出口商品经营单位所在地总值表',
        '(9)进出口商品境内的地/货源地总值表',
        '(10)进出口商品关别总值表',
        '(11)特定地区进出口总值表',
        '(12)外商投资企业进出口总值表',
        '(13)出口主要商品量值表',
        '(14)进口主要商品量值表',
        '(15)对部分国家(地区)出口商品类章金额表',
        '(16)自部分国家(地区)出口商品类章金额表'
    ]

    def __init__(self):
        self.func_map = self.map_parse_function()
        self.item_map = self.map_item_initializer()
        self.fields_map = self.map_table_fields()
        self.header_height_map = self.map_header_height()
        self.requested_url = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def map_parse_function(self):
        func_map = {}
        for i, tab_name in enumerate(self.tab_names):
            if i in (0, 1, 2, 3, 4, 8, 9, 10, 11):
                func_map[tab_name] = self.parse_table_normal
            elif i in (5, 6, 7):
                func_map[tab_name] = self.parse_table_dual
            elif i in (12,):
                func_map[tab_name] = self.parse_table_12
            elif i in (13, 14):
                func_map[tab_name] = self.parse_table_13_14
            elif i in (15, 16):
                func_map[tab_name] = self.parse_table_15_16

        return func_map

    def map_item_initializer(self):
        item_map = {}
        items = [
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
        ]
        for i, tab_name in enumerate(self.tab_names):
            item_map[tab_name] = items[i]
        return item_map

    def map_header_height(self):
        header_height_map = {}
        heights = [(2, 1)] * 17
        heights[6:8] = [(3, 1)] * 2
        heights[13:15] = [(2, 2)] * 2
        for i, tab_name in enumerate(self.tab_names):
            header_height_map[tab_name] = heights[i]
        return header_height_map

    def map_table_fields(self):
        fields_map = {}
        fields = [
            # Table 1a
            ['imp_exp', 'exp', 'imp', 'balance',
             'yoy_imp_exp', 'yoy_exp', 'yoy_imp'],
            # Table 1b
            ['imp_exp', 'exp', 'imp', 'balance',
             'ytd_imp_exp', 'ytd_exp', 'ytd_imp', 'ytd_balance'],
            # Table 2
            ['imp_exp', 'ytd_imp_exp', 'exp', 'ytd_exp', 'imp',
             'ytd_imp', 'yoy_ytd_imp_exp', 'yoy_ytd_exp', 'yoy_ytd_imp'],
            # Table 3
            ['exp', 'ytd_exp', 'imp', 'ytd_imp',
             'yoy_ytd_exp', 'yoy_ytd_imp'],
            # Table 4
            ['exp', 'ytd_exp', 'imp', 'ytd_imp',
             'yoy_ytd_exp', 'yoy_ytd_imp'],
            # Table 5
            ['imp_exp', 'yoy_imp_exp', 'ytd_imp_exp', 'yoy_ytd_imp_exp',
             'exp', 'yoy_exp', 'ytd_exp', 'yoy_ytd_exp', 'imp', 'yoy_imp',
             'ytd_imp', 'yoy_ytd_imp'],
            # Table 6
            ['sum_val', 'sum_yoy', 'soe_val', 'soe_yoy',
             'fie_subtotal_val', 'fie_subtotal_yoy',
             'fie_ce_val', 'fie_ce_yoy',
             'fie_jv_val', 'fie_jv_yoy', 'fie_foe_val', 'fie_foe_yoy',
             'pe_val', 'pe_yoy', 'other_val', 'other_yoy'],
            # Table 7
            ['sum_val', 'sum_yoy', 'soe_val', 'soe_yoy',
             'fie_subtotal_val', 'fie_subtotal_yoy',
             'fie_ce_val', 'fie_ce_yoy',
             'fie_jv_val', 'fie_jv_yoy', 'fie_foe_val', 'fie_foe_yoy',
             'pe_val', 'pe_yoy', 'other_val', 'other_yoy'],
            # Table 8
            ['imp_exp', 'ytd_imp_exp', 'exp', 'ytd_exp', 'imp', 'ytd_imp',
             'yoy_ytd_imp_exp', 'yoy_ytd_exp', 'yoy_ytd_imp'],
            # Table 9
            ['imp_exp', 'ytd_imp_exp', 'exp', 'ytd_exp', 'imp', 'ytd_imp',
             'yoy_ytd_imp_exp', 'yoy_ytd_exp', 'yoy_ytd_imp'],
            # Table 10
            ['imp_exp', 'ytd_imp_exp', 'exp', 'ytd_exp', 'imp', 'ytd_imp',
             'yoy_ytd_imp_exp', 'yoy_ytd_exp', 'yoy_ytd_imp'],
            # Table 11
            ['imp_exp', 'ytd_imp_exp', 'exp', 'ytd_exp', 'imp', 'ytd_imp',
             'yoy_ytd_imp_exp', 'yoy_ytd_exp', 'yoy_ytd_imp'],
            # Table 12
            ['imp_exp', 'ytd_imp_exp', 'exp', 'ytd_exp', 'imp', 'ytd_imp',
             'yoy_ytd_imp_exp', 'yoy_ytd_exp', 'yoy_ytd_imp'],
            # Table 13
            ['quantity', 'amount', 'quantity_ytd', 'amount_ytd',
             'quantity_yoy', 'amount_yoy',
             'quantity_ytd_yoy', 'amount_ytd_yoy'],
            # Table 14
            ['quantity', 'amount', 'quantity_ytd', 'amount_ytd',
             'quantity_yoy', 'amount_yoy',
             'quantity_ytd_yoy', 'amount_ytd_yoy'],
            # Table 15
            ['amount', 'amount_ytd'],
            # Table 16
            ['amount', 'amount_ytd'],
        ]
        for i, tab_name in enumerate(self.tab_names):
            fields_map[tab_name] = fields[i]
        return fields_map

    def parse(self, response):
        yrs = response.xpath(
            '//*[@id="ess_ctr187729_HtmlModule_lblContent"]'
            '/div/div[2]/span/text()').extract()

        c = re.compile(r'\s*(\d{4})年?\s*', re.M)
        yrs = map(lambda x: c.findall(x)[0],
                  filter(lambda x: c.match(x) is not None, yrs))

        for year in yrs:
            xpath = '//div[@class="tbtj{}_tab"]'.format(year)
            for table in response.xpath(xpath):
                currency = ''
                for i, tr in enumerate(table.xpath('table/tbody/tr')):
                    if i == 0:
                        currency_str = parse_currency(
                            tr.xpath('td[1]/text()').extract()[0])
                        if currency_str is not None:
                            currency = currency_str
                            # print('Currency:', currency)
                        continue
                    tab_str = tr.xpath('td[1]/text()').extract()
                    if tab_str is None or len(tab_str) < 1:
                        continue
                    tab_name = parse_table_name(tab_str[0])
                    # print('Table:', tab_name)
                    if (tab_name is None or
                            tab_name not in self.tab_names):
                        continue

                    for a in tr.xpath('td[2]/a'):
                        month = a.xpath('text()').extract()[0]
                        month = parse_month(month)
                        if month is None:
                            continue
                        urls = a.xpath('@href').extract()
                        if len(urls) < 1:
                            continue
                        url = response.urljoin(urls[0])

                        # 查重，排除已采集的网址
                        # if self.duplicate_url(url):
                        #     continue

                        # if self.invalid_url(url):
                        #     continue

                        meta = {}
                        meta['YEAR'] = year
                        meta['MONTH'] = month
                        meta['CURRENCY'] = currency
                        meta['ITEM'] = self.item_map[tab_name]
                        meta['FIELDS'] = self.fields_map[tab_name]
                        meta['HEADER_HEIGHT'] = (
                            self.header_height_map[tab_name])
                        func = self.func_map[tab_name]
                        yield scrapy.Request(url, func, meta=meta)

    '''
    def duplicate_url(self, url):
        if self.requested_url is None:
            self.requested_url = set()
        if url in self.requested_url:
            LOGGER.warning('Found duplicated url <GET %s>', url)
            return True
        self.requested_url.add(url)

        command = 'SELECT count(*) FROM DET_CSM_LOG WHERE hid=:1'
        m = hashlib.md5()
        m.update(url.encode())
        hid = m.hexdigest()
        self.cursor.execute(command, (hid,))
        count = self.cursor.fetchone()[0]
        if count > 0:
            LOGGER.info('Url has already been acquired <GET %s>', url)
            return True
        else:
            return False

    def invalid_url(self, url):
        if url.endswith('.xls'):
            LOGGER.warning("Xls content isn't supported <GET %s>", url)
            return True
    '''

    def parse_table_normal(self, response):
        # 1a, 1b, 2, 3, 4, 8, 9, 10, 11
        title_xpath = '//div[contains(@class,"titTop")]'
        title = response.xpath(title_xpath).extract()[0]
        year, month = parse_title(title)
        if year is None or month is None:
            year = response.meta['YEAR']
            month = response.meta['MONTH']
        currency = response.meta['CURRENCY']
        item_initializer = response.meta['ITEM']
        fields = response.meta['FIELDS']
        col_height, row_height = response.meta['HEADER_HEIGHT']
        units, title_name = '', ''
        xpath = '//*[contains(@style,"BORDER-COLLAPSE: collapse")]/tbody/tr'
        i_header, i_row, n_col = 0, 1, 0
        for i, tr in enumerate(response.xpath(xpath)):
            tds = tr.xpath('td').extract()
            n_col = max(n_col, len(tds))
            if i == i_header:
                test_title, _ = parse_title(tds[0])
                if test_title is not None:
                    i_header += 1
                    continue
                units = parse_units(tds)
                if units is None:
                    title_name = parse_title_name(tds)
                    i_header -= 1
                elif units == '':
                    i_header += 1
                continue
            elif i == i_header + 1:
                title_name = parse_title_name(tds)
                continue
            elif i <= i_header + col_height:
                continue
            if check_empty_row(tds, n_col):
                continue

            item = item_initializer()
            item['report_year'] = year
            item['report_month'] = month
            item['currency'] = currency
            item['units'] = units
            item['title_name'] = title_name
            item['idx'] = i_row
            i_row += 1
            for j, td_html in enumerate(tds):
                td_str = parse_html_tag(td_html, True)
                if j == 0:
                    item['title'] = td_str
                else:
                    item[fields[j - row_height]] = parse_value(td_str)
            item['hid'] = self.generate_hid(item)
            yield item

        yield self.generate_log_item(response)

    def parse_table_dual(self, response):
        # 5, 6, 7
        title_xpath = '//div[contains(@class,"titTop")]'
        title = response.xpath(title_xpath).extract()[0]
        year, month = parse_title(title)
        if year is None or month is None:
            year = response.meta['YEAR']
            month = response.meta['MONTH']
        currency = response.meta['CURRENCY']
        item_initializer = response.meta['ITEM']
        fields = response.meta['FIELDS']
        col_height, row_height = response.meta['HEADER_HEIGHT']
        units, title_name = '', ''
        xpath = '//*[contains(@style,"BORDER-COLLAPSE: collapse")]/tbody/tr'
        i_header, i_row, n_col = 0, 1, 0
        for i, tr in enumerate(response.xpath(xpath)):
            tds = tr.xpath('td').extract()
            n_col = max(n_col, len(tds))
            if i == i_header:
                test_title, _ = parse_title(tds[0])
                if test_title is not None:
                    i_header += 1
                    continue
                units = parse_units(tds)
                if units is None:
                    title_name = parse_title_name(tds)
                    i_header -= 1
                elif units == '':
                    i_header += 1
                continue
            elif i == i_header + 1:
                title_name = parse_title_name(tds)
                continue
            elif i <= i_header + col_height:
                continue
            if check_empty_row(tds, n_col):
                continue

            if (i - i_header - col_height - 1) % 2 == 0:
                item = item_initializer()
                item['report_year'] = year
                item['report_month'] = month
                item['currency'] = currency
                item['units'] = units
                item['title_name'] = title_name
                item['idx'] = i_row
                i_row += 1
                for j, td_html in enumerate(tds):
                    td_str = parse_html_tag(td_html, True)
                    if j == 0:
                        item['title'] = td_str
                    else:
                        item[fields[(j - row_height) * 2]] = parse_value(
                            td_str)
            else:
                offset = int(check_empty_str(parse_html_tag(tds[0])))
                for j, td_html in enumerate(tds):
                    td_str = parse_html_tag(td_html, True)
                    item[fields[(j - offset) * 2 + 1]] = parse_value(td_str)
                item['hid'] = self.generate_hid(item)
                yield item

        yield self.generate_log_item(response)

    def parse_table_12(self, response):
        title_xpath = '//div[contains(@class,"titTop")]'
        title = response.xpath(title_xpath).extract()[0]
        year, month = parse_title(title)
        if year is None or month is None:
            year = response.meta['YEAR']
            month = response.meta['MONTH']
        currency = response.meta['CURRENCY']
        item_initializer = response.meta['ITEM']
        fields = response.meta['FIELDS']
        col_height, row_height = response.meta['HEADER_HEIGHT']
        units, title_name = '', ''
        xpath = '//*[contains(@style,"BORDER-COLLAPSE: collapse")]/tbody/tr'
        i_header, i_row, n_col = 0, 1, 0
        for i, tr in enumerate(response.xpath(xpath)):
            tds = tr.xpath('td').extract()
            n_col = max(n_col, len(tds))
            if i == i_header:
                test_title, _ = parse_title(tds[0])
                if test_title is not None:
                    i_header += 1
                    continue
                units = parse_units(tds)
                if units is None:
                    title_name = parse_title_name(tds)
                    i_header -= 1
                elif units == '':
                    i_header += 1
                continue
            elif i == i_header + 1:
                title_name = parse_title_name(tds)
                continue
            elif i <= i_header + col_height:
                continue
            if check_empty_row(tds, n_col):
                continue

            item = item_initializer()
            item['report_year'] = year
            item['report_month'] = month
            item['currency'] = currency
            item['units'] = units
            item['title_name'] = title_name
            item['idx'] = i_row
            i_row += 1
            c = re.compile(r'.+[计省市区]$')
            for j, td_html in enumerate(tds):
                td_str = parse_html_tag(td_html, True)
                if j == 0:
                    if c.match(td_str) is not None:
                        province = td_str
                        item['title'] = td_str
                        item['province'] = td_str
                    else:
                        item['title'] = td_str
                        item['province'] = province
                else:
                    item[fields[j - row_height]] = parse_value(td_str)
            item['hid'] = self.generate_hid(item)
            yield item

        yield self.generate_log_item(response)

    def parse_table_13_14(self, response):
        title_xpath = '//div[contains(@class,"titTop")]'
        title = response.xpath(title_xpath).extract()[0]
        year, month = parse_title(title)
        if year is None or month is None:
            year = response.meta['YEAR']
            month = response.meta['MONTH']
        currency = response.meta['CURRENCY']
        item_initializer = response.meta['ITEM']
        fields = response.meta['FIELDS']
        col_height, row_height = response.meta['HEADER_HEIGHT']
        units, title_name = '', ''
        xpath = '//*[contains(@style,"BORDER-COLLAPSE: collapse")]/tbody/tr'
        i_header, i_row, n_col = 0, 1, 0
        for i, tr in enumerate(response.xpath(xpath)):
            tds = tr.xpath('td').extract()
            n_col = max(n_col, len(tds))
            if i == i_header:
                test_title, _ = parse_title(tds[0])
                if test_title is not None:
                    i_header += 1
                    continue
                units = parse_units(tds)
                if units is None:
                    title_name = parse_title_name(tds)
                    i_header -= 1
                elif units == '':
                    i_header += 1
                continue
            elif i == i_header + 1:
                title_name = parse_title_name(tds)
                continue
            elif i <= i_header + col_height:
                continue
            if check_empty_row(tds, n_col):
                continue

            c = re.compile(r'\s*其中：?')
            if c.match(parse_html_tag(tds[0], True)) is not None:
                continue

            item = item_initializer()
            item['report_year'] = year
            item['report_month'] = month
            item['currency'] = currency
            item['units'] = units
            item['title_name'] = title_name
            item['idx'] = i_row
            i_row += 1
            for j, td_html in enumerate(tds):
                td_str = parse_html_tag(td_html, True)
                if j == 0:
                    item['title'] = td_str
                elif j == 1:
                    item['measurement_units'] = td_str
                else:
                    item[fields[j - row_height]] = parse_value(td_str)
            item['hid'] = self.generate_hid(item)
            yield item

        yield self.generate_log_item(response)

    def parse_table_15_16(self, response):
        title_xpath = '//div[contains(@class,"titTop")]'
        title = response.xpath(title_xpath).extract()[0]
        year, month = parse_title(title)
        if year is None or month is None:
            year = response.meta['YEAR']
            month = response.meta['MONTH']
        currency = response.meta['CURRENCY']
        item_initializer = response.meta['ITEM']
        fields = response.meta['FIELDS']
        col_height, row_height = response.meta['HEADER_HEIGHT']
        units = ''
        title_name = ''
        areas = []
        xpath = '//*[contains(@style,"BORDER-COLLAPSE: collapse")]/tbody/tr'
        i_header, i_row, n_col = 0, 0, 0

        for i, tr in enumerate(response.xpath(xpath)):
            tds = tr.xpath('td').extract()
            n_col = max(n_col, len(tds))
            if i == i_header:
                test_title, _ = parse_title(tds[0])
                if test_title is not None:
                    i_header += 1
                    continue
                units = parse_units(tds)
                if units is None:
                    title_name = parse_title_name(tds)
                    areas = parse_all_title(tds)
                    i_header -= 1
                elif units == '':
                    i_header += 1
                continue
            elif i == i_header + 1:
                title_name = parse_title_name(tds)
                areas = parse_all_title(tds)
                continue
            elif i <= i_header + col_height:
                continue
            if check_empty_row(tds, n_col):
                continue

            title = ''
            i_row += 1
            for j, td_html in enumerate(tds):
                td_str = parse_html_tag(td_html, True)
                if j == 0:
                    title = td_str
                elif (j - row_height) % 2 == 0:
                    item = item_initializer()
                    item['report_year'] = year
                    item['report_month'] = month
                    item['currency'] = currency
                    item['units'] = units
                    item['title'] = title
                    item['title_name'] = title_name
                    item['idx'] = i_row
                    item['area'] = areas[j // 2]
                    item[fields[0]] = parse_value(td_str)
                else:
                    item[fields[1]] = parse_value(td_str)
                    item['hid'] = self.generate_hid(item)
                    yield item

        yield self.generate_log_item(response)

    def generate_hid(self, item):
        keys = list(item.fields.keys())
        try:
            keys.remove('hid')
        except ValueError:
            pass
        keys.sort()

        m = hashlib.md5()
        str_type = type('')
        hash_strs = []
        for key in keys:
            if item[key] is None:
                hash_strs.append('-')
            elif isinstance(item[key], str_type):
                hash_strs.append(item[key])
            else:
                hash_strs.append(str(item[key]))
        hash_str = '|'.join(hash_strs)
        m.update(hash_str.encode())
        hid = m.hexdigest()
        return hid

    def generate_log_item(self, response):
        m = hashlib.md5()
        m.update(response.url.encode())
        hid = m.hexdigest()
        item = CrawlLogItem()
        item['url'] = response.url
        item['hid'] = hid
        return item


def parse_table_name(s):
    c = re.compile(r'[\(（]\d+[\)）](\d{4}年?).+')
    m = c.search(s)
    if m is None:
        return s
    return s.replace(m.group(1), '')


def parse_currency(s):
    c = re.compile(r'[\(（](.+)[\)）]')
    m = c.search(s)
    if m is None:
        return None
    return m.group(1).replace(' ', '')


def parse_month(s):
    c = re.compile(r'(\d{1,2})月?')
    m = c.search(s)
    if m is None:
        return None
    return m.group(1)


def parse_title(s):
    if s is None or s == '':
        return None, None
    w = '(\d{4})年(\d{1,2})月'
    m = re.search(w, s)
    if m is None:
        return None, None
    return m.group(1), m.group(2)


def parse_html_tag(s, parse_all=False):
    c = re.compile(
        r'<(?P<tag>[0-9A-Za-z_]+)\s?.*?>\s*(?P<value>.*?)\s*</(?P=tag)>')
    s1 = s.replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ')
    m = c.search(s1)
    if m is None:
        return s
    elif parse_all:
        return parse_html_tag(m.group('value'), True)
    else:
        return m.group('value').strip()


def parse_units(tds):
    if len(tds) == 0:
        return ''

    units_html = tds[-1]
    units_str = parse_html_tag(units_html, True)
    if units_str == '':
        return ''

    c = re.compile(r'^\s*单位[：:](.+)')
    m = c.match(units_str)
    if m is None:
        return None

    units = m.group(1).strip()
    return units


def parse_title_name(tds):
    if len(tds) == 0:
        return ''

    title_html = tds[0]
    title_name = parse_html_tag(title_html, True)
    title_name = title_name.strip()
    title_name = title_name.replace('\xa0', ' ')
    return title_name


def parse_all_title(tds):
    titles = []
    if len(tds) < 2:
        return None

    titles = [parse_html_tag(td, True) for td in tds[1:]]
    return titles


def parse_value(s):
    if s.strip() == '-':
        return None
    elif s.find('#') >= 0:
        return None
    else:
        return atof(s)


def check_empty_row(tds, n_col):
    ''' 检查是否为空行，包括tr为None，tr中没有td，首td字段为空三种情况
    '''
    if len(tds) <= 0 or len(tds) < n_col // 2:
        return True
    header = parse_html_tag(tds[0], True)
    if check_empty_str(header):
        return True
    elif header == '-':
        return True

    count = 0
    for i, td in enumerate(tds):
        if i == 0:
            continue
        if check_empty_str(parse_html_tag(tds[i], True)):
            count += 1
    if count == len(tds) - 1:
        return True

    return False


def check_empty_str(s):
    if s is None:
        return True
    s = s.strip()
    if s == '':
        return True
    elif s.startswith('\u3000'):
        return True
    elif s.startswith('\xa0'):
        return True
    elif s.startswith('<br>'):
        return True
    else:
        return False
