import os

# توکن ربات (خودت دادی)
BOT_TOKEN = '8512123339:AAEOrT2yPiH1OmScwKByngVkOrnqroXaYco'

# آیدی ادمین (خودتی)
ADMIN_IDS = [8131712128]

# پلن‌های فروش
PLANS = {
    '1month': {
        'name': '۱ ماهه',
        'price': 50000,
        'duration': 30
    },
    '3months': {
        'name': '۳ ماهه',
        'price': 120000,
        'duration': 90
    },
    '6months': {
        'name': '۶ ماهه',
        'price': 200000,
        'duration': 180
    },
    '1year': {
        'name': 'یک ساله',
        'price': 350000,
        'duration': 365
    }
}

# درگاه پرداخت (اگه نداری همین خالی باشه)
ZARINPAL_MERCHANT_ID = ''
