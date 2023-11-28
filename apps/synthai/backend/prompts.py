MAP_PROMPT_EN = """
You will be given a single piece of an article. This section will be enclosed in triple backticks (```)
Your goal is to give a summary of this section so that a reader will have a full understanding of what happened.
Your response should be at least three paragraphs and fully encompass what was said in the passage.

```{text}```
FULL SUMMARY:
"""

MAP_PROMPT_ES = """
Se te dara una seccion de un articulo. Esta seccion estara encerrada en triple backticks (```)
Tu objetivo es dar un resumen de esta seccion para que el lector tenga un entendimiento completo de lo que paso.
Tu respuesta debe ser de al menos tres parrafos y abarcar completamente lo dicho en el pasaje.

```{text}```
RESUMEN COMPLETO:
"""

COMBINE_PROMPT_ES = """
Se te dara una serie de resumenes de un articulo. Los resumenes estaran encerrados en triple backticks (```)
Tu objetivo es dar un resumen extenso de lo que paso en la historia.
El lector debe ser capaz de entender de que trata el articulo.

```{text}```
RESUMEN EXTENSO:
"""

COMBINE_PROMPT_EN = """
You will be given a series of summaries from an article. The summaries will be enclosed in triple backticks (```)
Your goal is to give a verbose summary of what happened in the story.
The reader should be able to grasp what the article is about.

```{text}```
VERBOSE SUMMARY:
"""
