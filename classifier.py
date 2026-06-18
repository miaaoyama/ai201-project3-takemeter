import json
import os
from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL, VALID_LABELS, DATA_PATH, TRAIN_FILE, LABELS_FILE

_client = Groq(api_key=GROQ_API_KEY)


def load_labeled_examples() -> list[dict]:
    """
    Load the training episodes and merge them with the student's labels.

    Returns a list of dicts, each with:
      - "id"          : episode ID
      - "title"       : episode title
      - "podcast"     : podcast name
      - "description" : episode description
      - "label"       : the label from my_labels.json (may be None if not yet annotated)

    Only returns episodes where the label is a valid, non-null string.
    Episodes with null labels are silently skipped.
    """
    train_path = os.path.join(DATA_PATH, TRAIN_FILE)
    labels_path = os.path.join(DATA_PATH, LABELS_FILE)

    with open(train_path, encoding="utf-8") as f:
        episodes = {ep["id"]: ep for ep in json.load(f)}

    with open(labels_path, encoding="utf-8") as f:
        labels = {entry["id"]: entry["label"] for entry in json.load(f)}

    labeled = []
    for ep_id, ep in episodes.items():
        label = labels.get(ep_id)
        if label in VALID_LABELS:
            labeled.append({**ep, "label": label})

    return labeled


def build_few_shot_prompt(labeled_examples: list[dict], description: str) -> str:
    examples_text = ""

    for example in labeled_examples:
        examples_text += f"""
            ---
            Title: {example["title"]}
            Description: {example["description"]}
            Label: {example["label"]}
            """

    prompt = f"""
            You are classifying podcast episodes by their format. Classify the episode
            into exactly one of these four labels:

            - interview: a conversation between a host and one or more guests
            - solo: a single host speaking from memory, experience, or opinion — no guests,
              no assembled external sources
            - panel: multiple guests with roughly equal speaking time, often debating or
              discussing a topic together
            - narrative: a story assembled from external sources — interviews, archival
              audio, reporting — with a clear narrative arc

            Use the labeled examples below as demonstrations.

{examples_text}

            Now classify this episode:

            Description: {description}

            Return your answer exactly in this format:

            LABEL: <interview | solo | panel | narrative>
            REASONING: <brief explanation>
            """

    return prompt.strip()


def classify_episode(description: str, labeled_examples: list[dict]) -> dict:
    """
    Classify a single podcast episode description using the few-shot LLM classifier.
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
                label = clean_line.split(":", 1)[1].strip().lower()
                label = label.strip(" .,:;*`\"'")

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