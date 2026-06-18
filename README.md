# AI201 Project 3 — TakeMeter

## Overview

This project explores text classification within the r/kpopthoughts community. The goal was to create a label taxonomy that captures meaningful differences in discussion styles, collect and annotate a dataset, fine-tune a machine learning classifier, and compare its performance against a zero-shot large language model baseline.

The project investigates whether a fine-tuned DistilBERT model can learn to distinguish between different types of K-pop discourse and whether fine-tuning provides an advantage over a powerful general-purpose language model.

---

# Community

I selected **r/kpopthoughts** because it is a large and active online community with highly varied discussion styles. Members post detailed analyses of artists and industry trends, personal preferences about music and performers, and emotional reactions to comebacks, controversies, and performances.

This variety makes the community a strong classification task because users naturally engage in several distinct forms of discourse that can be separated into meaningful categories.

---

# Label Taxonomy

The classifier predicts one of three labels.

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

## Labeling Process

Each example was manually reviewed and assigned one of three labels: Analytical Take, Preference Take, or Reactive Take. Labels were assigned according to the definitions established in planning.md. Ambiguous examples were reviewed using the edge-case rules developed during the planning phase to ensure consistency across the dataset.

## Dataset Size

* 202 labeled examples

## Label Distribution

| Label           | Count |
| --------------- | ----: |
| Analytical Take |   123 |
| Preference Take |    52 |
| Reactive Take   |    27 |

The dataset is somewhat imbalanced, with Analytical Take examples representing the majority class.

---

# Difficult Annotation Cases

## Example 1

> "I think this group has the strongest stage presence because they seem more confident than others."

Potential labels:

* Analytical Take
* Preference Take

Decision:

* Preference Take

Reasoning:

The post expresses a subjective judgment despite including a brief explanation.

---

## Example 2

> "I loved the comeback because the concept feels more mature."

Potential labels:

* Reactive Take
* Preference Take

Decision:

* Reactive Take

Reasoning:

The focus is on an immediate emotional response to the release.

---

## Example 3

> "This group is declining because their recent songs are weaker."

Potential labels:

* Analytical Take
* Preference Take

Decision:

* Preference Take

Reasoning:

The statement presents an opinion without sufficient evidence to form a structured argument.

---

# Model Training

## Base Model

```text
distilbert-base-uncased
```

from Hugging Face.

## Training Environment

* Google Colab
* T4 GPU

## Training Approach

The dataset was automatically split into training, validation, and test sets using the notebook pipeline. DistilBERT was fine-tuned as a three-class sequence classification model.

## Key Hyperparameters

* Model: DistilBERT
* Task: Sequence Classification
* Labels: 3
* Epochs: 3
* Learning Rate: 2e-5
* Batch Size: 16

---

# Zero-Shot Baseline

A baseline classifier was created using:

```text llama-3.3-70b-versatile
```

through Groq.

## Baseline Prompt

The zero-shot baseline used Groq's `llama-3.3-70b-versatile` model. The model was provided with definitions for the three labels and instructed to classify each post into exactly one category without any task-specific training.

### Prompt Summary

* **Analytical Take:** a structured argument supported by evidence, comparisons, observations, or detailed reasoning.
* **Preference Take:** a personal preference, ranking, taste, or subjective opinion rather than evidence-based reasoning.
* **Reactive Take:** an emotional reaction to a recent event, release, announcement, controversy, or performance.

The model classified every example in the test set using only these instructions. The resulting predictions were compared directly against the fine-tuned DistilBERT model on the same test set to determine whether fine-tuning improved performance.

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

The baseline model slightly outperformed the fine-tuned model on the test set.

---

# Confusion Matrix

The confusion matrix generated during evaluation is included in:

```text
confusion_matrix.png
```

The matrix shows that the model frequently predicted the majority class, Analytical Take, for examples that belonged to Preference Take and Reactive Take.

---

# Sample Classifications

| Example                                                                                               | Predicted Label | Confidence |
| ----------------------------------------------------------------------------------------------------- | --------------- | ---------- |
| "I would give credit to the live band. They were amazing and I loved the jazz they added to the set." | Analytical Take | 0.36       |
| "The song was cool but the Macarena bit ruined it for me."                                            | Analytical Take | 0.36       |
| "I always keep my expectations low about releases I am looking forward to."                           | Analytical Take | 0.37       |
| "Atmos is simply pop music perfection. I have been listening to the album nonstop since it came out." | Analytical Take | 0.38       |

These examples demonstrate the model's tendency to classify subjective opinions and emotional reactions as Analytical Take.

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

## Error Example 1

**True Label:** Preference Take

> "I would give credit to the live band. They were amazing and I loved the jazz they added to the set."

**Predicted:** Analytical Take

**Reason:**

The model appears to interpret explanatory language as evidence-based analysis.

---

## Error Example 2

**True Label:** Preference Take

> "The song was cool but the Macarena bit ruined it for me."

**Predicted:** Analytical Take

**Reason:**

The model struggled to distinguish subjective opinions from structured arguments.

---

## Error Example 3

**True Label:** Reactive Take

> "Atmos is simply pop music perfection. I have been listening to the album nonstop since it came out."

**Predicted:** Analytical Take

**Reason:**

Strong emotional reactions sometimes contain descriptive language that resembles analytical discussion.

---

# Systematic Error Pattern

The most common failure mode was overpredicting the majority class:

```text
Analytical Take
```

Possible causes include:

1. Class imbalance in the training data.
2. Overlap between Preference Take and Analytical Take examples.
3. Small dataset size.
4. Short post length providing limited context.

The confusion matrix and incorrect predictions suggest that the classifier learned broad discussion patterns but did not learn the finer distinctions between subjective opinions and emotional reactions.

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

# Spec Reflection

The classifier specification helped guide implementation by requiring label definitions and edge-case rules before annotation began. This made the labeling process more consistent and provided clear decision boundaries during dataset creation.

One way the implementation diverged from the original plan was the final label distribution. The planning document initially targeted a balanced dataset, but the final dataset reflected the natural distribution of discourse within the community. This likely contributed to the model's tendency to predict the majority class.

---

# AI Usage

## AI Usage Example 1

I used ChatGPT to review and refine label definitions before annotation. The AI generated examples near the boundary between labels, helping identify situations where distinctions were unclear. I revised label definitions after reviewing these examples.

## AI Usage Example 2

I used ChatGPT during evaluation and failure analysis. After reviewing incorrect predictions, I asked the AI to identify possible error patterns. The AI suggested class imbalance and overlap between Preference Take and Analytical Take examples. I verified these observations manually using the confusion matrix and misclassified examples before including them in the report.

---

# Files Included

* planning.md
* README.md
* data/labeled_dataset.csv
* evaluation_results.json
* confusion_matrix.png

---

# Reflection

This project demonstrated that label design and annotation quality are often more important than model architecture. Although the fine-tuned model did not outperform the zero-shot baseline, the results provided valuable insight into how class imbalance and ambiguous label boundaries affect model behavior.

The most important lesson was that a model learns the patterns present in the labels and examples provided, which may differ from the distinctions the designer intended. The project reinforced the importance of careful annotation, balanced datasets, and clear label definitions when building classification systems.
