---
title: "Can AI Design a Crown? A Transformer Model Gets Surprisingly Close"
description: "A novel transformer-based implicit neural network reconstructs missing tooth morphology across molars, premolars, and incisors with high dimensional accuracy — matching original crowns more closely than an experienced technician in some dimensions."
pubDate: 2026-04-01
paperTitle: "Automated reconstruction of missing tooth morphology using a transformer-based implicit neural network: A multi-tooth position evaluation"
paperAuthors: "Wang Y, Shi Y, Li N, et al."
paperJournal: "Journal of Prosthodontics"
paperYear: 2026
tags: ["artificial intelligence", "digital dentistry", "CAD/CAM", "crown design", "deep learning", "implicit neural network", "prosthodontics", "dental technology"]
clinicalRelevance: "Transformer-based AI models can generate anatomically plausible single-tooth crown designs from digital arch scans, performing comparably to experienced technicians for molars and achieving clinically acceptable dimensional accuracy across tooth types — though anterior teeth and fine functional anatomy still require human refinement."
verdict: "AI matches technicians for molars"
pdfPath: "2MP Project/journals/Journal of Prosthodontics/2025/JProsth_Wang_jopr.70084.pdf"
---

The dental technician has been the quiet artisan of prosthodontics for the better part of a century — part sculptor, part engineer, fluent in a visual language of cusp tips and marginal ridges that no textbook has ever quite managed to codify. It is, you might say, one of the last genuinely craft-based roles in a profession that has been digitising everything else at remarkable speed. So when a research team in Beijing trains a neural network to do the same job, the question is not whether the machine can produce a crown. The question is whether it can produce one that a clinician would actually seat.

Wang, Shi, Li, Lin, Tan and Chen's study — *Automated Reconstruction of Missing Tooth Morphology Using a Transformer-Based Implicit Neural Network* (*Journal of Prosthodontics*, 2026) — suggests the answer is: **for molars, essentially yes; for anterior teeth, not quite yet**.

### The Data Anchor

The team at Peking University developed a transformer-based implicit neural network (INN) trained on **1,800 complete digital arch scans** — 500 with first molars, 600 with first premolars, and 700 with central incisors. Each arch was processed to simulate a missing tooth by segmenting the target using 3D mesh software (Meshmixer, Autodesk). The model combined a self-structure enhancement module with multi-view 2D depth maps to capture both global context and local geometric detail. Training used 50,000 sampling points per tooth, with performance evaluated using chamfer distance (CD), F-score and volumetric intersection over union (IoU).

The generated crowns (GC) were then compared against both the original clinical crowns (OC) and crowns designed by an experienced dental technician (TC, 15+ years' experience) using 3Shape CAD software. Morphological deviations were assessed via RMS error and 3D colour mapping, while dimensional accuracy was measured across mesiodistal width, buccopalatal/labiolingual breadth, and occlusogingival height.

### Key Findings

- **Central incisors achieved the best reconstruction accuracy**, with a chamfer distance of just 0.0028, F-score of 0.9670, and IoU of 0.9716 — indicating near-perfect geometric overlap with original crown morphology
- **For molars, AI-generated crowns matched technician-designed crowns** in RMS deviations (GC: 0.2786 ± 0.0462 mm vs TC: 0.3056 ± 0.0605 mm, p = 0.064), with no statistically significant difference
- **For premolars and incisors, the technician still wins on surface accuracy** — TC achieved significantly lower RMS deviations (premolars: p = 0.002, Cohen's d = 1.12; incisors: p = 0.014, d = 0.87), primarily in complex functional regions like marginal ridges and grooves
- **Dimensionally, AI outperformed the technician** — model-generated crowns showed no significant differences from original crowns in any measured dimension, while technician crowns showed significantly larger mesiodistal widths in molars and occlusogingival heights in incisors
- **The model generalised across tooth types** using a single network architecture, without requiring position-specific training — a meaningful advantage over earlier GAN-based approaches that were limited to single tooth positions
- *Limitations:* In vitro only, with a single technician as the comparator; only three tooth types tested (no canines, second premolars, or multi-tooth gaps); no functional validation of occlusal contacts or interproximal fit

### 💡 The Clinical Bottom Line

The clinical reality in 2026 is that AI-designed crowns are not yet ready to replace the technician's eye for anterior aesthetics or the subtle anatomy of premolar cusps — but for molar restorations, the gap has functionally closed. What makes this study interesting is not just the accuracy metrics but the workflow implication: a model that generates a dimensionally faithful starting point in seconds could reduce the technician's role from sculptor to editor, trimming design time without sacrificing the human judgement that matters most.

> The real test will come when someone trains this model on canines and multi-unit spans — and when the first clinician seats an AI-designed crown without adjusting it. That day is not here yet. But it is closer than most technicians would find comfortable.

The technician's job is not disappearing. It is, rather quietly, being promoted.

*Dr Samuel Rosehill is a general dentist with a prosthodontic focus, practising at Ethical Dental in Coffs Harbour, NSW. He holds a BDSc (Hons) from the University of Queensland, an MBA, an MMktg, and an MClinDent in Fixed & Removable Prosthodontics (Distinction) from King's College London.*

**Reference:** Wang Y, Shi Y, Li N, Lin W-S, Tan J, Chen L. Automated reconstruction of missing tooth morphology using a transformer-based implicit neural network: A multi-tooth position evaluation. *Journal of Prosthodontics*. 2026;35:191–200. https://doi.org/10.1111/jopr.70084
