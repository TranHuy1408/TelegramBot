import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from bs4 import BeautifulSoup

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

# Xử lý lệnh /weather
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Lấy thông tin thời tiết và gửi lên nhóm
    weather_info = get_weather_info()
    group_id = update.message.chat_id
    await send_weather_info(context, group_id, weather_info)

    # Lập lịch gửi thông tin cập nhật dự báo thời tiết mỗi 30 phút
    job_queue = context.job_queue
    job_queue.run_repeating(send_periodic_weather_info, interval=1800, first=0, context=update.message.chat_id)

# Hàm gửi thông tin cập nhật dự báo thời tiết mỗi 30 phút
async def send_periodic_weather_info(context):
    weather_info = get_weather_info()
    group_id = context.job.context
    await send_weather_info(context, group_id, weather_info)

# Khởi tạo ứng dụng
app = ApplicationBuilder().token("7119007732:AAE73mlsHrsqXNXTuOUiZ7ErCiZlabAzoGg").build()


# Dừng toàn bộ các phiên bản trước của bot (nếu có)
app.updater.stop_polling()

# Thêm xử lý lệnh
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("weather", weather))

# Khởi động ứng dụng
app.run_polling()
