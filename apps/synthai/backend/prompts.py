MAP_PROMPT_EN = """
You will be given a single piece of an article. This section will be enclosed in triple backticks (```)
Your goal is to give a summary of this section so that a reader will have a full understanding of what happened.
Your response should be at least three paragraphs and fully encompass what was said in the passage.

```{text}```
FULL SUMMARY:
"""
COMBINE_PROMPT_EN = """
You will be given a series of summaries from an article. The summaries will be enclosed in triple backticks (```)
Your goal is to give a verbose summary of what happened in the story.
The reader should be able to grasp what the article is about.

```{text}```
VERBOSE SUMMARY:
"""
