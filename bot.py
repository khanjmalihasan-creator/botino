from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from config import BOT_TOKEN, PLANS
from database import Database
import datetime

db = Database()

async def start(update: Update, context):
    user = update.effective_user
    db.add_user(user.id, user.username, user.first_name)
    
    keyboard = [
        [InlineKeyboardButton("🛒 خرید", callback_data='buy')],
        [InlineKeyboardButton("📋 اکانت‌ها", callback_data='accounts')],
        [InlineKeyboardButton("📞 پشتیبانی", callback_data='support')]
    ]
    
    await update.message.reply_text(
        f"سلام {user.first_name}!\nبه ربات VPN خوش اومدی",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_click(update: Update, context):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'buy':
        keyboard = []
        for pid, plan in PLANS.items():
            keyboard.append([InlineKeyboardButton(
                f"{plan['name']} - {plan['price']} تومان",
                callback_data=f'plan_{pid}'
            )])
        keyboard.append([InlineKeyboardButton("🔙 برگشت", callback_data='back')])
        
        await query.edit_message_text(
            "پلن مورد نظر رو انتخاب کن:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    elif query.data.startswith('plan_'):
        plan_id = query.data.replace('plan_', '')
        plan = PLANS[plan_id]
        
        order_id = db.create_order(query.from_user.id, plan_id, plan['price'])
        
        await query.edit_message_text(
            f"✅ سفارش شما ثبت شد\n"
            f"پلن: {plan['name']}\n"
            f"مبلغ: {plan['price']} تومان\n\n"
            f"برای پرداخت به آیدی زیر پیام بده:\n"
            f"@admin",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🏠 منو اصلی", callback_data='main')
            ]])
        )
    
    elif query.data == 'accounts':
        accounts = db.get_user_accounts(query.from_user.id)
        if not accounts:
            text = "شما هیچ اکانت فعالی نداری"
        else:
            text = "اکانت‌های فعال:\n\n"
            for config, expiry in accounts:
                text += f"📅 تاریخ انقضا: {expiry[:10]}\n"
                text += f"🔗 کانفیگ: {config}\n\n"
        
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🏠 منو اصلی", callback_data='main')
            ]])
        )
    
    elif query.data == 'support':
        await query.edit_message_text(
            "برای پشتیبانی به آیدی زیر پیام بده:\n@admin",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🏠 منو اصلی", callback_data='main')
            ]])
        )
    
    elif query.data == 'main':
        keyboard = [
            [InlineKeyboardButton("🛒 خرید", callback_data='buy')],
            [InlineKeyboardButton("📋 اکانت‌ها", callback_data='accounts')],
            [InlineKeyboardButton("📞 پشتیبانی", callback_data='support')]
        ]
        await query.edit_message_text(
            "منوی اصلی:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    
    print("ربات با موفقیت شروع به کار کرد...")
    app.run_polling()

if __name__ == '__main__':
    main()
