import os
import pandas as pd
from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

VALID_LABELS = [
    "Analytical Take",
    "Preference Take",
    "Reactive Take",
]

DATASET_PATH = "data/labeled_dataset.csv"

_client = Groq(api_key=GROQ_API_KEY)


def load_labeled_examples() -> list[dict]:
    """
    Load labeled examples from the project CSV.

    Returns a list of dicts with:
      - "text": the post/comment text
      - "label": the human-assigned label
    """
    if not os.path.exists(DATASET_PATH):
        return []

    df = pd.read_csv(DATASET_PATH)

    labeled = []
    for _, row in df.iterrows():
        text = str(row["text"]).strip()
        label = str(row["label"]).strip()

        if text and label in VALID_LABELS:
            labeled.append({
                "text": text,
                "label": label,
            })

    return labeled


def build_few_shot_prompt(labeled_examples: list[dict], text: str) -> str:
    examples_text = ""

    for example in labeled_examples[:15]:
        examples_text += f"""
---
Post:
{example["text"]}

Label: {example["label"]}
"""

    prompt = f"""
You are classifying r/kpopthoughts posts by discourse type.

Classify the post into exactly one of these three labels:

- Analytical Take: a structured argument supported by specific examples, evidence, comparisons, observations, or detailed reasoning.
- Preference Take: a personal preference, ranking, taste, or subjective opinion rather than evidence-based reasoning.
- Reactive Take: an emotional reaction to a recent event, release, announcement, controversy, or performance.

Use the labeled examples below as demonstrations.

{examples_text}

Now classify this new post:

Post:
{text}

Return your answer exactly in this format:

LABEL: <Analytical Take | Preference Take | Reactive Take>
REASONING: <brief explanation>
"""

    return prompt.strip()


def classify_episode(description: str, labeled_examples: list[dict]) -> dict:
    """
    Classify a single post using the few-shot LLM classifier.
    Kept the function name classify_episode so starter/evaluation code can still call it.
    """
    try:
        prompt = build_few_shot_prompt(labeled_examples, description)

        response = _client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=250,
        )

        response_text = response.choices[0].message.content.strip()

        label = "unknown"
        reasoning = response_text

        for line in response_text.splitlines():
            clean_line = line.strip()

            if clean_line.lower().startswith("label:"):
                parsed = clean_line.split(":", 1)[1].strip()
                parsed = parsed.strip(" .,:;*`\"'")

                for valid_label in VALID_LABELS:
                    if parsed.lower() == valid_label.lower():
                        label = valid_label
                        break

            elif clean_line.lower().startswith("reasoning:"):
                reasoning = clean_line.split(":", 1)[1].strip()

        if label not in VALID_LABELS:
            label = "unknown"
            reasoning = f"Could not parse valid label from response: {response_text}"

        return {
            "label": label,
            "reasoning": reasoning,
        }

    except Exception as e:
        return {
            "label": "unknown",
            "reasoning": f"Classifier error: {e}",
        }