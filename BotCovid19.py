"""
xem qua cái code Covid19 nhé. 
"""

#cài thư viện pyTelegramBotAPI nó sẽ co nhé.
import datetime, os
import telebot 

#cái này để nó hiểu định dạng vẽ bảng ra.
from telegram import ParseMode

#cái này để vẽ thành talbe các data mình đang có. as là mình gán cái thư viện thành tên pt ấy các bạn
import prettytable as pt 

#phần này sẽ là cái code video trước mình crawl data ấy.
from models.Covid19 import Covid19

"có 1 xíu lỗi. mình đã nhìn ra mình sai ở đâu ^_^ try except finally và bot.polling phải bọc ở ngoài nhé mọi ng."

#khai báo bot 
bot = telebot.TeleBot('2043191968:AAF_1ktnbHFv7blla6pOPfx7TEEpHez7zTY')
bot_chatID = ""# mình chưa lấy chat id của nó nên để rỗng đi nhé.


def render_talbe(): #sẽ tạo 1 hàm để render table nhé.
    _today = (datetime.datetime.now()).strftime("%Y%m%d") #tạo 1 biên _today. có định dạng là YYYYmmdd(20210930)
    file = os.path.join("data", f"{_today}.csv") 
    with open(file, "r", encoding='utf-8') as f: #mở file, dưới dạng read only (r)
        result  = f.readlines() #lấy toàn bộ data gán vào result
        result.pop(0) # bỏ đi dòng đầu tiên
    table = pt.PrettyTable(['Tỉnh/TP', 'Tổng số ca', 'Hôm nay', 'Tử vong']) #tạo 1 table có 1 cột. như bên.
    table.title = "Thông Tin CoVid 19 VN" #phần tiêu đề của bảng.
    for row_ in result:
        row = row_.replace("\n", "").split(",")
        table.add_row([row[0], row[1], row[2], row[3]])
    return table

if __name__ == "__main__": #dòng code chạy đầu tiên trong python.
    try:
        @bot.message_handler(func=lambda message: True,
                            commands=["covid19"]) 
        def covid19(message):
            #gọi hàm Covid video trước.
            #cái này trả ra giá trj True or False như mình xem lúc này nên có thể viết như sau
            if Covid19().check_data_day_exist(): #== True sẽ làm trong if.
                #nếu có data rồi thì sẽ làm gì. vẽ 1 cái table rồi in ra thôi.
                table = render_talbe() #gọi cái hàm vừa code xong. để vẻ bảng.
                bot.reply_to(message, f"<pre>{table}</pre>", parse_mode=ParseMode.HTML) #repply cái table vừa vẽ ra là xong. thử xem sao nhé.
            else: # == False thì nó sẽ xuống đây
                #nếu = False: thì crawl data lỗi. sẽ in ra màn hình là t craw data k được.
                bot.reply_to(message, "crawl data lỗi rồi. thử lại xem sao !!!!!")

            #bot.reply_to(message, "tôi sẽ lấy thông tin covid sau khi code xong")#nhìn cái tên cũng biết nó sẽ repply đúng k. 2 tham số nhé. msg. và tin nhắn trả lời là gì
    except Exception as e:
            print(e)
    finally:
        bot.polling() #cái này là cấu trúc của người viết ra conbot nhé. nên cần có nó

"""
mình sẽ giả lập một lỗi . mà nghĩ các bạn sẽ dễ dính phải nhất.
"""