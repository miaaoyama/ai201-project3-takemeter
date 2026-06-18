# Planning

## Community

I chose r/kpopthoughts because it is a large, active community with a wide variety of discussion styles. Members post detailed analyses of artists and industry trends, emotional reactions to news, controversial opinions, and questions for other fans. This variety makes it a strong candidate for a classification task because the discourse naturally falls into several distinct categories.

## Labels

### analysis

A post that makes a structured argument supported by specific examples, evidence, comparisons, statistics, or detailed reasoning.

**Example 1:** "Comparing album sales from 2019–2025 shows that fourth-generation groups are growing internationally faster than previous generations."

**Example 2:** "Looking at chart performance and concert attendance together provides a better measure of popularity than album sales alone."

**Uncertain example:** "I think this group has the strongest stage presence because they seem more confident than others."

---

### hot_take

A strong opinion presented with little or no supporting evidence.

**Example 1:** "This is the most overrated group in K-pop right now."

**Example 2:** "Every company should stop debuting trainees before age eighteen."

**Uncertain example:** "This group is declining because their recent songs are weaker."

---

### reaction

A post that primarily expresses an emotional response to a recent event, release, announcement, controversy, or performance.

**Example 1:** "I can't believe the comeback teaser just dropped. I'm so excited."

**Example 2:** "That award show performance was incredible. I watched it three times."

**Uncertain example:** "I loved the comeback because the concept feels more mature."

---

### question

A post whose primary purpose is requesting information, recommendations, opinions, or discussion from the community.

**Example 1:** "Which groups have the strongest live vocals?"

**Example 2:** "What are some underrated B-sides I should listen to?"

**Uncertain example:** "Am I the only one who thinks this comeback was disappointing?"

## Hard Edge Cases

The hardest edge case will be distinguishing between analysis and hot_take. Many users include one or two pieces of evidence when expressing a strong opinion. My decision rule will be: if the evidence forms a genuine argument that could stand on its own without the opinionated language, label it analysis. If the evidence is minimal, selective, or primarily used to support a bold claim, label it hot_take.

Another difficult edge case is reaction versus analysis. If the post focuses primarily on feelings or immediate impressions, it will be labeled reaction. If it develops a structured argument using evidence, it will be labeled analysis.

## Data Collection Plan

I will collect approximately 200 posts from r/kpopthoughts using publicly available posts. My target distribution is:

* Analysis: 50 posts
* Hot Take: 50 posts
* Reaction: 50 posts
* Question: 50 posts

If one category is underrepresented, I will intentionally search for additional examples using relevant keywords and post types to create a more balanced dataset.

## Evaluation Metrics

I will use:

* Accuracy: measures overall correctness.
* Precision: measures how often predictions for a label are correct.
* Recall: measures how many examples of a label are successfully found.
* F1 Score: balances precision and recall.

Accuracy alone is insufficient because a model could achieve high accuracy by overpredicting the largest class. Precision, recall, and F1 score provide a better understanding of performance across all labels.

## Definition of Success

I would consider the classifier successful if it achieves:

* Accuracy of at least 80%
* F1 score of at least 0.75 for each label
* No label with recall below 70%

For a real community tool, this level of performance would be useful for organizing discussions, surfacing high-quality content, and identifying different discussion types while still allowing human moderation for difficult cases.

## AI Tool Plan

### Label Stress-Testing

I will provide my label definitions and edge case rules to an AI tool and ask it to generate 5–10 posts that sit at the boundary between labels. If I cannot confidently classify those examples, I will revise my label definitions before annotation begins.

### Annotation Assistance

I may use an LLM to generate suggested labels for a subset of examples before reviewing them manually. Any AI-assisted labels will be reviewed and corrected by me before being added to the dataset. I will keep track of which examples were initially labeled by AI.

### Failure Analysis

After evaluation, I will provide misclassified examples to an AI tool and ask it to identify common failure patterns. I will verify any suggested patterns manually by reviewing the original examples and checking whether the issue comes from label ambiguity, insufficient examples, or classifier limitations.
