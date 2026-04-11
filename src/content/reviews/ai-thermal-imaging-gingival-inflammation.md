---
title: "Heat Signature: Can AI Read Gingival Inflammation Without a Probe?"
description: "Çankaya et al. train an XGBoost model on thermal images of the anterior maxillary gingiva and achieve 92.7% accuracy classifying gingival inflammation — no probing, no contact, no operator variability."
pubDate: 2025-10-30
paperTitle: "Artificial Intelligence Assisted Thermal Imaging for Gingival Inflammation Assessment: A Novel Approach"
paperAuthors: "Çankaya ZT, Koyuncu A, Gürbüz S"
paperJournal: "Journal of Esthetic and Restorative Dentistry"
paperYear: 2026
tags: ["artificial intelligence", "thermal imaging", "gingival inflammation", "periodontics", "XGBoost", "non-invasive diagnostics", "bleeding on probing", "thermography", "periodontal health"]
clinicalRelevance: "An XGBoost model trained on thermal images of the anterior maxillary gingiva classifies gingival health versus gingivitis with 92.7% accuracy and an F1 score of 0.9278, suggesting AI-assisted thermography could offer a non-contact, operator-independent screening tool for periodontal inflammation."
verdict: "AI reads gingival heat — 92.7%"
pdfPath: "2MP Project/journals/Journal of Esthetic and Restorative Dentistry/2026/JERD_Cankaya_jerd.70045.pdf"
---

Inflammation is, at its most elemental, a thermal event. Vasodilation, increased perfusion, erythema, oedema: the textbook description of gingivitis is, in structural terms, a description of heat redistribution in soft tissue.

"Artificial Intelligence Assisted Thermal Imaging for Gingival Inflammation Assessment: A Novel Approach" (Çankaya, Koyuncu and Gürbüz, *Journal of Esthetic and Restorative Dentistry*, 2026) is the first study to ask whether an AI model can read that heat signal well enough to classify gingival health without a probe. The short answer is: **yes, with 92.7% accuracy**.

Bleeding on probing (BoP) remains the most reliable clinical marker of gingival inflammation and the cornerstone of the 2017 World Workshop classification. Useful, indispensable, clinically validated. Also, when you think about it, a rather indirect way of measuring something that announces itself in the electromagnetic spectrum whether or not anyone is paying attention.

### The Data Anchor

Forty systemically healthy adults aged 18 to 25 were recruited from Gazi University, Türkiye, and divided into four groups of 10: mouth breathers with gingivitis, periodontally healthy mouth breathers, nasal breathers with gingivitis, and periodontally healthy nasal breathers. BoP < 10% defined periodontal health; BoP ≥ 10% defined plaque-induced gingivitis, confirmed by full-mouth clinical examination at six sites per tooth with a UNC-15 probe.

Thermal images were captured using an Optris PI 450 camera positioned 25 to 30 cm from the anterior maxillary gingiva. Each participant underwent four imaging sessions: baseline plus three post-rinse captures at 1, 2, and 3 minutes after a 60-second rinse with 20°C water, assessing the rewarming response as a proxy for microvascular perfusion.

After quality review by two periodontists, 160 of 164 images were retained and annotated via Make Sense AI, generating 1,734 labelled data points split 80/20 for training and testing.

Classification used XGBoost with hyperparameters tuned via grid search and 5-fold cross-validation. L1 and L2 regularisation reduced overfitting. Ground-truth labels came exclusively from BoP; the Gingival Index was recorded but used only to stratify severity within BoP-positive cases.

### Key Findings

- **92.74% accuracy, 92.95% precision, 92.74% sensitivity, F1 score 0.9278** on the best-performing fold: a strong result for an exploratory study at this scale
- **Cross-validation confirmed stability:** mean validation accuracy was 89.43%, mean test accuracy 88.28%, with individual fold results ranging from approximately 86% to 92.7%
- **ROC-AUC reached 0.99 on the best fold**, indicating near-perfect discriminative capacity between healthy and inflamed gingival tissue
- **Mouth breathing was not a predictive variable** — included only to broaden the physiological range of thermal presentations in the anterior maxillary region
- **Image-level statistical power exceeded 80%** across 1,734 data points; patient-level power was 71%, acceptable for exploratory AI research
- *Limitations:* Cross-sectional, n = 40, anterior maxilla only; no validation in older adults or periodontitis patients; site-level thermal thresholds not yet defined

### 💡 The Clinical Bottom Line

This study will not change how you probe on Monday morning. What it does is something more foundational: it demonstrates, for the first time, that an AI model can distinguish healthy from inflamed gingival tissue using thermal images alone, with accuracy that exceeds photographic gingivitis-detection models in comparable pilots. The practical implications (telehealth screening, community triage, resource-limited settings) are longer-horizon; the methodological contribution is immediate.

> Gingival inflammation has always been a thermal story. This study simply provides the first systematic evidence that a camera and a gradient-boosted classifier can read it.

The probe may be irreplaceable in the operatory. In the waiting room, the school gymnasium, or the remote health clinic, the thermometer might one day carry more weight than we currently give it.

*Dr Samuel Rosehill is a general dentist with a prosthodontic focus, practising at Ethical Dental in Coffs Harbour, NSW. He holds a BDSc (Hons) from the University of Queensland, an MBA, an MMktg, and an MClinDent in Fixed & Removable Prosthodontics (Distinction) from King's College London.*

**Reference:** [Çankaya ZT, Koyuncu A, Gürbüz S. Artificial Intelligence Assisted Thermal Imaging for Gingival Inflammation Assessment: A Novel Approach. *Journal of Esthetic and Restorative Dentistry*, 2026; 38:362–370. DOI: 10.1111/jerd.70045](https://doi.org/10.1111/jerd.70045)
