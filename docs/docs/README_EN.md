<div align="center">
  <h1>LangSub</h1> 
  <p>
    <a href="README_zh_CN.md">简体中文</a> | 
    <a href="../../README.md">繁體中文</a> | 
    <a href="README_EN.md">English</a>
  </p>
</div>

LangSub-Translation is a subtitle translation tool based on large language models (LLMs), supporting multiple translation modes and several LLM providers (OpenAI, Google, Anthropic, OpenAI Compatible API). It also offers a glossary management feature to ensure consistency and accuracy in translations.

## Features

- **Multi-Mode Translation**
  - Quick Translation: Direct subtitle translation.
  - Detailed Translation: In-depth translation optimization using LLM.
  - Keyword Extraction: Identify and extract important terminology.

- **Supported LLM Providers**
  - OpenAI (GPT Series)
  - Google (Gemini Series)
  - Anthropic (Claude Series)
  - Custom API Support

- **Advanced Features**
  - Glossary Management
  - Context-Aware Translation
  - Translation Progress Tracking

## User Guide
![alt text](/docs/attachments/image.png)

### Basic Translation Process
1. Set up the LLM
2. Choose the subtitle file to translate
3. Select the output destination (default is the same location as the subtitle)
4. Choose the translation mode
5. Set the target language
6. Set the region (optional) to enhance translation localization
7. Start the translation

### Glossary Usage
![alt text](/docs/attachments/image-1.png)
1. Use the keyword extraction feature to analyze subtitles
2. Edit translation pairs in the keyword editing interface
3. The program will automatically apply the glossary for translation

---

## Development

### Environment Requirements
- Python 3.11+

### Development Setup

This project uses **Poetry** to manage dependencies, allowing you to easily install and manage required libraries.

```bash
git clone https://github.com/your-username/langsub.git
poetry shell
poetry install
```

*  `poetry shell`: Creates a virtual environment containing all the dependencies needed for the project.
* `poetry install`: Installs the dependencies required by the project in the virtual environment, based on the settings in the `pyproject.toml` file.

---

## Help

If you have any questions, suggestions, or issues, feel free to raise them in the [Issues](https://github.com/Vinson1014/LangSub/issues) section. Thank you for your contributions!
