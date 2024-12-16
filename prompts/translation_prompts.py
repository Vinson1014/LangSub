# prompts/translation_prompts.py

class TranslationPrompts:
    @staticmethod
    def get_translation_prompt(target_language: str, region: str = "") -> str:
        return f"""
You are a professional translation expert.

Your task is to analyze the context of the subtitles before proceeding with the translation. Please follow these steps:

1. **Context Analysis**: Review the provided context to understand the tone, style, and nuances. This includes considering colloquial expressions and potential errors due to speech-to-text conversion. Write down your analysis process.

2. **Translation**: After analyzing the context, accurately translate the source text into {target_language} with precision and care. {"Ensure that the translation aligns with common phrases and the tone used in " +  region + "." if region else ""} 

3. **Output Format**: Provide the translated text in the following YAML format, using double quotes to wrap the text and translation_text and "id" sould represent as integers do not quoted. If any special characters are included in the strings, please escape them with a backslash (e.g., '\"'):

### Context Analysis:
<your analysis process>
### Translation Results:
```yaml
- id: <id of the source text>
  text: "<Source text>"
  translation_text: "<Translated text>"
```

If the source text is empty, leave the translation empty. Ensure the entire input is fully translated, and do not include the original text unless it is part of the translation. 
"""

    @staticmethod
    def get_keyword_extraction_prompt() -> str:
        return """
You are a professional translator and researcher. Your task is to analyze the subtitles of a video. After thoroughly reading the subtitles and understanding their context, identify proper nouns that are widely recognized (e.g., names of well-known works or notable individuals) and record them as keywords for subsequent translation work.

### Output Format:
Please write the output in a YAML code block, formatted as specified. Each entry must have double quotes around the key and value. If there are any special characters in the content, please escape them with a backslash (e.g., (\") to avoid parsing errors).

```yaml
- "name": "<The name or term extracted directly from the subtitles without translation or rewriting.>"
  "reason": "<An explanation for why you believe this is a relevant special name.>"
  "guessing": "<A guess about what type of name it is (e.g., person name, organization name, location name, event name, title of a work, concept, etc.).>"
  "grab_from": "<The original text from which the name was extracted.>"
```

If no special names are identified, return an empty list in a YAML code block:
```yaml
[]
```
"""

    @staticmethod
    def get_context_input_prompt() -> str:
        return """
Here is some reference information about the source text:
{reference}

Here is the context as a reference for translation. Please refer to the context and context for appropriate translation.
{context}

Please translate the following text in YAML format, and output the completed YAML structure in a code block:
```yaml
{input}
```
"""

    @staticmethod
    def get_retry_prompt() -> str:
        return """
Please make sure to present the results in a properly formatted YAML code blockand the content must be in valid YAML format. It is essential that you adhere to all the rules outlined in the instructions. You have already attempted this {retry_times} times.
"""

    @staticmethod
    def get_repair_prompt(original_output: str) -> str:
        return f"""
You are tasked with automatically correcting previously generated output that does not adhere to the required format.

Here is the previous output, which is in the wrong format:
{original_output}

Please adjust it to meet the following criteria:
- The results must be presented within a YAML code block.
- The content must be in valid YAML format.

Now, proceed to correct the output accordingly.
"""

    @staticmethod
    def get_reflection_prompt(target_language: str, region: str, initial_translation: str, reference_info: str) -> str:
        reference_info_str = f"""
Here is some reference information about the source text, delimited by XML tags <REFERENCE></REFERENCE>, are as follows:\n\n<REFERENCE>\n{reference_info}\n</REFERENCE>\n""" if reference_info else ""
        return f"""
You are a professional translation expert.

You will be provided with a source text and its initial translation derived from video subtitles. Your task is to thoroughly review both the source text and its translation in {target_language}, then provide constructive feedback and actionable suggestions for improvement.

The final style and tone of the translation should align with the colloquial style of {target_language} as spoken in {region}.

The source text and initial translation, delimited by XML tags <TEXT></TEXT>, are as follows:

<TEXT>
{initial_translation}
</TEXT>

{reference_info_str}

When crafting your suggestions, please focus on the following areas for potential improvement:
(i) **Accuracy**: Correct any errors related to addition, mistranslation, omission, or untranslated text.
(ii) **Fluency**: Ensure that the translation adheres to {target_language} grammar, spelling, and punctuation rules, and eliminate any unnecessary repetitions.
(iii) **Style**: Make sure the translation reflects the style of the source text and considers any relevant cultural context.
(iv) **Terminology**: Verify that the terminology is consistent, reflects the domain of the source text, and utilizes equivalent idioms in {target_language}.

Please provide a list of specific, helpful, and constructive suggestions for enhancing the translation. Each suggestion should address a distinct aspect of the translation. 

Output only the suggestions without any additional content.
"""

    @staticmethod
    def get_final_translation_system_prompt(target_language: str) -> str:
        return f"""
You are a professional translation expert.

Your task is to thoroughly read the original text (source text), the translation (translation text), and the adjustment suggestions (reflection). Based on the content of the suggestions, you will make necessary adjustments to the translation text. Your work is to translate the original text into {target_language}.

I will provide you with the initial translation and the reflection for your review.

### Output Format:
Please write the adjusted results in a YAML code block. The content must be in valid YAML format, structured as follows (where < > are placeholders):

```yaml
- id: <id of the source text>
  text: "<Source text>"
  translation_text: "<Translated text>"
```

Now, proceed with the analysis and make the appropriate adjustments based on the reflection provided.
"""

    @staticmethod
    def get_final_translation_prompt(initial_translation: str, reflection: str) -> str:
        return f"""
Here is the initial translation:
{initial_translation}

Here is the reflection:
{reflection}

Please translate the following text in YAML format, and output the completed YAML structure in a code block:
"""

if __name__ == "__main__":
    # test code
    pass