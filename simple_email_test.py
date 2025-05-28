#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡單的信件內容測試程式
快速查看單一信件的完整內容
"""

import os
from datetime import datetime
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def print_single_email():
    """打印單一信件內容"""
    
    # 獲取環境變數
    SENDER_EMAIL = os.getenv("SENDER_EMAIL", "automation@tomofun.com")
    RECEIVER_EMAIL = "amz_reviews_positive@tomofun.com"
    
    # 模擬評論內容
    review_content = """[Dog Camera] – PSP Reviews
• しろねこ (5 stars): "安心"
  > 留守の間も色々お知らせ來るし、おやつが飛ばせるのも良い。ミニと2台持ちで使ってますがとても活躍してます。

• アナ (5 stars): "畫像がきれい！"
  > こんなに鮮明に見れるとは思いませんでした。愛犬の様子が見れて安心。もっと早く買えばよかったです。

[Cat Camera] – SA Reviews
• Amazon カスタマー (5 stars): "無くてはならないです"
  > とても頼りにしてます。無くてはならないです。"""
    
    # 信件基本資訊
    country = "JP"
    today = datetime.now().strftime("%m/%d")
    subject = f"[{country}] Weekly positive feedback collection"
    
    # 完整信件內容
    email_body = f"""Hi Team,

This week's positive feedback summary for Japan as of {today}:

{review_content}

Best,
Automation Bot by Lean"""
    
    # 打印信件
    print("信件內容預覽")
    print("=" * 60)
    print(f"FROM: {SENDER_EMAIL}")
    print(f"TO:   {RECEIVER_EMAIL}")
    print(f"主旨: {subject}")
    print("=" * 60)
    print(email_body)
    print("=" * 60)
    print(f"信件長度: {len(email_body)} 字元")
    print("測試完成！")

if __name__ == "__main__":
    print_single_email() 