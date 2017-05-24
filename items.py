# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlLogItem(scrapy.Item):
    hid = scrapy.Field()
    url = scrapy.Field()


class CustomsStatTable1aItem(scrapy.Item):
    # define the fields for your item here like:
    hid = scrapy.Field()
    report_year = scrapy.Field()
    report_month = scrapy.Field()
    currency = scrapy.Field()
    units = scrapy.Field()
    idx = scrapy.Field()
    title = scrapy.Field()
    title_name = scrapy.Field()
    imp_exp = scrapy.Field()
    exp = scrapy.Field()
    imp = scrapy.Field()
    balance = scrapy.Field()
    yoy_imp_exp = scrapy.Field()
    yoy_exp = scrapy.Field()
    yoy_imp = scrapy.Field()


class CustomsStatTable1bItem(scrapy.Item):
    # define the fields for your item here like:
    hid = scrapy.Field()
    report_year = scrapy.Field()
    report_month = scrapy.Field()
    currency = scrapy.Field()
    units = scrapy.Field()
    idx = scrapy.Field()
    title = scrapy.Field()
    title_name = scrapy.Field()
    imp_exp = scrapy.Field()
    exp = scrapy.Field()
    imp = scrapy.Field()
    balance = scrapy.Field()
    ytd_imp_exp = scrapy.Field()
    ytd_exp = scrapy.Field()
    ytd_imp = scrapy.Field()
    ytd_balance = scrapy.Field()


class CustomsStatTable2Item(scrapy.Item):
    # define the fields for your item here like:
    hid = scrapy.Field()
    report_year = scrapy.Field()
    report_month = scrapy.Field()
    currency = scrapy.Field()
    units = scrapy.Field()
    idx = scrapy.Field()
    title = scrapy.Field()
    title_name = scrapy.Field()
    imp_exp = scrapy.Field()
    ytd_imp_exp = scrapy.Field()
    exp = scrapy.Field()
    ytd_exp = scrapy.Field()
    imp = scrapy.Field()
    ytd_imp = scrapy.Field()
    yoy_ytd_imp_exp = scrapy.Field()
    yoy_ytd_exp = scrapy.Field()
    yoy_ytd_imp = scrapy.Field()


class CustomsStatTable3Item(scrapy.Item):
    # define the fields for your item here like:
    hid = scrapy.Field()
    report_year = scrapy.Field()
    report_month = scrapy.Field()
    currency = scrapy.Field()
    units = scrapy.Field()
    idx = scrapy.Field()
    title = scrapy.Field()
    title_name = scrapy.Field()
    exp = scrapy.Field()
    imp = scrapy.Field()
    ytd_exp = scrapy.Field()
    ytd_imp = scrapy.Field()
    yoy_ytd_exp = scrapy.Field()
    yoy_ytd_imp = scrapy.Field()


class CustomsStatTable4Item(scrapy.Item):
    # define the fields for your item here like:
    hid = scrapy.Field()
    report_year = scrapy.Field()
    report_month = scrapy.Field()
    currency = scrapy.Field()
    units = scrapy.Field()
    idx = scrapy.Field()
    title = scrapy.Field()
    title_name = scrapy.Field()
    exp = scrapy.Field()
    imp = scrapy.Field()
    ytd_exp = scrapy.Field()
    ytd_imp = scrapy.Field()
    yoy_ytd_exp = scrapy.Field()
    yoy_ytd_imp = scrapy.Field()


class CustomsStatTable5Item(scrapy.Item):
    # define the fields for your item here like:
    hid = scrapy.Field()
    report_year = scrapy.Field()
    report_month = scrapy.Field()
    currency = scrapy.Field()
    units = scrapy.Field()
    idx = scrapy.Field()
    title = scrapy.Field()
    title_name = scrapy.Field()
    imp_exp = scrapy.Field()
    exp = scrapy.Field()
    imp = scrapy.Field()
    ytd_imp_exp = scrapy.Field()
    ytd_exp = scrapy.Field()
    ytd_imp = scrapy.Field()
    yoy_imp_exp = scrapy.Field()
    yoy_exp = scrapy.Field()
    yoy_imp = scrapy.Field()
    yoy_ytd_imp_exp = scrapy.Field()
    yoy_ytd_exp = scrapy.Field()
    yoy_ytd_imp = scrapy.Field()


class CustomsStatTable6Item(scrapy.Item):
    # define the fields for your item here like:
    hid = scrapy.Field()
    report_year = scrapy.Field()
    report_month = scrapy.Field()
    currency = scrapy.Field()
    units = scrapy.Field()
    idx = scrapy.Field()
    title = scrapy.Field()
    title_name = scrapy.Field()
    sum_val = scrapy.Field()
    sum_yoy = scrapy.Field()
    soe_val = scrapy.Field()  # State-owned Enterprices
    soe_yoy = scrapy.Field()
    fie_subtotal_val = scrapy.Field()  # Foreign Invested Enterprices
    fie_subtotal_yoy = scrapy.Field()
    fie_ce_val = scrapy.Field()  # Cooperative Enterprises
    fie_ce_yoy = scrapy.Field()
    fie_jv_val = scrapy.Field()  # Joint Ventures
    fie_jv_yoy = scrapy.Field()
    fie_foe_val = scrapy.Field()  # Foreign-owned Enterprices
    fie_foe_yoy = scrapy.Field()
    pe_val = scrapy.Field()  # Private Enterprices
    pe_yoy = scrapy.Field()
    other_val = scrapy.Field()  # Others
    other_yoy = scrapy.Field()


class CustomsStatTable7Item(scrapy.Item):
    # define the fields for your item here like:
    hid = scrapy.Field()
    report_year = scrapy.Field()
    report_month = scrapy.Field()
    currency = scrapy.Field()
    units = scrapy.Field()
    idx = scrapy.Field()
    title = scrapy.Field()
    title_name = scrapy.Field()
    sum_val = scrapy.Field()
    sum_yoy = scrapy.Field()
    soe_val = scrapy.Field()  # State-owned Enterprices
    soe_yoy = scrapy.Field()
    fie_subtotal_val = scrapy.Field()  # Foreign Invested Enterprices
    fie_subtotal_yoy = scrapy.Field()
    fie_ce_val = scrapy.Field()  # Cooperative Enterprises
    fie_ce_yoy = scrapy.Field()
    fie_jv_val = scrapy.Field()  # Joint Ventures
    fie_jv_yoy = scrapy.Field()
    fie_foe_val = scrapy.Field()  # Foreign-owned Enterprices
    fie_foe_yoy = scrapy.Field()
    pe_val = scrapy.Field()  # Private Enterprices
    pe_yoy = scrapy.Field()
    other_val = scrapy.Field()  # Others
    other_yoy = scrapy.Field()


class CustomsStatTable8Item(scrapy.Item):
    # define the fields for your item here like:
    hid = scrapy.Field()
    report_year = scrapy.Field()
    report_month = scrapy.Field()
    currency = scrapy.Field()
    units = scrapy.Field()
    idx = scrapy.Field()
    title = scrapy.Field()
    title_name = scrapy.Field()
    imp_exp = scrapy.Field()
    exp = scrapy.Field()
    imp = scrapy.Field()
    ytd_imp_exp = scrapy.Field()
    ytd_exp = scrapy.Field()
    ytd_imp = scrapy.Field()
    yoy_ytd_imp_exp = scrapy.Field()
    yoy_ytd_exp = scrapy.Field()
    yoy_ytd_imp = scrapy.Field()


class CustomsStatTable9Item(scrapy.Item):
    # define the fields for your item here like:
    hid = scrapy.Field()
    report_year = scrapy.Field()
    report_month = scrapy.Field()
    currency = scrapy.Field()
    units = scrapy.Field()
    idx = scrapy.Field()
    title = scrapy.Field()
    title_name = scrapy.Field()
    imp_exp = scrapy.Field()
    exp = scrapy.Field()
    imp = scrapy.Field()
    ytd_imp_exp = scrapy.Field()
    ytd_exp = scrapy.Field()
    ytd_imp = scrapy.Field()
    yoy_ytd_imp_exp = scrapy.Field()
    yoy_ytd_exp = scrapy.Field()
    yoy_ytd_imp = scrapy.Field()


class CustomsStatTable10Item(scrapy.Item):
    # define the fields for your item here like:
    hid = scrapy.Field()
    report_year = scrapy.Field()
    report_month = scrapy.Field()
    currency = scrapy.Field()
    units = scrapy.Field()
    idx = scrapy.Field()
    title = scrapy.Field()
    title_name = scrapy.Field()
    imp_exp = scrapy.Field()
    exp = scrapy.Field()
    imp = scrapy.Field()
    ytd_imp_exp = scrapy.Field()
    ytd_exp = scrapy.Field()
    ytd_imp = scrapy.Field()
    yoy_ytd_imp_exp = scrapy.Field()
    yoy_ytd_exp = scrapy.Field()
    yoy_ytd_imp = scrapy.Field()


class CustomsStatTable11Item(scrapy.Item):
    # define the fields for your item here like:
    hid = scrapy.Field()
    report_year = scrapy.Field()
    report_month = scrapy.Field()
    currency = scrapy.Field()
    units = scrapy.Field()
    idx = scrapy.Field()
    title = scrapy.Field()
    title_name = scrapy.Field()
    imp_exp = scrapy.Field()
    exp = scrapy.Field()
    imp = scrapy.Field()
    ytd_imp_exp = scrapy.Field()
    ytd_exp = scrapy.Field()
    ytd_imp = scrapy.Field()
    yoy_ytd_imp_exp = scrapy.Field()
    yoy_ytd_exp = scrapy.Field()
    yoy_ytd_imp = scrapy.Field()


class CustomsStatTable12Item(scrapy.Item):
    # define the fields for your item here like:
    hid = scrapy.Field()
    report_year = scrapy.Field()
    report_month = scrapy.Field()
    currency = scrapy.Field()
    units = scrapy.Field()
    idx = scrapy.Field()
    title = scrapy.Field()
    title_name = scrapy.Field()
    province = scrapy.Field()
    imp_exp = scrapy.Field()
    exp = scrapy.Field()
    imp = scrapy.Field()
    ytd_imp_exp = scrapy.Field()
    ytd_exp = scrapy.Field()
    ytd_imp = scrapy.Field()
    yoy_ytd_imp_exp = scrapy.Field()
    yoy_ytd_exp = scrapy.Field()
    yoy_ytd_imp = scrapy.Field()


class CustomsStatTable13Item(scrapy.Item):
    # define the fields for your item here like:
    hid = scrapy.Field()
    report_year = scrapy.Field()
    report_month = scrapy.Field()
    currency = scrapy.Field()
    units = scrapy.Field()
    idx = scrapy.Field()
    title = scrapy.Field()
    title_name = scrapy.Field()
    measurement_units = scrapy.Field()
    quantity = scrapy.Field()
    amount = scrapy.Field()
    quantity_ytd = scrapy.Field()
    amount_ytd = scrapy.Field()
    quantity_yoy = scrapy.Field()
    amount_yoy = scrapy.Field()
    quantity_ytd_yoy = scrapy.Field()
    amount_ytd_yoy = scrapy.Field()


class CustomsStatTable14Item(scrapy.Item):
    # define the fields for your item here like:
    hid = scrapy.Field()
    report_year = scrapy.Field()
    report_month = scrapy.Field()
    currency = scrapy.Field()
    units = scrapy.Field()
    idx = scrapy.Field()
    title = scrapy.Field()
    title_name = scrapy.Field()
    measurement_units = scrapy.Field()
    quantity = scrapy.Field()
    amount = scrapy.Field()
    quantity_ytd = scrapy.Field()
    amount_ytd = scrapy.Field()
    quantity_yoy = scrapy.Field()
    amount_yoy = scrapy.Field()
    quantity_ytd_yoy = scrapy.Field()
    amount_ytd_yoy = scrapy.Field()


class CustomsStatTable15Item(scrapy.Item):
    # define the fields for your item here like:
    hid = scrapy.Field()
    report_year = scrapy.Field()
    report_month = scrapy.Field()
    currency = scrapy.Field()
    units = scrapy.Field()
    idx = scrapy.Field()
    title = scrapy.Field()
    title_name = scrapy.Field()
    area = scrapy.Field()
    amount = scrapy.Field()
    amount_ytd = scrapy.Field()


class CustomsStatTable16Item(scrapy.Item):
    # define the fields for your item here like:
    hid = scrapy.Field()
    report_year = scrapy.Field()
    report_month = scrapy.Field()
    currency = scrapy.Field()
    units = scrapy.Field()
    idx = scrapy.Field()
    title = scrapy.Field()
    title_name = scrapy.Field()
    area = scrapy.Field()
    amount = scrapy.Field()
    amount_ytd = scrapy.Field()
