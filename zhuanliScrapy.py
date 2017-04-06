#!/usr/bin/env python
# -*- coding:cp936 -*-
import time
import os
import sys
import re
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import tkMessageBox
import xlsxwriter
import datetime
import Tkinter


def getdatafromweb():
    data_status_list = []
    data_sn_list = []
    data_filename_list = []
    data_creator_list = []
    data_created_date_list = []
    data_current_nodename_list = []
    department_name_list = []
    type_invention_list = []
    username = 'yanshuo@inspur.com'
    password = 'patsnapinspur'
    chromedriverpath = os.path.join(os.path.abspath(os.path.curdir), "chromedriver.exe")
    browser = webdriver.Chrome(chromedriverpath)
    url = "http://10.110.6.34/users/login"
    browser.get(url)
    browser.find_element_by_id("UserEmail").send_keys(username)
    browser.find_element_by_id("EmailPassword").send_keys(password)
    browser.find_element_by_css_selector("button.new-login").click()
    time.sleep(3)
    ActionChains(browser).move_to_element(browser.find_element_by_css_selector("li.fl.audit")).perform()
    WebDriverWait(browser, 100).until(ec.element_to_be_clickable((By.XPATH, "//a[@title='������˵�']".decode('gbk'))))
    browser.find_element_by_xpath("//a[@title='������˵�']".decode('gbk')).click()
    time.sleep(3)
    except_list = ['����'.decode('gbk'), '�˻ط�����'.decode('gbk')]
    while True:
        current_table_line = browser.find_elements_by_css_selector("#list-result > div.template-list-condition > div.list-mail-con > table > tbody > tr")
        length_table = len(current_table_line) + 1
        for line_number in range(1, length_table):
            data_status = browser.find_element_by_css_selector("#list-result > div.template-list-condition > div.list-mail-con > table > tbody > tr:nth-child(%d) > td.cos.status > span" % line_number).text
            if data_status not in except_list:
                data_sn_filename_link = browser.find_element_by_css_selector("#list-result > div.template-list-condition > div.list-mail-con > table > tbody > tr:nth-child(%d) > td.cos.subject > a " % line_number)
                data_sn_filename = data_sn_filename_link.text
                data_sn = data_sn_filename.split('/')[0].strip()
                data_filaname = data_sn_filename.split('/')[1].strip()
                data_current_nodename = browser.find_element_by_css_selector("#list-result > div.template-list-condition > div.list-mail-con > table > tbody > tr:nth-child(%d) > td.cos.node_name" % line_number).text.strip()
                data_created_by = browser.find_element_by_css_selector("#list-result > div.template-list-condition > div.list-mail-con > table > tbody > tr:nth-child(%d) > td.cos.created_by" % line_number).text.strip()
                data_created_at_temp = browser.find_element_by_css_selector("#list-result > div.template-list-condition > div.list-mail-con > table > tbody > tr:nth-child(%d) > td.cos.created_at" % line_number).text.strip()
                data_created_at = data_created_at_temp
                data_status_list.append(data_status)
                data_sn_list.append(data_sn)
                data_filename_list.append(data_filaname)
                data_current_nodename_list.append(data_current_nodename)
                data_creator_list.append(data_created_by)
                data_created_date_list.append(data_created_at)
                data_sn_filename_link.click()
                time.sleep(3)
                handles = browser.window_handles
                browser.switch_to.window(handles[1])
                WebDriverWait(browser, 100).until(ec.presence_of_element_located((By.CSS_SELECTOR, '#main > div.major > div.major-section.clearfix > div.content-wrapper.clearfix.layout-detail-main > div.basic-info > div.major-left > div > table > tbody > tr:nth-child(10) > th')))
                try:
                    departmane_name = browser.find_element_by_css_selector("#main > div.major > div.major-section.clearfix > div.content-wrapper.clearfix.layout-detail-main > div.basic-info > div.major-left > div > table > tbody > tr:nth-child(10) > td > a:nth-child(4)").text.strip()
                except selenium.common.exceptions.NoSuchElementException:
                    departmane_name = 'None'
                type_invention = browser.find_element_by_css_selector('#main > div.major > div.major-section.clearfix > div.content-wrapper.clearfix.layout-detail-main > div.basic-info > div.major-left > div > table > tbody > tr:nth-child(6) > td').text.strip()
                department_name_list.append(departmane_name)
                type_invention_list.append(type_invention)
                browser.close()
                browser.switch_to.window(handles[0])
        try:
            next_page = browser.find_element_by_css_selector("#table_page > div > a:nth-child(3)")
            if next_page.text != "��һҳ".decode('gbk'):
                browser.quit()
                break
            else:
                next_page.click()
                time.sleep(3)
        except selenium.common.exceptions.NoSuchElementException:
            browser.quit()
            break

    return data_status_list, data_sn_list, data_filename_list, department_name_list, type_invention_list, data_current_nodename_list, data_creator_list, data_created_date_list


def write_excel(data_status_list, data_sn_list, data_filename_list, department_name_list, type_invention_list, data_current_nodename_list, data_creator_list, data_created_date_list):
    title_sheet = ['��ǰ״̬'.decode('gbk'), '�᰸���'.decode('gbk'), '�᰸����'.decode('gbk'), '����'.decode('gbk'), '��������'.decode('gbk'), '��ǰ�����ڵ�'.decode('gbk'), '������'.decode('gbk'), '����ʱ��'.decode('gbk'), '����ʱ��'.decode('gbk')]
    timestamp = time.strftime('%Y%m%d', time.localtime())
    workbook_display = xlsxwriter.Workbook('������֤��ר������-%s.xlsx'.decode('gbk') % timestamp)
    sheet = workbook_display.add_worksheet('2017���������֤��ר��ͳ��'.decode('gbk'))
    formatOne = workbook_display.add_format()
    formatOne.set_border(1)
    formatTwo = workbook_display.add_format()
    formatTwo.set_border(1)
    formattitle = workbook_display.add_format()
    formattitle.set_border(1)
    formattitle.set_align('center')
    formattitle.set_bg_color("yellow")
    formattitle.set_bold(True)
    sheet.set_column('H:I', 22)
    sheet.set_column('B:B', 14)
    sheet.set_column('C:C', 58)
    sheet.merge_range(0, 0, 0, 8, "������֤��2017����ר������".decode('gbk'), formattitle)
    for index_title, item_title in enumerate(title_sheet):
        sheet.write(1, index_title, item_title, formatOne)
        for index_data, item_data in enumerate(data_sn_list):
            sheet.write(2 + index_data, 0, data_status_list[index_data], formatOne)
            sheet.write(2 + index_data, 1, data_sn_list[index_data], formatOne)
            sheet.write(2 + index_data, 2, data_filename_list[index_data], formatOne)
            sheet.write(2 + index_data, 3, department_name_list[index_data], formatOne)
            sheet.write(2 + index_data, 4, type_invention_list[index_data], formatOne)
            sheet.write(2 + index_data, 5, data_current_nodename_list[index_data], formatOne)
            sheet.write(2 + index_data, 6, data_creator_list[index_data], formatOne)
            sheet.write_datetime(2 + index_data, 7, datetime.datetime.strptime(data_created_date_list[index_data], '%Y/%m/%d %H:%M:%S'), workbook_display.add_format({'num_format': 'yyyy-mm-dd hh:mm:ss', 'border': 1}))
    workbook_display.close()
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
a, b, c, d, e, f, g, h = getdatafromweb()
write_excel(a, b, c, d, e, f, g, h)
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))