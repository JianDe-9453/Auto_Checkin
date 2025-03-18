# 載入此檔案所需自定義py
from Forum_Users import Forum_Users_Functions
import sys

def __Forum_Config_Main():
    while True:
        try:
            sys.stdout.write("網頁自動簽到修改工具 \n(1)列出所有帳號\n(2)新增帳號\n(3)刪除帳號\n(4)離開此工具\n")
            # Console使用輸入
            # AnsData = sys.stdin.readline().rstrip()
            AnsData = int(input())
            match AnsData:
                case 1:
                    Data = Forum_Users_Functions().Load_Users()
                    for Forum_Name, Forum_Account in Data:
                        sys.stdout.write(f"網頁名稱: {Forum_Name}, 帳號: {Forum_Account}\n")
                case 2:
                    sys.stdout.write("輸入網頁\n(1)APK\n")
                    Forum_Name = int(input())
                    match Forum_Name:
                        case 1:
                            sys.stdout.write("輸入帳號\n")
                            Forum_Account = input()
                            sys.stdout.write("輸入密碼\n")
                            Forum_Password = input()
                            Forum_Users_Functions().Creat_Users(Checkin_Froum='APK', Account=Forum_Account, Password=Forum_Password)
                        case _:
                            raise ValueError
                case 3:
                    sys.stdout.write("輸入網頁\n(1)APK\n")
                    Forum_Name = int(input())
                    match Forum_Name:
                        case 1:
                            sys.stdout.write("輸入帳號\n")
                            Forum_Account = input()
                            Forum_Users_Functions().Remove_Users(Checkin_Froum='APK', Account=Forum_Account)
                        case _:
                            raise ValueError
                case 4:
                    break
                case _:
                    raise ValueError
        except ValueError:
            sys.stdout.write("Alarm: 請輸入選項內數值")

if __name__ == '__main__':
    __Forum_Config_Main()