# Classifier Spec — TakeMeter K-pop Discourse Classifier

Complete this spec before writing or updating classifier code for Project 3.

This classifier is for labeling r/kpopthoughts posts by discourse type. The labels must match the labels in `data/labeled_dataset.csv`.

---

## build_few_shot_prompt(labeled_examples, text)

### What it does

Constructs a prompt string for the LLM that includes the task instructions, labeled examples from the dataset, and the new post text to classify.

### Inputs

| Parameter          | Type         | Description                                                                               |
| ------------------ | ------------ | ----------------------------------------------------------------------------------------- |
| `labeled_examples` | `list[dict]` | Each dict has `"text"` and `"label"`. These are examples from `data/labeled_dataset.csv`. |
| `text`             | `str`        | The post or comment text to classify.                                                     |

### Output

| Return value | Type  | Description                                        |
| ------------ | ----- | -------------------------------------------------- |
| prompt       | `str` | A complete prompt string ready to send to the LLM. |

---

## Labels

The classifier must return exactly one of these labels:

* `Analytical Take`
* `Preference Take`
* `Reactive Take`

### Analytical Take

A post that makes a structured argument supported by specific examples, evidence, comparisons, observations, or detailed reasoning.

### Preference Take

A post that primarily expresses a personal preference, ranking, taste, or subjective opinion rather than evidence-based reasoning.

### Reactive Take

A post that primarily expresses an emotional reaction to a recent event, release, announcement, controversy, or performance.

---

## build_few_shot_prompt Spec Fields

### Task instruction

```text
You are classifying r/kpopthoughts posts by discourse type.

Classify the post into exactly one of these three labels:

- Analytical Take: a structured argument supported by specific examples, evidence, comparisons, observations, or detailed reasoning.
- Preference Take: a personal preference, ranking, taste, or subjective opinion rather than evidence-based reasoning.
- Reactive Take: an emotional reaction to a recent event, release, announcement, controversy, or performance.

Return only a label and brief reasoning. Do not invent new labels.
```

### How labeled examples should be formatted

Each labeled example should include the post text and the correct label. Examples should be separated by a delimiter such as `---`. The examples should come from the labeled dataset and should show the model what each label looks like.

### Example block sketch

```text
---
Post:
{text}

Label: {label}
```

### How the new post should be presented

The new post should be presented in the same format as the examples, but without a filled-in label:

```text
Now classify this new post:

Post:
{text}
```

Then the prompt should request the exact output format below.

### Output format requested from the LLM

```text
LABEL: <Analytical Take | Preference Take | Reactive Take>
REASONING: <brief explanation>
```

I chose this two-line structured format because it is easier to parse reliably than a paragraph and less fragile than JSON. JSON is more structured, but an LLM can accidentally add extra text or invalid formatting. A label-only response would be easiest to parse, but reasoning is useful for debugging and failure analysis.

### Edge cases to handle in the prompt

If `labeled_examples` is empty, the prompt should still include the label definitions and ask the model to classify using those definitions. If the post text is very short, the model should make the best classification using the available evidence and return one of the three labels. The model should not create an "other" category.

---

## classify_episode(text, labeled_examples)

### What it does

Classifies a single r/kpopthoughts post using the few-shot LLM classifier. The function name may remain `classify_episode` if starter or evaluation code expects that name, but the content being classified is a post, not a podcast episode.

### Inputs

| Parameter          | Type         | Description                                              |
| ------------------ | ------------ | -------------------------------------------------------- |
| `text`             | `str`        | The post or comment text to classify.                    |
| `labeled_examples` | `list[dict]` | Labeled examples loaded from `data/labeled_dataset.csv`. |

### Output

| Return value | Type   | Description                                                                                                 |
| ------------ | ------ | ----------------------------------------------------------------------------------------------------------- |
| result       | `dict` | Must have keys `"label"` and `"reasoning"`. `"label"` must be one of the three valid labels or `"unknown"`. |

---

## classify_episode Spec Fields

### Step 1 — Build the prompt

Call `build_few_shot_prompt(labeled_examples, text)` and store the returned string in a variable called `prompt`.

### Step 2 — Send to the LLM

Call `_client.chat.completions.create()` with:

* `model`: the Groq model name
* `messages`: `[{"role": "user", "content": prompt}]`
* `max_tokens`: about 200–300

Extract the raw response text from:

```python
response.choices[0].message.content
```

### Step 3 — Parse the response

Split the response into lines. Look for a line that starts with `LABEL:` and extract the text after the colon. Strip whitespace, punctuation, markdown symbols, and compare case-insensitively against the valid labels.

For reasoning, look for a line that starts with `REASONING:` and extract the text after the colon. If there is no reasoning line, use the raw response as the reasoning for debugging.

### Step 4 — Validate the label

After parsing, compare the label against:

```python
["Analytical Take", "Preference Take", "Reactive Take"]
```

If the parsed label matches one of these labels case-insensitively, return the official label spelling. If it does not match, set the label to `"unknown"` and include the raw response in the reasoning.

### Step 5 — Handle errors gracefully

Possible errors include:

* missing API key
* network/API error
* empty response
* unexpected response format
* invalid label

The function should catch exceptions and return:

```python
{
    "label": "unknown",
    "reasoning": "Classifier error: <error message>"
}
```

This prevents one bad response from crashing the full evaluation run.

---

## Return value structure

```python
{
    "label": str,
    "reasoning": str,
}
```

---

## Notes on label quality

The classifier is only as good as the dataset labels. The current dataset is imbalanced, with more Analytical Take examples than Preference Take or Reactive Take examples, so evaluation should include per-class metrics such as precision, recall, and F1 score instead of relying only on accuracy.

---

## Implementation Notes

*Fill this in after implementing and testing both functions.*

**Test: what does the raw LLM response look like for one episode?**

```
Episode tested: [title]
Raw response text: [paste it here]
```

**How did you parse the label out of the response?**

```
[describe the string operations — strip, split, lower, etc.]
```

**Did any episodes return `"unknown"`? If so, why?**

```
[yes / no — if yes, what did the raw response look like?]
```

**One thing about the output format that surprised you:**

```
[your answer here]
```
