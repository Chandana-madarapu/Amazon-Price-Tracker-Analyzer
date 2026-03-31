
# 🛒 Amazon Price Tracker & Analyzer

An automated Python-based system that tracks product prices from Amazon, stores historical price data, and sends alerts when prices drop below a defined threshold.

---

## 🚀 Features

- 🔍 Web scraping using BeautifulSoup to extract product details
- 📊 Tracks and stores price history in CSV (dataset creation)
- 📧 Email notifications when price drops below target
- ⏰ Automated daily execution using scheduler
- 🛍️ Supports tracking multiple products

---

## 🧠 How It Works

1. Sends request to Amazon product page
2. Parses HTML to extract product title and price
3. Stores data in a CSV file (`price_data.csv`)
4. Compares current price with target price
5. Sends email alert if price drops
6. Runs automatically at scheduled time

---

## 🛠️ Tech Stack

- Python
- BeautifulSoup (Web Scraping)
- Requests (HTTP Requests)
- SMTP (Email Notifications)
- Schedule (Automation)
- CSV (Data Storage)

---

## 📂 Project Structure

price-tracker/
│── price_tracker.py
│── price_data.csv
│── .env
│── README.md


---

## 🔐 Environment Variables

Create a `.env` file in the root directory:

MY_EMAIL=your_email@gmail.com

MY_PASSWORD=your_app_password


> ⚠️ Use Gmail App Password instead of your actual password

---

## 📦 Installation

```bash
pip install requests beautifulsoup4 python-dotenv schedule
