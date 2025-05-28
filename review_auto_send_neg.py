import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

# 載入 .env 變數
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SENDER_EMAIL   = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD= os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

print(f"環境設置檢查:")
print(f"- OpenAI API 金鑰: {'已設置' if OPENAI_API_KEY else '未設置'}")
print(f"- 發件人郵箱: {'已設置' if SENDER_EMAIL else '未設置'}")
print(f"- 發件人密碼: {'已設置' if SENDER_PASSWORD else '未設置'}")
print(f"- 收件人郵箱: {'已設置' if RECEIVER_EMAIL else '未設置'}")

if not all([OPENAI_API_KEY, SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL]):
    print("錯誤：缺少必要的環境變數，請確認 .env 檔案已正確設置。")
    exit(1)

# 初始化新版 SDK 客戶端
client = OpenAI(api_key=OPENAI_API_KEY)
print("OpenAI 客戶端初始化完成")

# 根據檔名決定收件人
script_name = os.path.basename(__file__)
if "neg" in script_name:
    RECEIVER_EMAIL = "amz_reviews_negative@tomofun.com"
else:
    RECEIVER_EMAIL = "amz_reviews_positive@tomofun.com"

# 用於獲取地區全名的函數
def get_region_full_name(region_code):
    region_names = {
        "US": "United States",
        "CA": "Canada",
        "JP": "Japan",
        "DE": "Germany",
        "UK": "United Kingdom",
        "AU": "Australia", 
        "FR": "France"
    }
    return region_names.get(region_code, region_code)

# 測試模式標誌 - 設為 True 時，即使 OpenAI API 失敗也會嘗試發送郵件
TEST_MODE = True

# Step 1: 讀取原始評論檔案
try:
    with open("raw_reviews.txt", "r", encoding="utf-8") as f:
        # 讀取第一行作為市場代碼
        country = f.readline().strip()
        # 讀取剩餘所有行作為評論內容
        reviews = f.read()
    
    print(f"成功讀取評論檔案")
    print(f"- 市場代碼: {country}")
    print(f"- 評論內容長度: {len(reviews)} 字元")
    print(f"- 評論內容前 100 字元: {reviews[:100]}...")
    
except FileNotFoundError:
    print("錯誤：找不到 raw_reviews.txt，請確認檔案存在且命名正確。")
    exit(1)
except Exception as e:
    print(f"讀取檔案時發生錯誤: {e}")
    exit(1)

# 檢查市場代碼是否有效
valid_regions = ["US", "CA", "JP", "DE", "UK", "AU", "FR"]
if country not in valid_regions:
    print(f"錯誤：市場代碼 '{country}' 無效。有效的市場代碼為: {', '.join(valid_regions)}")
    exit(1)

print(f"\n處理 {country} 地區評論...")

# 取得今天日期 (mm/dd)
today_str = datetime.now().strftime("%m/%d")

# 對評論進行 OpenAI 處理
system_prompt = """
You'll get raw Amazon-style review text. Turn it into grouped, structured blocks.
1. Extract & Classify
   • Product Type (e.g. Dog Cam)
   • Subscription Model
     – PSP = paid/in-app subscription required
     – SA  = self-contained or limited features
2. Group by Product Type + Model
   Only include headings if there's ≥1 review:
   [Product Type] – PSP Reviews
   [Product Type] – SA Reviews
3. Under each heading, one review per line:
   • Reviewer Name (X stars): "Review Title"
     > Review Content
   – Round "5.0 out of 5 stars" → "5 stars."
   – Strip locale/date ("Reviewed in…on…").
   – Leave content verbatim.
4. Example
Raw Input:
Lynn Gregory 5.0 out of 5 stars Amazing Pet camera and nanny!
Reviewed in the United States on February 1, 2025
Style: Dog Cam – Limited Features
Anyone that works and wants to keep an eye on their fur babies, this is phenomenal. The treat tosser is incredible I highly recommend getting the recommended size. If my dogs bark too much it plays soothing music and spits treats out to discourage barking. It also gives you a sped up entire day video clip and Report. This is the best purchase I have purchased in years

Slack Output:
Dog Cam – SA Reviews
• Lynn Gregory (5 stars): "Amazing Pet camera and nanny!"
  > Anyone that works and wants to keep an eye on their fur babies, this is phenomenal. The treat tosser is incredible I highly recommend getting the recommended size. If my dogs bark too much it plays soothing music and spits treats out to discourage barking. It also gives you a sped up entire day video clip and Report. This is the best purchase I have purchased in years

Email output (keep exactly as-is):
[Product Name + PSP/SA Reviews] Reviewer Name rated X star(s): Review Title Review Content
"""

user_prompt = f"Raw Reviews from {get_region_full_name(country)}:\n{reviews}"

# 預設虛擬內容，用於 API 失敗時測試郵件功能
dummy_review_result = f"""
[Dog Camera] – PSP Reviews
あ (1 star): "楽しみにしていたのに最悪な気持ちです"
> 楽しみに待っていましたがこんなに画面黒い線入っているのが普通なのでしょうか？すごく残念です。

[Mini Camera] – PSP Reviews
もかれん (2 stars): "留守番時、安心しますが品質に問題あり"
> 5歳のトイプードル1頭用で使用しています。留守番時は寝室に居ることが多いので設置したら寝て待っている様子が記録されてます。しかし画質が悪いです。
"""

review_result = dummy_review_result  # 先設定預設內容

try:
    # 呼叫 OpenAI
    print(f"正在呼叫 OpenAI API 處理 {country} 評論...")
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
    print(f"API 呼叫成功，處理結果長度: {len(review_result)} 字元")

    print(f"=== {country} AI 整理後內容 ===")
    print(review_result[:200] + "..." if len(review_result) > 200 else review_result)
except Exception as e:
    print(f"OpenAI API 呼叫失敗: {e}")
    print(f"使用預設評論內容進行測試...")
    if not TEST_MODE:
        exit(1)

# 發送電子郵件
subject = f"[{country}] Weekly negative feedback collection"
body = f"""\
Hi Team,

This week's negative feedback summary for {get_region_full_name(country)} as of {today_str}:

{review_result}

Best,
Automation Bot by Lean
"""

msg = MIMEMultipart()
msg["From"] = SENDER_EMAIL
msg["To"] = RECEIVER_EMAIL
msg["Subject"] = subject
msg.attach(MIMEText(body, "plain"))

print(f"郵件已準備完成:")
print(f"- 寄件人: {SENDER_EMAIL}")
print(f"- 收件人: {RECEIVER_EMAIL}")
print(f"- 主旨: {subject}")
print(f"- 內容長度: {len(body)} 字元")

context = ssl.create_default_context()
try:
    print(f"準備發送郵件至 {RECEIVER_EMAIL}...")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        print(f"正在嘗試登入 SMTP 伺服器...")
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        print(f"登入成功，正在發送郵件...")
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
    print(f"Email 已寄出到 {RECEIVER_EMAIL}（{country} 負面回應）！")
except Exception as e:
    print(f"Email 發送失敗，詳細錯誤：")
    print(f"錯誤類型: {type(e).__name__}")
    print(f"錯誤訊息: {str(e)}")
    
    # 檢查常見的錯誤並提供建議
    if "smtplib.SMTPAuthenticationError" in str(type(e)):
        print("可能是郵箱登入資訊有誤。請檢查:")
        print("1. 發件郵箱地址是否正確")
        print("2. 使用的是否為應用專用密碼而非一般密碼")
        print("3. 郵箱是否啟用了兩步驗證")
    elif "ssl.SSLError" in str(type(e)):
        print("SSL 連線錯誤。請檢查網路連線和伺服器設定。")
    elif "smtplib.SMTPSenderRefused" in str(type(e)):
        print("發件人被拒絕。可能是發件郵箱有限制或被暫時封鎖。")
    elif "smtplib.SMTPRecipientsRefused" in str(type(e)):
        print("收件人郵箱地址被拒絕。請確認收件地址正確性。")

print("\n程式執行完成。")
