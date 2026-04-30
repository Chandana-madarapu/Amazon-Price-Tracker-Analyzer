import requests
from bs4 import BeautifulSoup
import smtplib
import ssl
from email.message import EmailMessage
import schedule
import time
import os
from dotenv import load_dotenv
import csv
from datetime import datetime
import pandas as pd

load_dotenv()

# ----------- LOAD PRODUCTS FROM CSV -----------
def load_products():
    try:
        df = pd.read_csv("products.csv")
        products = []

        for _, row in df.iterrows():
            products.append({
                "url": row["url"],
                "target": row["target"]
            })

        return products

    except Exception as e:
        print("❌ Error loading products:", e)
        return []


# ----------- GET PRODUCT DETAILS -----------
def get_product_details(url):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    title_tag = soup.find(id="productTitle")
    title = title_tag.get_text().strip() if title_tag else "No Title"

    price = None

    selectors = [
        ("span", "a-offscreen"),
        ("span", "a-price-whole"),
        ("span", "a-price a-text-price a-size-medium apexPriceToPay")
    ]

    for tag, cls in selectors:
        price_tag = soup.find(tag, class_=cls)
        if price_tag:
            price_text = price_tag.get_text().replace("₹", "").replace(",", "").strip()
            if price_text.replace(".", "", 1).isdigit():
                price = float(price_text)
                break

    return title, price


# ----------- SAVE DATA -----------
def save_price(title, price):
    if price is None:
        return

    file_exists = False

    try:
        with open("price_data.csv", "r"):
            file_exists = True
    except:
        pass

    with open("price_data.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Date", "Product", "Price"])

        writer.writerow([datetime.now(), title, price])


# ----------- SEND EMAIL -----------
def send_email(title, price, url):
    MY_EMAIL = os.getenv("MY_EMAIL")
    MY_PASSWORD = os.getenv("MY_PASSWORD")

    if not MY_EMAIL or not MY_PASSWORD:
        print("❌ Email not configured")
        return

    msg = EmailMessage()
    msg["Subject"] = "📉 Price Drop Alert!"
    msg["From"] = MY_EMAIL
    msg["To"] = MY_EMAIL

    msg.set_content(f"{title}\n\nPrice: ₹{price}\n\n{url}")

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(MY_EMAIL, MY_PASSWORD)
            server.send_message(msg)
        print("📧 Email sent!")
    except Exception as e:
        print("❌ Email failed:", e)


# ----------- MAIN FUNCTION -----------
def check_price():
    print("\n🔍 Checking prices...\n")

    products = load_products()

    for product in products:
        url = product["url"]
        target = product["target"]

        title, price = get_product_details(url)

        print(f"Product: {title}")
        print(f"Current Price: ₹{price}")

        save_price(title, price)

        if price and price < target:
            print("🚨 Price dropped!")
            send_email(title, price, url)
        else:
            print("😐 No price drop yet")

        print("-" * 50)


# ----------- RUN ONCE -----------
check_price()

# ----------- AUTOMATION -----------
schedule.every().day.at("09:00").do(check_price)

print("⏰ Automation running...")

while True:
    schedule.run_pending()
    time.sleep(1)
