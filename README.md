# AI201 Project 3 — TakeMeter

## Overview

This project explores text classification within the r/kpopthoughts community. The goal was to create a label taxonomy that captures meaningful differences in discussion styles, collect and annotate a dataset, fine-tune a machine learning classifier, and compare its performance against a zero-shot large language model baseline.

The project investigates whether a fine-tuned DistilBERT model can learn to distinguish between different types of K-pop discourse and whether fine-tuning provides an advantage over a powerful general-purpose language model.

---

# Community

I selected **r/kpopthoughts** because it is a large and active online community with highly varied discussion styles. Posts range from detailed analyses of artists and industry trends to personal preferences and emotional reactions to releases, controversies, and performances.

This diversity makes it a strong classification problem because community members naturally engage in several different forms of discourse that can be separated into meaningful categories.

---

# Label Taxonomy

The classifier predicts one of three labels:

## Analytical Take

A post that makes a structured argument supported by evidence, comparisons, observations, or detailed reasoning.

### Examples

* "Comparing album sales from 2019–2025 shows that fourth-generation groups are growing internationally faster than previous generations."
* "Looking at chart performance and concert attendance together provides a better measure of popularity than album sales alone."

---

## Preference Take

A post that primarily expresses a personal preference, ranking, taste, or subjective opinion rather than evidence-based reasoning.

### Examples

* "I prefer BTS's earlier albums because their sound felt more authentic to me."
* "This is my favorite comeback of the year even though it wasn't the most successful commercially."

---

## Reactive Take

A post that primarily expresses an emotional reaction to a recent event, release, announcement, controversy, or performance.

### Examples

* "I can't believe the comeback teaser just dropped. I'm so excited."
* "That award show performance was incredible. I watched it three times."

---

# Data Collection

## Source

All examples were collected from publicly available posts and comments from:

* r/kpopthoughts

## Dataset Size

Total examples:

* 202 labeled examples

## Label Distribution

| Label           | Count |
| --------------- | ----: |
| Analytical Take |   123 |
| Preference Take |    52 |
| Reactive Take   |    27 |

---

# Difficult Annotation Cases

Several examples were difficult to label because the boundaries between discourse types are not always clear.

### Example 1

> "I think this group has the strongest stage presence because they seem more confident than others."

Potential labels:

* Analytical Take
* Preference Take

Decision:

* Preference Take

Reasoning:

The post primarily expresses a subjective judgment despite including a brief explanation.

---

### Example 2

> "I loved the comeback because the concept feels more mature."

Potential labels:

* Reactive Take
* Preference Take

Decision:

* Reactive Take

Reasoning:

The focus is on an immediate emotional reaction to the release.

---

### Example 3

> "This group is declining because their recent songs are weaker."

Potential labels:

* Analytical Take
* Preference Take

Decision:

* Preference Take

Reasoning:

The statement presents a personal opinion without sufficient evidence to form a structured argument.

---

# Model Training

## Base Model

The project uses:

```text
distilbert-base-uncased
```

from Hugging Face.

## Training Environment

* Google Colab
* T4 GPU

## Training Approach

The labeled dataset was split into:

* Training set
* Validation set
* Test set

The DistilBERT model was fine-tuned as a three-class text classifier.

## Key Hyperparameters

* Model: DistilBERT
* Task: Sequence Classification
* Labels: 3
* Epochs: notebook default
* Learning rate: notebook default
* Batch size: notebook default

---

# Zero-Shot Baseline

A baseline classifier was created using:

```text
llama-3.3-70b-versatile
```

through Groq.

The model received the label definitions and classified each test example without task-specific training.

This baseline provides a comparison point to determine whether fine-tuning improved performance.

---

# Evaluation Results

## Accuracy Comparison

| Model                   | Accuracy |
| ----------------------- | -------: |
| Groq Zero-Shot Baseline |    0.645 |
| Fine-Tuned DistilBERT   |    0.613 |

### Result

Fine-tuning resulted in a small regression:

```text
-0.032
```

relative to the zero-shot baseline.

---

# Confusion Matrix

See:

```text
confusion_matrix.png
```

for the full confusion matrix visualization.

---

# Error Analysis

The fine-tuned model made 12 incorrect predictions out of 31 test examples.

A common pattern was predicting:

```text
Analytical Take
```

for examples that were actually:

* Preference Take
* Reactive Take

### Example 1

**True Label:** Preference Take

> "I would give credit to the live band. They were amazing and I loved the jazz they added to the set."

**Predicted:** Analytical Take

Reason:

The model appears to interpret explanatory language as evidence-based analysis.

---

### Example 2

**True Label:** Preference Take

> "The song was cool but the Macarena bit ruined it for me."

**Predicted:** Analytical Take

Reason:

The model struggled to distinguish subjective opinions from structured arguments.

---

### Example 3

**True Label:** Reactive Take

> "Atmos is simply pop music perfection. I have been listening to the album nonstop since it came out."

**Predicted:** Analytical Take

Reason:

Strong emotional reactions sometimes contain descriptive language that resembles analytical discussion.

---

# Systematic Error Pattern

The model frequently predicted the majority class:

```text
Analytical Take
```

for minority-class examples.

Possible causes include:

1. Class imbalance
2. Overlap between label definitions
3. Limited dataset size
4. Short post lengths that provide limited context

---

# What the Model Learned vs. What I Intended

My goal was for the classifier to distinguish between:

* evidence-based reasoning
* personal preferences
* emotional reactions

However, the model primarily learned to identify Analytical Take examples and struggled to separate Preference Take and Reactive Take posts.

This suggests that the model learned broad linguistic patterns associated with discussion rather than the more subtle distinctions represented by the label taxonomy.

The results highlight how important dataset balance and precise label boundaries are in classification tasks.

---

# Files Included

* `planning.md`
* `data/labeled_dataset.csv`
* `evaluation_results.json`
* `confusion_matrix.png`
* `README.md`

---

# Reflection

This project demonstrated that label design and annotation quality are often more important than model architecture. Although the fine-tuned model did not outperform the zero-shot baseline, the results provided valuable insight into how class imbalance and ambiguous label boundaries affect model behavior.

The most important lesson was that a model learns the patterns present in the labels and examples provided, which may differ from the distinctions the designer intended.

