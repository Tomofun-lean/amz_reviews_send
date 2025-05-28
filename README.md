# Amazon Reviews Auto-Send (Positive/Negative)

## 專案簡介

本專案提供兩支 Python 腳本，自動整理 Amazon 商品評論（正面/負面），並寄送彙整結果到指定 Email。  

**主要程式：**
- `review_auto_send_pos.py`：整理「正面」評論並寄送報告
- `review_auto_send_neg.py`：整理「負面」評論並寄送報告

**測試程式：**
- `test_real_reviews.py`：測試 `raw_reviews.txt` 內容並預覽完整信件
- `simple_email_test.py`：快速預覽單一信件內容
- `test_email_content.py`：多類型信件內容測試

**功能：**
- 自動分析與整理評論內容
- 依據檔案第一行的市場代碼決定地區（支援 US、CA、JP、DE、UK、AU、FR）
- 自動發送格式化郵件
- 提供完整的測試和預覽功能

---

## 環境需求

- Python 3.10 以上
- 建議使用 [conda](https://docs.conda.io/en/latest/) 管理虛擬環境

### 安裝方式

1. 建立 conda 環境：
    ```bash
    conda env create -f environment.yml
    conda activate amz_reviews_send
    ```

2. （若未使用 conda，可用 pip）
    ```bash
    pip install -r requirements.txt
    ```

---

## 📧 信件內容測試

在實際發送信件之前，建議先使用測試程式預覽信件內容：

### 1. 測試實際評論檔案
```bash
python test_real_reviews.py
```
**功能：**
- 讀取 `raw_reviews.txt` 檔案
- 模擬 OpenAI 處理流程
- 顯示完整的信件內容預覽
- 提供原始內容對比

### 2. 快速信件預覽
```bash
python simple_email_test.py
```
**功能：**
- 快速查看單一信件格式
- 不需要 raw_reviews.txt 檔案
- 適合格式驗證

### 3. 多類型測試
```bash
python test_email_content.py
```
**功能：**
- 測試不同地區的信件格式
- 測試正面/負面評論格式
- 互動式選單操作

---

## 使用說明

### 1. 準備 `.env` 檔案（**勿上傳 Github**）

在專案根目錄建立 `.env` 檔，格式如下：

```
OPENAI_API_KEY= OpenAI金鑰
SENDER_EMAIL= 寄件人信箱
SENDER_PASSWORD= 寄件人信箱密碼或應用程式密碼
```

- **RECEIVER_EMAIL 不需設定，程式會自動根據腳本名稱決定收件人：**
    - 執行 `review_auto_send_pos.py` 會寄到 `amz_reviews_positive@tomofun.com`
    - 執行 `review_auto_send_neg.py` 會寄到 `amz_reviews_negative@tomofun.com`

- **注意：Gmail 必須用 [App Password](https://support.google.com/accounts/answer/185833?hl=zh-Hant)，不能用一般登入密碼！**

### 2. 準備評論原始資料

- 準備 `raw_reviews.txt` 檔案，放在與主程式相同目錄下
- **第一行必須為市場代碼**（如 US、JP、CA 等）
- 從第二行開始寫入原始評論內容

例如：
```
US
Victoria Nerkowski
5.0 out of 5 stars Great product
Reviewed in the United States on May 21, 2025
Style: Dog Cam (No Subscription Required)Verified Purchase
I bought this for a wedding shower gift and it was a big hit! She just got a new puppy and is a nervous new dog mom so she loved this. The treat aspect is also a nice touch. Highly recommend
```

### 3. 測試與執行流程

**建議流程：**

1. **先測試信件內容**：
   ```bash
   python test_real_reviews.py
   ```
   確認信件格式和內容正確

2. **執行實際發送**：
   ```bash
   # 寄送正面評論報告
   python review_auto_send_pos.py
   
   # 或寄送負面評論報告
   python review_auto_send_neg.py
   ```

- 程式執行時會顯示詳細的處理步驟及進度，方便調試
- 成功時，終端機會看到「Email 已寄出到 ...！」的訊息

---

## 支援的市場代碼

系統目前支援以下地區的市場代碼：

- US：美國（United States）
- CA：加拿大（Canada）
- JP：日本（Japan）
- DE：德國（Germany）
- UK：英國（United Kingdom）
- AU：澳洲（Australia）
- FR：法國（France）

在 `raw_reviews.txt` 的第一行填入對應的市場代碼，程式會自動處理該地區的評論。

---

## 測試模式

腳本內建測試模式（`TEST_MODE = True`），在此模式下：

- 即使 OpenAI API 呼叫失敗，仍會嘗試發送郵件
- 使用預設的範例評論內容進行測試
- 提供詳細的錯誤診斷訊息

若要關閉測試模式，可將程式碼中的 `TEST_MODE` 變數設為 `False`。

---

## 進階與注意事項

- `.env` 及 `raw_reviews.txt` **已加入 `.gitignore`，勿推送到 git 上**。
- 腳本執行時，會呼叫 OpenAI API（需有網路），API 會產生摘要格式化內容。
- 若要定時自動化（如每週三/五排程寄信），可搭配 crontab 實現。
- 如需改成多收件者，可修改 `RECEIVER_EMAIL`（逗號分隔）。
- 若程式沒有輸出，建議檢查：
  1. `.env` 檔案是否正確設置
  2. `raw_reviews.txt` 檔案是否存在且第一行包含有效的市場代碼
  3. 執行程式前確認已啟動正確的虛擬環境

---

## 📁 檔案說明

**主要程式：**
- `review_auto_send_pos.py`  # 正面評論自動摘要 + 寄送
- `review_auto_send_neg.py`  # 負面評論自動摘要 + 寄送

**測試程式：**
- `test_real_reviews.py`     # 測試 raw_reviews.txt 內容與信件預覽
- `simple_email_test.py`     # 快速信件內容預覽
- `test_email_content.py`    # 多類型信件測試

**設定檔：**
- `environment.yml`          # Conda 環境設定
- `raw_reviews.txt`          # 原始評論資料（須自行建立）
- `.env`                     # 環境配置（須自行建立）

---

## 🔍 測試範例

使用 `test_real_reviews.py` 測試時，您會看到：

```
🧪 實際評論檔案測試
======================================================================
✅ 成功讀取評論檔案
   📍 市場代碼: US
   📊 評論內容長度: 1571 字元
   🔍 評論內容預覽: Victoria Nerkowski...

🤖 模擬 OpenAI 處理 US 地區評論...
✅ 處理完成，結果長度: 1033 字元

📧 生成的信件內容
======================================================================
📤 寄件人: it@tomofun.com
📥 收件人: amz_reviews_positive@tomofun.com
📋 主旨: [US] Weekly positive feedback collection
======================================================================
📝 信件正文:
----------------------------------------------------------------------
Hi Team,

This week's positive feedback summary for United States as of 05/28:

[Dog Camera] – SA Reviews
• Victoria Nerkowski (5 stars): "Great product"
  > I bought this for a wedding shower gift and it was a big hit!...
```

這樣您就可以在實際發送前確認所有內容都正確無誤！