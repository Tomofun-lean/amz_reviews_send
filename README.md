# Amazon Reviews Auto-Send (Positive/Negative)

## 專案簡介

本專案提供兩支 Python 腳本，自動整理 Amazon 商品評論（正面/負面），並寄送彙整結果到指定 Email。  


- `review_auto_send_pos.py`：整理「正面」評論並寄送報告
- `review_auto_send_neg.py`：整理「負面」評論並寄送報告

**功能：**
- 自動分析與整理評論內容
- 依據檔案第一行的市場代碼決定地區（支援 US、CA、JP、DE、UK、AU、FR）
- 自動發送格式化郵件

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
JP
しろねこ
5つ星のうち5.0 安心
2025年4月21日に日本でレビュー済み
スタイル: ネコカメラ 単体購入（サブスク任意）
留守の間も色々お知らせ来るし、おやつが飛ばせるのも良い。
...以下評論內容...
```

### 3. 執行腳本

- 寄送正面評論報告：
    ```bash
    python review_auto_send_pos.py
    ```
- 寄送負面評論報告：
    ```bash
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

## 檔案說明

- `review_auto_send_pos.py`  # 正面評論自動摘要 + 寄送
- `review_auto_send_neg.py`  # 負面評論自動摘要 + 寄送
- `environment.yml`      # Conda 環境設定
- `raw_reviews.txt`      # 原始評論資料（須自行建立）
- `.env`                 # 環境配置（須自行建立）