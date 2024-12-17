<div align="center">
  <h1>LangSub-朗译</h1> 
  <p>
    <a href="README_zh_CN.md">简体中文</a> | 
    <a href="../../README.md">繁体中文</a> | 
    <a href="README_EN.md">English</a>
  </p>
</div>

LangSub-朗译 是一款基于大型语言模型（LLM）的字幕翻译工具，支持多种翻译模式及多个 LLM 提供者（OpenAI、Google、Anthropic、OpenAI 兼容 API），并拥有术语表管理功能，以确保翻译的一致性和准确性。

## 功能特点

- **多模式翻译**
  - 快速翻译：直接进行字幕翻译。
  - 详细翻译：利用 LLM 进行深度翻译优化。
  - 关键词提取：识别并提取重要术语。

- **LLM 提供者支持**
  - OpenAI (GPT 系列)
  - Google (Gemini 系列)
  - Anthropic (Claude 系列)
  - 自定义 API 支持

- **高级功能**
  - 术语表管理
  - 上下文感知翻译
  - 翻译进度追踪

## 使用指南
![alt text](/docs/attachments/image.png)

### 基本翻译流程
1. 设置 LLM
2. 选择要翻译的字幕文件
3. 选择输出目的地（默认与字幕相同位置）
4. 选择翻译模式
5. 设置目标语言
6. 设置区域（可选）以提升翻译本地化
7. 开始翻译

### 术语表使用
![alt text](/docs/attachments/image-1.png)
1. 使用关键词提取功能分析字幕
2. 在关键词编辑界面中编辑翻译对照
3. 程序会自动套用术语表进行翻译

---

## 开发相关

### 环境需求
- Python 3.11+

### 开发设置

本项目使用 **Poetry** 管理依赖，让你轻松安装和管理所需的库。

```bash
git clone https://github.com/Vinson1014/LangSub.git
poetry shell
poetry install
```

*  `poetry shell`：建立一个包含所有项目需要的环境的虚拟环境。
* `poetry install`：在虚拟环境中安装项目所需的依赖库，根据 `pyproject.toml` 文件中的设置。

---

## 帮助

如果你有任何疑问、建议或问题，欢迎在 [Issues](https://github.com/Vinson1014/LangSub/issues) 中提出。谢谢你的贡献！
