import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# 載入日期與時間
import datetime
# 載入日誌管理
import logging

Logging_Format = '%(asctime)s %(levelname)s: %(message)s'
Date_Log = '%Y-%m-%d'
Date_Format = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(level=logging.INFO, filename=f'{datetime.date.today().strftime("%Y%m%d")}_Auto_Checkin.log', filemode='a', format=Logging_Format, datefmt=Date_Format)

class Forum_Encryption_Functions():
    def __init__(self, Key=None):
        if Key is not None:
            self.Key = Key
            
    def New_RandomKey(self):
        return get_random_bytes(32)
    
    def AES_Encrypt(self, PlainText):
        iv = get_random_bytes(16)
        logging.info("Forum_Encryption, AES進階加密-產生初始向量")
        cipher = AES.new(self.Key, AES.MODE_CBC, iv)
        logging.info("Forum_Encryption, AES進階加密-創建加密對象")
        encrypted = cipher.encrypt(pad(PlainText.encode('utf-8'), AES.block_size))
        logging.info("Forum_Encryption, AES進階加密-加密並補位")
        return base64.b64encode(iv + encrypted).decode('utf-8')
        logging.info("Forum_Encryption, AES進階加密-返回加密後的資料(含IV)")
        
    def AES_Decrypt(self, EncryptedText):
        encrypted_bytes = base64.b64decode(EncryptedText)
        logging.info("Forum_Encryption, AES進階加密-解密")
        iv = encrypted_bytes[:16]
        logging.info("Forum_Encryption, AES進階加密-提取IV")
        encrypted_data = encrypted_bytes[16:]
        logging.info("Forum_Encryption, AES進階加密-提取加密資料")
        cipher = AES.new(self.Key, AES.MODE_CBC, iv)
        logging.info("Forum_Encryption, AES進階加密-創建解密對象")
        decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size).decode('utf-8')
        logging.info("Forum_Encryption, AES進階加密-解密並去補位")
        return decrypted
        logging.info("Forum_Encryption, AES進階加密-返回解密過後資料")

if __name__ == '__main__':
    Forum_Encryption_Functions()