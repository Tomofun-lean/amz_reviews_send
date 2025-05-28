#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試程式：在 console 打印信件內容
用於查看和測試電子郵件的完整內容
"""

import os
from datetime import datetime
from dotenv import load_dotenv

# 載入 .env 變數
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

def generate_test_content(country, is_negative=False):
    """生成測試信件內容"""
    
    # 模擬評論內容
    if is_negative:
        review_result = f"""[Dog Camera] – PSP Reviews
• John Smith (2 stars): "有些問題需要改進"
  > 產品功能不錯但有時會斷線，希望能改善連接穩定性。

• Mary Jones (1 star): "不太滿意"
  > 設定比較複雜，對年長用戶不太友善。

[Cat Camera] – SA Reviews
• David Wilson (3 stars): "還可以"
  > 基本功能正常，但畫質可以更好一些。
"""
    else:
        review_result = f"""[Dog Camera] – PSP Reviews
• しろねこ (5 stars): "安心"
  > 留守の間も色々お知らせ來るし、おやつが飛ばせるのも良い。ミニと2台持ちで使ってますがとても活躍してます。

• アナ (5 stars): "畫像がきれい！"
  > こんなに鮮明に見れるとは思いませんでした。愛犬の様子が見れて安心。もっと早く買えばよかったです。

[Cat Camera] – SA Reviews
• Amazon カスタマー (5 stars): "無くてはならないです"
  > とても頼りにしてます。無くてはならないです。
"""
    
    return review_result

def print_email_content(country="US", email_type="positive"):
    """打印完整的信件內容"""
    
    # 獲取環境變數
    SENDER_EMAIL = os.getenv("SENDER_EMAIL", "test@example.com")
    
    # 根據類型決定收件人和主旨
    if email_type == "negative":
        RECEIVER_EMAIL = "amz_reviews_negative@tomofun.com"
        subject_type = "negative feedback"
        is_negative = True
    else:
        RECEIVER_EMAIL = "amz_reviews_positive@tomofun.com"
        subject_type = "positive feedback"
        is_negative = False
    
    # 生成測試內容
    review_result = generate_test_content(country, is_negative)
    
    # 創建信件內容
    today_str = datetime.now().strftime("%m/%d")
    subject = f"[{country}] Weekly {subject_type} collection"
    body = f"""\
Hi Team,

This week's {subject_type} summary for {get_region_full_name(country)} as of {today_str}:

{review_result}

Best,
Automation Bot by Lean
"""

    # 打印信件詳細資訊
    print("=" * 80)
    print("📧 信件內容測試")
    print("=" * 80)
    print(f" 寄件人: {SENDER_EMAIL}")
    print(f" 收件人: {RECEIVER_EMAIL}")
    print(f" 日期: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f" 主旨: {subject}")
    print("=" * 80)
    print(" 信件正文:")
    print("-" * 80)
    print(body)
    print("=" * 80)
    print(f"📊 統計資訊:")
    print(f"   - 主旨長度: {len(subject)} 字元")
    print(f"   - 正文長度: {len(body)} 字元")
    print(f"   - 總字數: {len(body.split())} 單字")
    print("=" * 80)

def main():
    """主要測試函數"""
    print(" 信件內容測試程式")
    print("這個程式會顯示完整的信件內容，用於測試和檢查")
    print()
    
    # 測試不同類型的信件
    test_cases = [
        ("US", "positive"),
        ("JP", "positive"),
        ("US", "negative"),
        ("DE", "negative")
    ]
    
    for i, (country, email_type) in enumerate(test_cases, 1):
        print(f"\n🔍 測試案例 {i}: {country} 地區 {email_type} 評論")
        print_email_content(country, email_type)
        
        if i < len(test_cases):
            input("\n按 Enter 繼續下一個測試案例...")

if __name__ == "__main__":
    main() 