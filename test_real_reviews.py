#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
實際評論測試程式：測試 raw_reviews.txt 檔案內容
模擬完整的信件生成流程，在 console 中顯示結果
"""

import os
from datetime import datetime
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def get_region_full_name(region_code):
    """獲取地區全名"""
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

def simulate_openai_processing(reviews_text, country):
    """模擬 OpenAI 處理評論的結果"""
    
    # 這裡模擬 OpenAI 會如何處理和格式化評論
    # 在實際情況中，這會是 OpenAI API 的回應
    
    processed_result = f"""[Dog Camera] – SA Reviews
• Victoria Nerkowski (5 stars): "Great product"
  > I bought this for a wedding shower gift and it was a big hit! She just got a new puppy and is a nervous new dog mom so she loved this. The treat aspect is also a nice touch. Highly recommend

• Amazon Customer (5 stars): "All purpose excellence"
  > It tells you when your dog is barking, when it's getting active or whatever the case! This was the best purchase for us! Our German shepherd puppy is a bit destructive when we're gone and we were able to distract her until she went to sleep by launching treats/kibs at her!

• Crystal Wojciechowski (5 stars): "Love it! Dogs love it too!"
  > Love this camera!

• Gabriela Chavez (5 stars): "Love it"
  > Love it!!!

[Cat Camera] – Only Reviews  
• Deborah Rees (5 stars): "Fun!"
  > I love watching my cat enjoy the treats when they are dispensed. I find the top a little difficult to remove, but that makes it hard for it to be removed by the cat. I also like being able to check on her while I am away."""
    
    return processed_result

def test_raw_reviews_email():
    """測試使用 raw_reviews.txt 的實際信件內容"""
    
    print(" 實際評論檔案測試")
    print("=" * 70)
    
    # Step 1: 讀取 raw_reviews.txt
    try:
        with open("raw_reviews.txt", "r", encoding="utf-8") as f:
            # 第一行是市場代碼
            country = f.readline().strip()
            # 其餘內容是評論
            reviews = f.read()
        
        print(f"✅ 成功讀取評論檔案")
        print(f"    市場代碼: {country}")
        print(f"    評論內容長度: {len(reviews)} 字元")
        print(f"    評論內容預覽: {reviews[:100]}...")
        
    except FileNotFoundError:
        print("錯誤：找不到 raw_reviews.txt 檔案")
        return
    except Exception as e:
        print(f"讀取檔案錯誤: {e}")
        return
    
    # Step 2: 模擬 OpenAI 處理
    print(f"\n🤖 模擬 OpenAI 處理 {country} 地區評論...")
    processed_reviews = simulate_openai_processing(reviews, country)
    print(f"✅ 處理完成，結果長度: {len(processed_reviews)} 字元")
    
    # Step 3: 生成信件內容
    SENDER_EMAIL = os.getenv("SENDER_EMAIL", "automation@tomofun.com")
    
    # 根據檔名決定是正面還是負面評論
    script_name = os.path.basename(__file__)
    if "neg" in script_name:
        RECEIVER_EMAIL = "amz_reviews_negative@tomofun.com"
        feedback_type = "negative feedback"
    else:
        RECEIVER_EMAIL = "amz_reviews_positive@tomofun.com"
        feedback_type = "positive feedback"
    
    today_str = datetime.now().strftime("%m/%d")
    subject = f"[{country}] Weekly {feedback_type} collection"
    
    email_body = f"""Hi Team,

This week's {feedback_type} summary for {get_region_full_name(country)} as of {today_str}:

{processed_reviews}

Best,
Automation Bot by Lean"""
    
    # Step 4: 顯示完整信件內容
    print(f"\n📧 生成的信件內容")
    print("=" * 70)
    print(f"寄件人: {SENDER_EMAIL}")
    print(f"收件人: {RECEIVER_EMAIL}")
    print(f"日期: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"主旨: {subject}")
    print("=" * 70)
    print("信件正文:")
    print("-" * 70)
    print(email_body)
    print("=" * 70)
    
    # Step 5: 統計資訊
    print(f"統計資訊:")
    print(f"   - 原始評論長度: {len(reviews)} 字元")
    print(f"   - 處理後長度: {len(processed_reviews)} 字元")
    print(f"   - 主旨長度: {len(subject)} 字元")
    print(f"   - 完整信件長度: {len(email_body)} 字元")
    print(f"   - 總單字數: {len(email_body.split())} 單字")
    print("=" * 70)
    print("測試完成！這就是實際會發送的信件內容。")

def show_raw_content():
    """顯示原始評論內容以便比對"""
    print("\n 原始評論內容 (raw_reviews.txt):")
    print("=" * 70)
    
    try:
        with open("raw_reviews.txt", "r", encoding="utf-8") as f:
            content = f.read()
            print(content)
    except FileNotFoundError:
        print("找不到 raw_reviews.txt 檔案")
    
    print("=" * 70)

if __name__ == "__main__":
    print("Raw Reviews 測試程式")
    print("這個程式會讀取 raw_reviews.txt 並模擬完整的信件生成流程")
    print()
    
    # 選項選單
    while True:
        print("\n選擇測試選項:")
        print("1. 🧪 測試完整信件生成流程")
        print("2. 🔍 查看原始評論內容")
        print("3. 🚪 退出")
        
        choice = input("\n請輸入選項 (1-3): ").strip()
        
        if choice == "1":
            test_raw_reviews_email()
        elif choice == "2":
            show_raw_content()
        elif choice == "3":
            print(" bye!")
            break
        else:
            print("無效選項，請重新選擇") 