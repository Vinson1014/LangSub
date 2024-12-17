<div align="center">
  <h1>LangSub-朗譯</h1> 
  <p>
    <a href="/docs/docs/README_zh_CN.md">简体中文</a> | 
    <a href="README.md">繁體中文</a> | 
    <a href="/docs/docs/README_EN.md">English</a>
  </p>
</div>

LangSub-朗譯 是一款基於大型語言模型（LLM）的字幕翻譯工具，支援多種翻譯模式及多個 LLM 提供者（OpenAI、Google、Anthropic、OpenAI 兼容 API），並擁有術語表管理功能，以確保翻譯的一致性和準確性。

## 功能特點

- **多模式翻譯**
  - 快速翻譯：直接進行字幕翻譯。
  - 詳細翻譯：利用 LLM 進行深度翻譯優化。
  - 關鍵字提取：識別並提取重要術語。

- **LLM 提供者支援**
  - OpenAI (GPT 系列)
  - Google (Gemini 系列)
  - Anthropic (Claude 系列)
  - 自訂 API 支援

- **進階功能**
  - 術語表管理
  - 上下文感知翻譯
  - 翻譯進度追蹤

## 使用指南
![alt text](/docs/attachments/image.png)

### 基本翻譯流程
1. 設定 LLM
2. 選擇要翻譯的字幕檔
3. 選擇輸出目的地（預設為與字幕相同位置）
4. 選擇翻譯模式
5. 設定目標語言
6. 設定區域（可選）以提升翻譯本地化
7. 開始翻譯

### 術語表使用
![alt text](/docs/attachments/image-1.png)
1. 使用關鍵字提取功能分析字幕
2. 在關鍵字編輯介面中編輯翻譯對照
3. 程式會自動套用術語表進行翻譯

---

## 開發相關

### 環境需求
- Python 3.11+

### 開發設定

本專案使用 **Poetry** 管理依賴，讓你輕鬆安裝和管理所需的程式庫。

```bash
git clone https://github.com/your-username/langsub.git
poetry shell
poetry install
```

*  `poetry shell`：建立一個包含所有專案需要的環境的虛擬環境。
* `poetry install`：在虛擬環境中安裝專案所需的依賴程式庫，根據 `pyproject.toml` 文件中的設定。

---

## 幫助

如果你有任何疑問、建議或問題，歡迎在 [Issues](https://github.com/Vinson1014/LangSub/issues) 中提出。謝謝你的貢獻！
