# 載入日期與時間
import datetime
# 載入OCR驗證碼辨識
import ddddocr
# 載入隨機產生User-Agent
from anti_useragent import UserAgent
# 載入此檔案所需自定義py
from Forum_Stealth import Forum_Stealth_Functions
from Forum_Users import Forum_Users_Functions
# 載入處理Json檔案
import json
# 載入檔案操作
import os
# 載入requests
import requests
# 載入自動化網頁瀏覽器操作工具
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
# 載入時間處理
from time import sleep
# 載入日誌管理
import logging
# 載入處理XML檔案
from lxml import etree
# 載入處理XML檔案
import xml.etree.ElementTree as ET
# 載入webdriver管理器
from webdriver_manager.chrome import ChromeDriverManager

Logging_Format = '%(asctime)s %(levelname)s: %(message)s'
Date_Log = '%Y-%m-%d'
Date_Format = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(level=logging.INFO, filename=f'{datetime.date.today().strftime("%Y%m%d")}_Auto_Checkin.log', filemode='a', format=Logging_Format, datefmt=Date_Format)

class Forum_CheckIn_APK_Functions():
    def __init__(self):
        self.APK_URL = 'https://apk.tw/'
        self.APK_URL_FORUM = 'forum.php'
        self.APK_URL_CHECKEND = '&inajax=1&ajaxtarget=my_amupper'
        self.ConfigXml = "Forums_Users.xml"
        self.Forum_Stealth_Functions = Forum_Stealth_Functions()
        self.Forum_Users_Functions = Forum_Users_Functions()
        self.Stealth_JS = 'stealth.min.js'
        
    def APK_CheckIn(self):
        if os.path.exists(self.ConfigXml):
            self.Forum_Users_Functions.Decrypt_Config()
            Users_Tree = ET.parse(self.ConfigXml)
            logging.info(f"Forum_CheckIn, 解析{self.ConfigXml}-進行簽到")
            Users_Root = Users_Tree.getroot()
            for Eles in Users_Root.findall('.//*[.="APK"]..'):
                logging.info(f"Forum_CheckIn, 帳號: {Eles.find('Account').text} 開始進行自動簽到")
                if not Eles.findall('RequestsCookies') and not Eles.findall('Cookies_DateTime') or \
                    (datetime.datetime.now() - datetime.datetime.strptime(Eles.find('Cookies_DateTime').text, '%Y-%m-%d %H:%M:%S')).days > 2:
                    Chrome_Options = webdriver.ChromeOptions()
                    logging.info("Forum_CheckIn, 設定Chrome參數")
                    Chrome_Options.add_argument('--headless')
                    logging.info("Forum_CheckIn, 設定無視窗模式")
                    Chrome_Options.add_argument('--disable-gpu')
                    logging.info("Forum_CheckIn, 禁止用硬體加速模式")
                    Chrome_Options.add_argument('--window-size=1920,1080')
                    logging.info("Forum_CheckIn, 設定視窗解析度為1920,1080")
                    Chrome_Options.add_argument(f"user-agent={UserAgent(platform='windows').random}")
                    logging.info("Forum_CheckIn, 偽造user-agent")
                    Chrome_Options.add_argument('--disable-blink-features=AutomationControlled')
                    logging.info("Forum_CheckIn, 關閉自動測試軟體控制的blink特徵")
                    Chrome_Options.add_experimental_option('useAutomationExtension', False)
                    Chrome_Options.add_experimental_option('excludeSwitches', ['enable-automation'])
                    logging.info("Forum_CheckIn, 關閉Chrome顯示: Chrome目前受到自動測試軟體控制")
                    Chrome_Driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=Chrome_Options)
                    logging.info("Forum_CheckIn, 使用Webdriver開啟Chrome")
                    self.Forum_Stealth_Functions.Update_Stealth()
                    if os.path.exists(self.Stealth_JS):
                        with open(self.Stealth_JS) as file:
                            stealth_JS = file.read()
                        Chrome_Driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': stealth_JS})
                        logging.info(f"Forum_CheckIn, 使用{self.Stealth_JS}隱藏Selenium特徵")
                    elif not os.path.exists(self.Stealth_JS):
                        Chrome_Driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
                        logging.info("Forum_CheckIn, 將WebDriver的特徵變更為undefined navigator")
                    Chrome_Driver.get(f'{self.APK_URL+self.APK_URL_FORUM}')
                    logging.info(f"Forum_CheckIn, 前往 {self.APK_URL+self.APK_URL_FORUM}")
                    try:
                        WebDriverWait(Chrome_Driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, '//a[@class="logb"]')))
                        ActionChains(Chrome_Driver).move_to_element(Chrome_Driver.find_element(By.XPATH, '//a[@class="logb"]')).perform()
                        logging.info("Forum_CheckIn, 使用滑鼠移動到JavaScript登錄")
                        Chrome_Driver.find_element(By.XPATH, '//input[@id="ls_username"]').send_keys(Eles.find('Account').text)
                        logging.info(f"Forum_CheckIn, 輸入帳號: {Eles.find('Account').text}")
                        Chrome_Driver.find_element(By.XPATH, '//input[@id="ls_password"]').send_keys(Eles.find('Password').text)
                        logging.info("Forum_CheckIn, 輸入密碼: {Password}".format(Password='************'))
                        Chrome_Driver.find_element(By.XPATH, '//button[@type="submit"]').click()
                        logging.info("Forum_CheckIn, 使用滑鼠點擊登錄按鈕")
                        WebDriverWait(Chrome_Driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, '//img[starts-with(@onclick, "updateseccode")]')))
                        Captch_Ocr = ddddocr.DdddOcr()
                        
                        while not Chrome_Driver.find_elements(By.XPATH, '//span[starts-with(@id, "checkseccodeverify")]//img[contains(@src, "right.gif")]'):
                            Captcha_Img = Chrome_Driver.find_element(By.XPATH, '//img[starts-with(@onclick, "updateseccode")]').screenshot_as_png
                            logging.info("Forum_CheckIn, 找到驗證碼資訊, 對驗證碼截圖")
                            Captch_Parse = Captch_Ocr.classification(Captcha_Img)
                            logging.info("Forum_CheckIn, 使用OCR對驗證碼進行解析")
                            if len(Captch_Parse) == 0:
                                sleep(0.001)
                                logging.info("Forum_CheckIn, 未正確截圖, 強制等待0.001")
                            elif len(Captch_Parse) > 0 and 4 > len(Captch_Parse):
                                Chrome_Driver.find_element(By.XPATH, '//img[starts-with(@onclick, "updateseccode")]').click()
                                logging.info(f"Forum_CheckIn, 驗證碼解析答案錯誤, 刷新驗證碼 答案: {Captch_Parse}")
                                sleep(0.15)
                                logging.info("Forum_CheckIn, 強制等待0.15秒")
                            elif len(Captch_Parse) == 4:
                                Chrome_Driver.find_element(By.XPATH, '//input[starts-with(@id, "seccodeverify")]').clear()
                                Chrome_Driver.find_element(By.XPATH, '//input[starts-with(@id, "seccodeverify")]').send_keys(Captch_Parse)
                                logging.info(f"Forum_CheckIn, 輸入驗證碼, 驗證碼解析為 {Captch_Parse}")
                                Chrome_Driver.find_element(By.XPATH, '//span[starts-with(@id, "checkseccodeverify")]').click()
                                logging.info("Forum_CheckIn, 使用滑鼠點擊判斷驗證碼是否正確")
                                WebDriverWait(Chrome_Driver, 30).until_not(expected_conditions.presence_of_element_located((By.XPATH, '//span[starts-with(@id, "checkseccodeverify")]//img[contains(@src, "loading.gif")]')))
                                if Chrome_Driver.find_elements(By.XPATH, '//span[starts-with(@id, "checkseccodeverify")]//img[contains(@src, "error.gif")]'):
                                    Chrome_Driver.find_element(By.XPATH, '//img[starts-with(@onclick, "updateseccode")]').click()
                                    logging.info("Forum_CheckIn, 驗證碼解析答案錯誤, 刷新驗證碼")
                                    sleep(0.15)
                                    logging.info("Forum_CheckIn, 強制等待0.15秒")
                        Chrome_Driver.find_element(By.XPATH, '//button[@name="loginsubmit"]').click()
                        WebDriverWait(Chrome_Driver, 120).until_not(expected_conditions.presence_of_element_located((By.XPATH, '//img[starts-with(@onclick, "updateseccode")]')))
                        Selenium_Cookies = {}
                        for Cookie in Chrome_Driver.get_cookies():
                            Selenium_Cookies[Cookie['name']] = Cookie['value']
                        logging.info("Forum_CheckIn, 將Selenium獲取的Cookies轉換成Requests的格式")
                        if Eles.findall('RequestsCookies'):
                            Eles.find('RequestsCookies').text = json.dumps(Selenium_Cookies)
                            logging.info("Forum_CheckIn, RequestsCookies節點已存在, 更新RequestsCookies")
                            Eles.find('Cookies_DateTime').text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            logging.info(f"Forum_CheckIn, Cookies_DateTime節點已存在, 更新Datetime: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                        else:
                            User_Requests = ET.SubElement(Eles, 'RequestsCookies')
                            User_Requests.text = json.dumps(Selenium_Cookies)
                            logging.info("Forum_CheckIn, 建立RequestsCookies節點")
                            User_Cookies_Datetime = ET.SubElement(Eles, 'Cookies_DateTime')
                            User_Cookies_Datetime.text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            logging.info(f"Forum_CheckIn, 建立Cookies_DateTime節點: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                        Users_Tree.write(self.ConfigXml, encoding='utf-8', xml_declaration=True)
                        logging.info(f"Forum_CheckIn, 更新{self.ConfigXml}論壇使用者參數")
                    except TimeoutException as Ex:
                        logging.error(f"Forum_CheckIn, 錯誤: {Ex}")
                    finally:
                        Chrome_Driver.quit()
                        logging.info("Forum_CheckIn, 使用Webdriver結束Chrome")
                
                if Eles.findall('RequestsCookies') and Eles.findall('Cookies_DateTime'):
                    Requests_Session = requests.session()
                    logging.info("Forum_CheckIn, 創建requests.session()")
                    Session_Headers = {'User-Agent': UserAgent(platform='windows').random}
                    logging.info("Forum_CheckIn, 偽造user-agent")
                    Session_Cookies = json.loads(Eles.find('RequestsCookies').text)
                    logging.info("Forum_CheckIn, 載入requests所要帶入的Cookies")
                    Response = Requests_Session.get(f"{self.APK_URL+self.APK_URL_FORUM}", headers=Session_Headers, cookies=Session_Cookies)
                    logging.info(f"Forum_CheckIn, 取得網址: {self.APK_URL+self.APK_URL_FORUM}, 並將Cookies帶入")
                    Reponse_Html = etree.HTML(Response.text.encode())
                    logging.info("Forum_CheckIn, 將網址的原始碼輸出並解析")
                    if Reponse_Html.xpath(f"//a[text()=\"{Eles.find('Account').text}\"]"):
                        logging.info(f"Forum_CheckIn, 帳號: {Eles.find('Account').text} 使用session登入成功")
                        if Reponse_Html.xpath('//img[contains(@src, "dk.gif")]'):
                            logging.info("Forum_CheckIn, 網址未進行簽到, 開始進行簽到")
                            XPath_Onclick_Str = Reponse_Html.xpath('//a[@id="my_amupper"]')[0].attrib['onclick']
                            logging.info("Forum_CheckIn, 使用XPATH並取得OnClick的值")
                            XPath_Onclick_List = XPath_Onclick_Str.split(', ')
                            logging.info("Forum_CheckIn, 分割OnClick的值並轉為List")
                            XPath_Onclick_Str = [I for I in XPath_Onclick_List if 'ajaxget' in I][0]
                            logging.info("Forum_CheckIn, 取得XPath_Onclick_List中有ajaxget再裡面的值")
                            XPath_Onclick_Str = XPath_Onclick_Str.lstrip('ajaxget(\'').rstrip('\'')
                            logging.info("Forum_CheckIn, 將多餘的字串刪除")
                            Requests_Session.get(f'{self.APK_URL+XPath_Onclick_Str+self.APK_URL_CHECKEND}', headers=Session_Headers, cookies=Session_Cookies)
                            logging.info(f"Forum_CheckIn, 取得網址並進行簽到: {self.APK_URL+XPath_Onclick_Str+self.APK_URL_CHECKEND}, 並將Cookies帶入")
                            Response = Requests_Session.get(f"{self.APK_URL+self.APK_URL_FORUM}", headers=Session_Headers, cookies=Session_Cookies)
                            logging.info(f"Forum_CheckIn, 取得網址: {self.APK_URL+self.APK_URL_FORUM}, 並將Cookies帶入")
                            Reponse_Html = etree.HTML(Response.text.encode())
                            logging.info("Forum_CheckIn, 將網址的原始碼輸出並解析")
                            if Reponse_Html.xpath('//img[contains(@src, "wb.gif")]'):
                                logging.info("Forum_CheckIn, 網址簽到完成")
                                if Eles.findall('Cookies_DateTime'):
                                    Eles.find('Cookies_DateTime').text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                    logging.info(f"Forum_CheckIn, Cookies_DateTime節點已存在, 更新Datetime: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                                    Users_Tree.write(self.ConfigXml, encoding='utf-8', xml_declaration=True)
                                    logging.info("Forum_CheckIn, 更新{self.ConfigXml}論壇使用者參數")
                        elif Reponse_Html.xpath('//img[contains(@src, "wb.gif")]'):
                            logging.info("Forum_CheckIn, 網址已簽到過")
                    elif Reponse_Html.xpath('//a[@class="logb"]'):
                        logging.info(f"Forum_CheckIn, 帳號: {Eles.find('Account').text} 使用session未登入")
            self.Forum_Users_Functions.Encrypt_Config()

if __name__ == '__main__':
    Forum_CheckIn_APK_Functions()