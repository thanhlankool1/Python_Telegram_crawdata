from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime
import os, time

class Covid19():
    def __init__(self):
        # self.chrome =  webdriver.Chrome(executable_path=os.path.join("etc", "chromedriver.exe"))
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome = webdriver.Chrome(executable_path=os.path.join("etc", "chromedriver_94.exe"), options=self.chrome_options)
        
    def craw_data(self, _today):
        data_save_file = []
        try:
            self.chrome.get("https://covid19.gov.vn/")
            self.chrome.switch_to.frame(1)  # 1 là iframe thứ bao nhiêu trong trang web mình crawl
            target = self.chrome.find_elements_by_xpath("/html/body/div[2]/div[1]/div")  # xpath data mục tiêu.
            for data in target:
                cities = data.find_elements_by_class_name("city")
                totals = data.find_elements_by_class_name("total")
                todays = data.find_elements_by_class_name("daynow")
                deads = data.find_elements_by_class_name("die")

            list_cities = [city.text for city in cities]
            list_total = [total.text for total in totals]
            list_today = [today.text for today in todays]
            list_dead = [dead.text for dead in deads]
            for i in range(len(list_cities)):
                row = "{},{},{},{}\n".format(list_cities[i], list_total[i], list_today[i], list_dead[i])
                data_save_file.append(row)
            with open(_today, 'w+', encoding='utf-8') as f:
                f.writelines(data_save_file)
            return True
        except Exception as e:
            print("%s" % e)
            return False
        finally:
            self.chrome.close()  # đóng trình duyệt

    def check_data_day_exist(self):
        _today = (datetime.datetime.now()).strftime("%Y%m%d")
        file = os.path.join("data", f"{_today}.csv") #biến file có giá trị là today.csv
        if os.path.isfile(file):#check xem có file này không
            return True #trả ra true nếu có
        result = self.craw_data(file) #không thì crawl data.
        return result #rồi trả ra.