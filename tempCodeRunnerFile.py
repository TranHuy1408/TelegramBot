import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from bs4 import BeautifulSoup

# Hàm gửi tin nhắn cập nhật thông tin thời tiết
async def send_periodic_weather_info(context):
    while True:
        await asyncio.sleep(1800)  # Chờ 1800 giây (30 phút)
        weather_info = get_weather_info()
        group_id = -4151032640  # ID của nhóm, thay thế bằng ID thực tế của nhóm
        await send_weather_info(context, group_id, weather_info)

# Hàm lấy thông tin thời tiết từ trang web
def get_weather_info():
    weather_info = []
    response = requests.get('https://nchmf.gov.vn/Kttvsite/vi-VN/1/da-nang-w55.html#')
    soup = BeautifulSoup(response.text, 'html.parser')
    mydivs = soup.find_all('div', class_='text-weather-location fix-weather-location')
    for div in mydivs:
        weather_info.append(div.text.strip())
    return weather_info

# Hàm gửi tin nhắn thời tiết
async def send_weather_info(context, group_id, weather_info):
    message = "\n".join(weather_info)
    await context.bot.send_message(chat_id=group_id, text=f'Thông tin thời tiết Đà Nẵng:\n{message}')

# Xử lý lệnh /hello
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Chào bạn {update.effective_user.first_name}')

# Khởi tạo ứng dụng
app = ApplicationBuilder().token("7119007732:AAE73mlsHrsqXNXTuOUiZ7ErCiZlabAzoGg").build()

# Thêm xử lý lệnh
app.add_handler(CommandHandler("hello", hello))

# Thêm công việc lập lịch
app.job_queue.run_repeating(send_periodic_weather_info, interval=1800, first=0)

# Khởi động ứng dụng
app.run_polling()