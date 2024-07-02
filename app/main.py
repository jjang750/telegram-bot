# -*- coding: UTF-8 -*-

import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    keyboard = [
        [InlineKeyboardButton("디스크사용량", callback_data='Button1')],
        [InlineKeyboardButton("시스템사용량", callback_data='Button2')]
    ]
    replay_markup = InlineKeyboardMarkup(keyboard)

    # 채팅방으로 버튼 전송
    await update.message.reply_text("채팅방 입장을 환영합니다.\n버튼을 선택해 주세요.", reply_markup=replay_markup)


# 버튼 클릭 콜백 처리
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = '/start'
    # 콜백 정보 저장
    query = update.callback_query
    # 버튼 선택에 따른 기능 구현
    if query.data == 'Button1':
        message = os.popen('du / -hd 1 --exclude=volume1 --exclude=volume2 --exclude=volume3 --exclude=proc').read()
    elif query.data == 'Button2':
        message = os.popen('free').read()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


if __name__ == '__main__':
    # 챗봇 application 인스턴스 생성
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    # start 핸들러
    start_handler = CommandHandler('start', start)
    # start 핸들러 추가
    application.add_handler(start_handler)
    # 콜백 핸들러 추가
    application.add_handler(CallbackQueryHandler(button_callback))
    # 폴링 방식으로 실행
    application.run_polling()
