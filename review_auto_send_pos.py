import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from openai import OpenAI

# 載入 .env 變數
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SENDER_EMAIL   = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD= os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# 初始化新版 SDK 客戶端
client = OpenAI(api_key=OPENAI_API_KEY)

# Step 1: 讀取原始評論
try:
    with open("raw_reviews.txt", "r", encoding="utf-8") as f:
        raw_reviews = f.read()
except FileNotFoundError:
    print("錯誤：找不到 raw_reviews.txt，請確認檔案存在且命名正確。")
    exit(1)

# Step 2: 呼叫 OpenAI 進行整理格式
system_prompt = """
You’ll get raw Amazon-style review text. Turn it into grouped, structured blocks.
1. Extract & Classify
   • Product Type (e.g. Dog Cam)
   • Subscription Model
     – PSP = paid/in-app subscription required
     – SA  = self-contained or limited features
2. Group by Product Type + Model
   Only include headings if there’s ≥1 review:
   [Product Type] – PSP Reviews
   [Product Type] – SA Reviews
3. Under each heading, one review per line:
   • Reviewer Name (X stars): “Review Title”
     > Review Content
   – Round “5.0 out of 5 stars” → “5 stars.”
   – Strip locale/date (“Reviewed in…on…“).
   – Leave content verbatim.
4. Return the result in plain text.
"""

user_prompt = f"Raw Reviews:\n{raw_reviews}"

# 呼叫 OpenAI
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": user_prompt},
    ],
    temperature=0.7,
    max_tokens=2000,
)
review_result = response.choices[0].message.content

print("=== AI 整理後內容 ===")
print(review_result)

# Step 3: 自動寄送 Email（這裡標題改為正面回應）
subject = "Amazon Reviews Weekly Report (正面回應)"
body = f"""\
Hi Team,

本週為正面回應彙整：

{review_result}

Best,
Automation Bot
"""

msg = MIMEMultipart()
msg["From"]    = SENDER_EMAIL
msg["To"]      = RECEIVER_EMAIL
msg["Subject"] = subject
msg.attach(MIMEText(body, "plain"))

context = ssl.create_default_context()
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
    print("Email 已寄出到 it@tomofun.com！")
except Exception as e:
    print("Email 發送失敗，錯誤：", e)
