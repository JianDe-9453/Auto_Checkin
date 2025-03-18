# 載入日期與時間
import datetime
# 載入檔案操作
import os
# 載入requests
import requests
# 載入日誌管理
import logging

Logging_Format = '%(asctime)s %(levelname)s: %(message)s'
Date_Log = '%Y-%m-%d'
Date_Format = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(level=logging.INFO, filename=f'{datetime.date.today().strftime("%Y%m%d")}_Auto_Checkin.log', filemode='a', format=Logging_Format, datefmt=Date_Format)

class Forum_Stealth_Functions:
    def __init__(self):
        self.Stealth_Url = 'https://cdn.jsdelivr.net/gh/requireCool/stealth.min.js/stealth.min.js'
        self.Stealth_JS = 'stealth.min.js'
        
    def Update_Stealth(self):
        if os.path.exists(self.Stealth_JS):
            Modification_Time = datetime.datetime.fromtimestamp(os.path.getmtime(self.Stealth_JS))
            Time_Gap = (datetime.datetime.now() - Modification_Time).days
            if Time_Gap >= 7:
                logging.info(f"Forum_Stealth, 檢測到{self.Stealth_JS}修改日期超過7天, {self.Stealth_JS}:上次修改日期: {Modification_Time}")
                Response = requests.get(self.Stealth_Url)
                logging.info(f"取得網址: {self.Stealth_Url}")
                if Response.ok:
                    logging.info(f"{self.Stealth_Url}取得網址狀態正常")
                    with open(self.Stealth_JS, "w", encoding='utf-8') as file:
                        file.write(Response.text)
                        logging.info(f"更新{self.Stealth_JS}並寫入資料")
        elif not os.path.exists(self.Stealth_JS):
            logging.info(f"Forum_Stealth, 檢測到 {self.Stealth_JS} 不存在")
            Response = requests.get(self.Stealth_Url)
            logging.info(f"取得網址: {self.Stealth_Url}")
            if Response.ok:
                logging.info(f"{self.Stealth_Url}取得網址狀態正常")
                with open(self.Stealth_JS, "w", encoding='utf-8') as file:
                    file.write(Response.text)
                    logging.info(f"創建{self.Stealth_JS}並寫入資料")

if __name__ == '__main__':
    Forum_Stealth_Functions()