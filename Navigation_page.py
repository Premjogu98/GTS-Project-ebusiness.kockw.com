from selenium import webdriver
import time
from datetime import datetime
import Global_var
import sys, os
import ctypes
import string
from Insert_On_Datbase import insert_in_Local
import html
import wx
app = wx.App()

def ChromeDriver():
    browser = webdriver.Chrome(executable_path='C:\\chromedriver.exe')
    browser.get('https://ebusiness.kockw.com/')
    browser.maximize_window()
    time.sleep(2)
    list_of_url = ['https://ebusiness.kockw.com/Tenders/Published?tenderType=3','https://ebusiness.kockw.com/RFQ/Issued']
    link = 1
    for href in list_of_url:
        browser.get(href)
        time.sleep(2)
        for From_Date in browser.find_elements_by_id('filterFromIssue'):
            From_Date.send_keys(str(Global_var.From_Date))
            time.sleep(1)
            break
        for To_Date in browser.find_elements_by_id('filterToIssue'):
            To_Date.send_keys(str(Global_var.todate))
            time.sleep(1)
            break
        for search in browser.find_elements_by_id('search'):
            search.click()
            time.sleep(2)
            break
        if link == 1:
            scrap_link1(browser)
            link += 1
        else:
            scrap_link2(browser)
    wx.MessageBox(f'Total: {Global_var.Total}\nDeadline Not given: {Global_var.deadline_Not_given}\nduplicate: {Global_var.duplicate}\ninserted: {Global_var.inserted}\nexpired: {Global_var.expired}\nQC Tenders: {Global_var.QC_Tender}','ebusiness.kockw.com', wx.OK | wx.ICON_INFORMATION)
    browser.close()
    sys.exit()

def scrap_link1(browser):
    pagination = False
    for pagination_is_there in browser.find_elements_by_xpath('//*[@id="myPagerId"]/span/ul/li'):
        pagination = True
        break
    tr_count = 1
    next_page = True
    while next_page == True:
        next_page = False
        for tr in browser.find_elements_by_xpath('//*[@id="grid"]/table/tbody/tr'):
            MyLoop = 0
            while MyLoop == 0:
                try:
                    SegField = []
                    for data in range(42):
                        SegField.append('')
                    for tender_id in browser.find_elements_by_xpath(f'//*[@id="grid"]/table/tbody/tr[{str(tr_count)}]/td[3]'):
                        tender_id = tender_id.get_attribute('innerText')
                        SegField[13] = tender_id.strip()
                        break
                    for Title in browser.find_elements_by_xpath(f'//*[@id="grid"]/table/tbody/tr[{str(tr_count)}]/td[4]'):
                        Title = Title.get_attribute('innerText').strip()
                        SegField[19] = Title.strip()
                        SegField[18] += f'{SegField[19]}'
                        break
                    for Brief_Description in browser.find_elements_by_xpath(f'//*[@id="grid"]/table/tbody/tr[{str(tr_count)}]/td[5]'):
                        Brief_Description = Brief_Description.get_attribute('innerText').strip()
                        SegField[18] += f'<br>\nBrief Description: {Brief_Description}'
                        break
                    for Category in browser.find_elements_by_xpath(f'//*[@id="grid"]/table/tbody/tr[{str(tr_count)}]/td[6]'):
                        Category = Category.get_attribute('innerText').strip()
                        SegField[18] += f'<br>\nCategory: {Category}'
                        break
                    for Issue_Date in browser.find_elements_by_xpath(f'//*[@id="grid"]/table/tbody/tr[{str(tr_count)}]/td[7]'):
                        Issue_Date = Issue_Date.get_attribute('innerText').strip()
                        SegField[18] += f'<br>\nIssue Date: {Issue_Date}'
                        break
                    for PTM_Date in browser.find_elements_by_xpath(f'//*[@id="grid"]/table/tbody/tr[{str(tr_count)}]/td[8]'):
                        PTM_Date = PTM_Date.get_attribute('innerText').strip()
                        SegField[18] += f'<br>\nPTM Date: {PTM_Date}'
                        break
                    for deadline in browser.find_elements_by_xpath(f'//*[@id="grid"]/table/tbody/tr[{str(tr_count)}]/td[9]'):
                        deadline = deadline.get_attribute('innerText').strip()
                        if deadline != "":
                            deadline = datetime.strptime(str(deadline).strip(), "%d/%m/%Y")
                            deadline = deadline.strftime("%Y-%m-%d")
                            SegField[24] = deadline.strip()
                        break
                    visible = True
                    while visible == True:
                        try:
                            for more_detail_tab in browser.find_elements_by_xpath(f'/html/body/div[7]/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div/table/tbody/tr[{str(tr_count)}]/td[10]/i'):
                                browser.execute_script("arguments[0].scrollIntoView();", more_detail_tab)
                                more_detail_tab.click()
                                time.sleep(2)
                                visible = False
                                break
                        except:
                            visible = True
                            wx.MessageBox(' Scroll To element ','ebusiness.kockw.com', wx.OK | wx.ICON_ERROR)
                            browser.execute_script("arguments[0].scrollIntoView();", more_detail_tab)
                            time.sleep(1)
                            
                    for publishedDocsNo in browser.find_elements_by_id('publishedDocsNo'):
                        publishedDocsNo = publishedDocsNo.get_attribute('outerHTML').strip()
                        publishedDocsNo = publishedDocsNo.partition('value="')[2].partition('">')[0].strip()
                        publishedDocsNo = string.capwords(str(publishedDocsNo))
                        SegField[18] += f'<br>\nNumber of Published Documents: {publishedDocsNo}'
                        break
                    for Currency in browser.find_elements_by_id('RFP_CURRENCYCODE'):
                        Currency = Currency.get_attribute('outerHTML').strip()
                        Currency = Currency.partition('value="')[2].partition('">')[0].strip()
                        Currency = string.capwords(str(Currency))
                        SegField[18] += f'<br>\nCurrency: {Currency}'
                        break
                    get_htmlsource = ''
                    for AjaxAntiForgeryForm in browser.find_elements_by_id('__AjaxAntiForgeryForm'):
                        AjaxAntiForgeryForm = AjaxAntiForgeryForm.get_attribute('outerHTML').strip()
                        get_htmlsource += AjaxAntiForgeryForm
                        break
                    for page_body_htmlsource in browser.find_elements_by_class_name('page-body'):
                        page_body_htmlsource = page_body_htmlsource.get_attribute('outerHTML').strip()
                        get_htmlsource += page_body_htmlsource
                        break
                    for submitId in browser.find_elements_by_id('submitId'):
                        submitId = submitId.get_attribute('outerHTML').strip()
                        get_htmlsource = get_htmlsource.replace(str(submitId),'')
                        break
                    for tabbable in browser.find_elements_by_class_name('tabbable'):
                        tabbable = tabbable.get_attribute('outerHTML').strip()
                        get_htmlsource = get_htmlsource.replace(str(tabbable),'')
                        break
                    for alert_dismissable in browser.find_elements_by_xpath('//*[@class="alert alert-info alert-dismissable"]'):
                        alert_dismissable = alert_dismissable.get_attribute('outerHTML').strip().replace('\n','')
                        get_htmlsource = get_htmlsource.replace(str(alert_dismissable),'')
                        break
                    get_htmlsource = get_htmlsource.replace('href="/','href="https://ebusiness.kockw.com/').replace('action="/','action="https://ebusiness.kockw.com/')
                    SegField[1] = 'kocinfo@kockw.com'
                    SegField[2] = 'P.O. Box 9758 Ahmadi, 61008 Ahmadi, Kuwait, Tel: 00965 - 23989111, Fax: 00965 – 23983661'
                    SegField[12] = 'Kwait Oil Company'.upper()
                    SegField[14] = '2'
                    SegField[22] = "0"
                    SegField[26] = "0.0"
                    SegField[27] = "0" 
                    SegField[7] = 'KW'
                    SegField[8] = 'www.kockw.com'
                    SegField[28] = 'https://ebusiness.kockw.com/Tenders/Published?tenderType=3'
                    SegField[31] = 'ebusiness.kockw.com'
                    for SegIndex in range(len(SegField)):
                        print(SegIndex, end=' ')
                        print(SegField[SegIndex])
                        SegField[SegIndex] = html.unescape(str(SegField[SegIndex]))
                        SegField[SegIndex] = str(SegField[SegIndex]).replace("'", "''")

                    if len(SegField[19]) >= 200:
                        SegField[19] = str(SegField[19])[:200]+'...'

                    if len(SegField[18]) >= 1500:
                        SegField[18] = str(SegField[18])[:1500]+'...'

                    if SegField[19] == '':
                        wx.MessageBox(' Short Desc Blank ','ebusiness.kockw.com', wx.OK | wx.ICON_ERROR)
                    else:
                        check_date(get_htmlsource, SegField)
                        Global_var.Total += 1
                        print(f'Total: {Global_var.Total} Deadline Not given: {Global_var.deadline_Not_given} duplicate: {Global_var.duplicate} inserted: {Global_var.inserted} expired: {Global_var.expired} QC Tenders: {Global_var.QC_Tender}')
                    browser.back()
                    tr_count += 1
                    MyLoop = 1
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,"\n", exc_tb.tb_lineno)
                    MyLoop = 0
                    time.sleep(3)
            
        if pagination == True:
            a = True
            while a == True:
                try:
                    for nextpage in browser.find_elements_by_xpath('//*[@id="myPagerId"]/span/ul/li[3]/a'):
                        for header in browser.find_elements_by_xpath('//*[@id="widget-header"]'):
                            browser.execute_script("arguments[0].scrollIntoView();", header)
                            break
                        nextpagetext = nextpage.get_attribute('innerText').strip()
                        if nextpagetext == '>':
                            nextpage.click()
                            next_page = True
                            tr_count = 1
                            time.sleep(2)
                            a = False
                        else:
                            a = False
                except:
                    print('Scarp 1 Error On Next Page')
                    time.sleep(3)
                    a = True
def scrap_link2(browser):
    pagination = False
    for pagination_is_there in browser.find_elements_by_xpath('//*[@id="myPagerId"]/span/ul/li'):
        pagination = True
        break
    tr_count = 1
    next_page_li = 6
    next_page = True
    while next_page == True:
        next_page = False
        for tr in browser.find_elements_by_xpath('//*[@id="grid"]/table/tbody/tr'):
            MyLoop = 0
            while MyLoop == 0:
                try:
                    SegField = []
                    for data in range(42):
                        SegField.append('')
                    for tender_id in browser.find_elements_by_xpath(f'//*[@id="grid"]/table/tbody/tr[{str(tr_count)}]/td[3]'):
                        tender_id = tender_id.get_attribute('innerText')
                        SegField[13] = tender_id.strip()
                        break
                    for Title in browser.find_elements_by_xpath(f'//*[@id="grid"]/table/tbody/tr[{str(tr_count)}]/td[4]'):
                        Title = Title.get_attribute('innerText').strip()
                        SegField[19] = Title.strip()
                        SegField[18] += f'{SegField[19]}'
                        break
                    for Commodity_Group in browser.find_elements_by_xpath(f'//*[@id="grid"]/table/tbody/tr[{str(tr_count)}]/td[5]'):
                        Commodity_Group = Commodity_Group.get_attribute('innerText').strip()
                        SegField[18] += f'<br>\nCommodity Group: {Commodity_Group}'
                        break
                    
                    for TenderFeeRequired in browser.find_elements_by_xpath(f'//*[@id="grid"]/table/tbody/tr[{str(tr_count)}]/td[6]'):
                        TenderFeeRequired = TenderFeeRequired.get_attribute('innerText').strip()
                        SegField[18] += f'<br>\nTender Fee Required: {TenderFeeRequired}'
                        break
                    for Issue_Date in browser.find_elements_by_xpath(f'//*[@id="grid"]/table/tbody/tr[{str(tr_count)}]/td[7]'):
                        Issue_Date = Issue_Date.get_attribute('innerText').strip()
                        SegField[18] += f'<br>\nIssue Date: {Issue_Date}'
                        break
                    for deadline in browser.find_elements_by_xpath(f'//*[@id="grid"]/table/tbody/tr[{str(tr_count)}]/td[8]'):
                        deadline = deadline.get_attribute('innerText').strip()
                        if deadline != "":
                            deadline = datetime.strptime(str(deadline).strip(), "%d/%m/%Y")
                            deadline = deadline.strftime("%Y-%m-%d")
                            SegField[24] = deadline.strip()
                        break
                    
                    visible = True
                    while visible == True:
                        try:
                            for more_detail_tab in browser.find_elements_by_xpath(f'//*[@id="grid"]/table/tbody/tr[{str(tr_count)}]/td[9]/i'):
                                browser.execute_script("arguments[0].scrollIntoView();", more_detail_tab)
                                more_detail_tab.click()
                                time.sleep(2)
                                visible = False
                                break
                        except:
                            visible = True
                            wx.MessageBox(' Scroll To element ','ebusiness.kockw.com', wx.OK | wx.ICON_ERROR)
                            browser.execute_script("arguments[0].scrollIntoView();", more_detail_tab)
                            time.sleep(1)
                    for Description in browser.find_elements_by_id('RFQ_TITLE'):
                        Description = Description.get_attribute('outerHTML').strip()
                        Description = Description.partition('">')[2].partition('</textarea>')[0].strip()
                        Description = string.capwords(str(Description))
                        SegField[18] += f'<br>\nDescription: {Description}'
                        break
                    for Currency in browser.find_elements_by_id('RFQ_CURRENCYCODE'):
                        Currency = Currency.get_attribute('outerHTML').strip()
                        Currency = Currency.partition('value="')[2].partition('">')[0].strip()
                        Currency = string.capwords(str(Currency))
                        SegField[18] += f'<br>\nCurrency: {Currency}'
                        break
                    get_htmlsource = ''
                    for AjaxAntiForgeryForm in browser.find_elements_by_id('__AjaxAntiForgeryForm'):
                        AjaxAntiForgeryForm = AjaxAntiForgeryForm.get_attribute('outerHTML').strip()
                        get_htmlsource += AjaxAntiForgeryForm.replace('\n','')
                        break
                    for page_body_htmlsource in browser.find_elements_by_class_name('page-body'):
                        page_body_htmlsource = page_body_htmlsource.get_attribute('outerHTML').strip()
                        get_htmlsource += page_body_htmlsource.replace('\n','')
                        break
                    for submitId in browser.find_elements_by_id('submitId'):
                        submitId = submitId.get_attribute('outerHTML').strip()
                        get_htmlsource = get_htmlsource.replace(str(submitId),'').replace('\n','')
                        break
                    for tabbable in browser.find_elements_by_class_name('tabbable'):
                        tabbable = tabbable.get_attribute('outerHTML').strip()
                        get_htmlsource = get_htmlsource.replace(str(tabbable),'').replace('\n','')
                        break
                    for alert_dismissable in browser.find_elements_by_xpath('//*[@class="alert alert-info alert-dismissable"]'):
                        alert_dismissable = alert_dismissable.get_attribute('outerHTML').strip()
                        get_htmlsource = get_htmlsource.replace(str(alert_dismissable),'').replace('\n','')
                        break
                    get_htmlsource = get_htmlsource.replace('href="/','href="https://ebusiness.kockw.com/').replace('action="/','action="https://ebusiness.kockw.com/')
                    SegField[1] = 'kocinfo@kockw.com'
                    SegField[2] = 'P.O. Box 9758 Ahmadi, 61008 Ahmadi, Kuwait, Tel: 00965 - 23989111, Fax: 00965 – 23983661'
                    SegField[12] = 'Kwait Oil Company'.upper()
                    SegField[14] = '2'
                    SegField[22] = "0"
                    SegField[26] = "0.0"
                    SegField[27] = "0" 
                    SegField[7] = 'KW'
                    SegField[8] = 'www.kockw.com'
                    SegField[28] = 'https://ebusiness.kockw.com/RFQ/Issued'
                    SegField[31] = 'ebusiness.kockw.com'
                    for SegIndex in range(len(SegField)):
                        print(SegIndex, end=' ')
                        print(SegField[SegIndex])
                        SegField[SegIndex] = html.unescape(str(SegField[SegIndex]))
                        SegField[SegIndex] = str(SegField[SegIndex]).replace("'", "''")

                    if len(SegField[19]) >= 200:
                        SegField[19] = str(SegField[19])[:200]+'...'

                    if len(SegField[18]) >= 1500:
                        SegField[18] = str(SegField[18])[:1500]+'...'

                    if SegField[19] == '':
                        wx.MessageBox(' Short Desc Blank ','ebusiness.kockw.com', wx.OK | wx.ICON_ERROR)
                    else:
                        check_date(get_htmlsource, SegField)
                        Global_var.Total += 1
                        print(f'Total: {Global_var.Total} Deadline Not given: {Global_var.deadline_Not_given} duplicate: {Global_var.duplicate} inserted: {Global_var.inserted} expired: {Global_var.expired} QC Tenders: {Global_var.QC_Tender}')
                    time.sleep(5)
                    browser.back()
                    tr_count += 1
                    MyLoop = 1
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,"\n", exc_tb.tb_lineno)
                    MyLoop = 0
            
        if pagination == True:
            a = True
            while a == True:
                try:
                    for nextpage in browser.find_elements_by_xpath(f'//*[@id="myPagerId"]/span/ul/li[{str(next_page_li)}]/a'):
                        try:
                            header = browser.find_elements_by_xpath('//*[@class="widget-header"]')
                            browser.execute_script("arguments[0].scrollIntoView();", header[1])
                        except:
                            pass
                        nextpagetext = nextpage.get_attribute('innerText').strip()
                        if nextpagetext == '>':
                            nextpage.click()
                            next_page = True
                            tr_count = 1
                            next_page_li = 8
                            time.sleep(2)
                            a = False
                        else:
                            a = False
                except:
                    print('Scarp 2 Error On Next Page')
                    time.sleep(3)
                    a = True
def check_date(get_htmlSource, SegField):
    deadline = str(SegField[24])
    curdate = datetime.now()
    curdate_str = curdate.strftime("%Y-%m-%d")
    try:
        if deadline != '':
            datetime_object_deadline = datetime.strptime(deadline, '%Y-%m-%d')
            datetime_object_curdate = datetime.strptime(curdate_str, '%Y-%m-%d')
            timedelta_obj = datetime_object_deadline - datetime_object_curdate
            day = timedelta_obj.days
            if day > 0:
                insert_in_Local(get_htmlSource, SegField)
                # create_filename(get_htmlSource , SegField)
            else:
                print("Expired Tender")
                Global_var.expired += 1
        else:
            print("Deadline Not Given")
            Global_var.deadline_Not_given += 1
            wx.MessageBox(' Deadline Not Given ','ipms.ppadb.co.bw', wx.OK | wx.ICON_INFORMATION)
            # insert_in_Local(get_htmlSource, SegField)
    except Exception as e:
        exc_type , exc_obj , exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error ON : " , sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname , "\n" ,exc_tb.tb_lineno)
ChromeDriver()