# Amazon Reviews Auto-Send (Positive/Negative)

## 專案簡介

本專案提供兩支 Python 腳本，自動整理 Amazon 商品評論（正面/負面），並寄送彙整結果到指定 Email。  


- `review_auto_send_pos.py`：整理「正面」評論並寄送報告
- `review_auto_send_neg.py`：整理「負面」評論並寄送報告

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

OPENAI_API_KEY=sk-xxxxxxx
SENDER_EMAIL=xxxx@gmail.com
SENDER_PASSWORD=xxxxxxx
RECEIVER_EMAIL=yyyy@tomofun.com


- **注意：Gmail 必須用 [App Password](https://support.google.com/accounts/answer/185833?hl=zh-Hant)，不能用一般登入密碼！**

### 2. 準備評論原始資料

- 將要整理的原始評論內容（全正面或全負面），存為 `raw_reviews.txt`，與主程式放在同一目錄。

### 3. 執行腳本

- 寄送正面評論報告：
    ```bash
    python review_auto_send_pos.py
    ```
- 寄送負面評論報告：
    ```bash
    python review_auto_send_neg.py
    ```

- 成功時，終端機會看到「Email 已寄出到 ...！」

---

## 進階與注意事項

- `.env` 及 `raw_reviews.txt` **已加入 `.gitignore`，勿推送到 git 上**。
- 腳本執行時，會呼叫 OpenAI API（需有網路），API 會產生摘要格式化內容。
- 若要定時自動化（如每週三/五排程寄信），可搭配 crontab 實現。
- 如需改成多收件者，可修改 `RECEIVER_EMAIL`（逗號分隔）。

---

## 檔案說明

- `review_auto_send_pos.py`  # 正面評論自動摘要 + 寄送
- `review_auto_send_neg.py`  # 負面評論自動摘要 + 寄送
- `environment.yml`      # Conda 環境設定

---

## 範例 .env
```
OPENAI_API_KEY=sk-xxxxxxx
SENDER_EMAIL=xxxx@gmail.com
SENDER_PASSWORD=xxxxxxx
RECEIVER_EMAIL=yyyy@tomofun.com
```