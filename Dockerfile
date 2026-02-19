# استفاده از پایتون رسمی
FROM python:3.11-slim

# ایجاد پوشه کار
WORKDIR /app

# کپی فایل‌های مورد نیاز
COPY requirements.txt .
COPY bot.py .
COPY config.py .

# نصب کتابخونه‌ها
RUN pip install --no-cache-dir -r requirements.txt

# اجرای ربات
CMD ["python", "bot.py"]
