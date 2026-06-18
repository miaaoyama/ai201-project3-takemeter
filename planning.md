## Labels

### Analytical Take

A post that makes a structured argument supported by specific examples, evidence, comparisons, observations, or detailed reasoning.

**Example 1:** "Comparing album sales from 2019–2025 shows that fourth-generation groups are growing internationally faster than previous generations."

**Example 2:** "Looking at chart performance and concert attendance together provides a better measure of popularity than album sales alone."

**Uncertain example:** "I think this group has the strongest stage presence because they seem more confident than others."

---

### Preference Take

A post that primarily expresses a personal preference, ranking, taste, or subjective opinion rather than presenting evidence-based reasoning.

**Example 1:** "I prefer BTS's earlier albums because their sound felt more authentic to me."

**Example 2:** "This is my favorite comeback of the year even though it wasn't the most successful commercially."

**Uncertain example:** "This group is declining because their recent songs are weaker."

---

### Reactive Take

A post that primarily expresses an emotional reaction to a recent event, release, announcement, controversy, or performance.

**Example 1:** "I can't believe the comeback teaser just dropped. I'm so excited."

**Example 2:** "That award show performance was incredible. I watched it three times."

**Uncertain example:** "I loved the comeback because the concept feels more mature."

## Hard Edge Cases

The hardest edge case will be distinguishing between Analytical Take and Preference Take. Many users provide one or two examples while expressing a personal preference. My decision rule will be: if the post builds a structured argument supported by evidence or reasoning, it will be labeled Analytical Take. If the post primarily expresses personal taste, rankings, favorites, or subjective opinions, it will be labeled Preference Take.

Another difficult edge case is distinguishing Reactive Take from Preference Take. If the post focuses mainly on an immediate emotional response to an event or release, it will be labeled Reactive Take. If the post focuses on long-term preferences or opinions, it will be labeled Preference Take.

## Data Collection Plan

I collected approximately 200 posts from r/kpopthoughts using publicly available posts. The final dataset contains 202 labeled examples with the following distribution:

* Analytical Take: 123 posts
* Preference Take: 52 posts
* Reactive Take: 27 posts

Although the dataset is not perfectly balanced, the labels reflect naturally occurring discussion patterns within the community. During evaluation, I will use precision, recall, and F1 score in addition to accuracy to account for class imbalance.

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
