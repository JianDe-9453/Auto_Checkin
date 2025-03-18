# 載入日期與時間
import datetime
# 載入此檔案所需自定義py
from Forum_Encryption import Forum_Encryption_Functions
# 載入檔案操作
import os
# 載入日誌管理
import logging
# 載入處理XML檔案
import xml.etree.ElementTree as ET


Logging_Format = '%(asctime)s %(levelname)s: %(message)s'
Date_Log = '%Y-%m-%d'
Date_Format = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(level=logging.INFO, filename=f'{datetime.date.today().strftime("%Y%m%d")}_Auto_Checkin.log', filemode='a', format=Logging_Format, datefmt=Date_Format)

class Forum_Users_Functions():
    def __init__(self):
        self.Key = 
        self.Forum_Encryption_Main = Forum_Encryption_Functions(self.Key)
        self.ConfigXml = "Forums_Users.xml"
        self.Creat_Users()
        
    def Creat_Users(self, Checkin_Froum='', Account='', Password=''):
        if not os.path.exists(self.ConfigXml):
            logging.info("Forum_Users, 檢測到論壇使用者參數不存在")
            Users_Root = ET.Element('Forums_Users')
            logging.info("Forum_Users, 建立Root節點: Forums_Users")
            Users_Tree = ET.ElementTree(Users_Root)
            Users_Tree.write(self.ConfigXml, encoding='utf-8', xml_declaration=True)
            logging.info("Forum_Users, 寫入論壇使用者參數")
            self.Encrypt_Config()
        elif os.path.exists(self.ConfigXml):
            if Checkin_Froum!='' and Account!='' and Password!='':
                self.Decrypt_Config()
                Users_Tree = ET.parse(self.ConfigXml)
                logging.info(f"Forum_Users, 解析{self.ConfigXml}-新增帳號")
                Users_Root = Users_Tree.getroot()
                if not Users_Root.findall(f'.//*[.="{Checkin_Froum}"]../*[.="{Account}"]'):
                    Users_UserElement = ET.SubElement(Users_Root, 'User')
                    logging.info("Forum_Users, 建立子節點: User")
                    Users_Forum = ET.SubElement(Users_UserElement, 'Forum')
                    Users_Forum.text = Checkin_Froum
                    logging.info(f"Forum_Users, 建立論壇名稱: {Checkin_Froum}")
                    Users_Account = ET.SubElement(Users_UserElement, 'Account')
                    Users_Account.text = Account
                    logging.info(f"Forum_Users, 建立帳號: {Account}")
                    Users_Password = ET.SubElement(Users_UserElement, 'Password')
                    Users_Password.text = Password
                    logging.info("Forum_Users, 建立密碼: {Password}".format(Password='************'))
                    Users_Tree = ET.ElementTree(Users_Root)
                    Users_Tree.write(self.ConfigXml, encoding='utf-8', xml_declaration=True)
                    logging.info(f"Forum_Users, 更新{self.ConfigXml}論壇使用者參數")
                self.Encrypt_Config()
                
    def Load_Users(self):
        if os.path.exists(self.ConfigXml):
            Temp_List = []
            self.Decrypt_Config()
            Users_Tree = ET.parse(self.ConfigXml)
            logging.info(f"Forum_Users, 解析{self.ConfigXml}-讀取帳號")
            Users_Root = Users_Tree.getroot()
            for User_Element in Users_Root:
                for Temp_Element in User_Element:
                    if Temp_Element.tag == 'Forum':
                        Temp_Forum = Temp_Element.text
                        logging.info(f"Forum_Users, 讀取論壇名稱: {Temp_Forum}")
                    if Temp_Element.tag == 'Account':
                        Temp_Account = Temp_Element.text
                        logging.info(f"Forum_Users, 讀取帳號: {Temp_Account}")
                Temp_List.append([Temp_Forum, Temp_Account])
            self.Encrypt_Config()
            return Temp_List
            logging.info("Forum_Users, 返回所有論壇帳號")
                
    def Remove_Users(self, Checkin_Froum='', Account=''):
        if os.path.exists(self.ConfigXml):
            if Checkin_Froum!='' and Account!='':
                self.Decrypt_Config()
                Users_Tree = ET.parse(self.ConfigXml)
                logging.info(f"Forum_Users, 解析{self.ConfigXml}-刪除帳號")
                Users_Root = Users_Tree.getroot()
                if Users_Root.findall(f'.//*[.="{Checkin_Froum}"]../*[.="{Account}"]'):
                    Users_Root.remove(Users_Root.findall(f'.//*[.="{Checkin_Froum}"]../*[.="{Account}"]..')[0])
                    logging.info(f"Forum_Users, 移除論壇名稱: {Checkin_Froum}, 移除帳號: {Account}")
                    Users_Tree = ET.ElementTree(Users_Root)
                    Users_Tree.write(self.ConfigXml, encoding='utf-8', xml_declaration=True)
                    logging.info(f"Forum_Users, 更新{self.ConfigXml}論壇使用者參數")
                self.Encrypt_Config()
                
    def Encrypt_Config(self):
        with open(self.ConfigXml, 'r+', encoding='utf-8') as file:
            TempEncrypt = self.Forum_Encryption_Main.AES_Encrypt(file.read())
            logging.info(f"Forum_Users, 讀取{self.ConfigXml}並使用AES進階加密") 
            file.seek(0)
            logging.info("Forum_Users, 文件指標移動到文件開頭") 
            file.truncate()
            logging.info("Forum_Users, 文件截斷到目前為止的資料") 
            file.write(TempEncrypt)
            logging.info("Forum_Users, 寫入AES進階解密後的資料")
            
    def Decrypt_Config(self):
        with open(self.ConfigXml, 'r+', encoding='utf-8') as file:
            TempDecrypt = self.Forum_Encryption_Main.AES_Decrypt(file.read())
            logging.info(f"Forum_Users, 讀取{self.ConfigXml}並使用AES進階解密")
            file.seek(0)
            logging.info("Forum_Users, 文件指標移動到文件開頭") 
            file.truncate()
            logging.info("Forum_Users, 文件截斷到目前為止的資料")
            file.write(TempDecrypt)
            logging.info("Forum_Users, 寫入AES進階解密後的資料")
            
if __name__ == '__main__':
    Forum_Users_Functions()