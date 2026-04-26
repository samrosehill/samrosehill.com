---
title: "The Dental AI That Can Show Its Work"
description: "CariesAI-3D, a multitask learning network developed by Qi et al. at Tongji University, classifies dentin caries severity on CBCT images with 88.6% accuracy across four categories — and unusually, uses class activation mapping to show clinicians exactly which anatomical regions drove each decision."
pubDate: 2026-04-27
paperTitle: "A clinically oriented and interpretable AI framework for classifying dentin caries severity on CBCT images"
paperAuthors: "Qi, S & Shan, H et al."
paperJournal: "The Journal of Prosthetic Dentistry"
paperYear: 2026
tags: ["caries", "artificial intelligence", "CBCT", "deep learning", "caries classification", "interpretable AI", "class activation mapping", "minimally invasive dentistry", "endodontics", "diagnostic imaging"]
clinicalRelevance: "CariesAI-3D classifies dentin caries severity into four ICCMS-aligned categories (Sound, Moderate, Deep, Extremely Deep) on existing CBCT scans with 88.6% accuracy and AUC values from 0.947 to 0.998 on an independent test set. Critically, the authors stress that CBCT should not be ordered for caries diagnosis alone — this tool is designed to extract additional diagnostic value from scans already acquired for orthodontic or surgical indications. Class activation mapping shows the model consistently focuses on caries and pulp regions, providing a degree of clinical interpretability unusual for diagnostic AI. Single-centre data and absence of histological validation are key limitations."
verdict: "88.6% accurate, shows its work"
pdfPath: "2MP Project/journals/The Journal of Prosthetic Dentistry/2025/JPD_Qi_j.prosdent.2025.10.034.pdf"
---

Most diagnostic AI in dentistry sits in an epistemologically awkward position: it is either right or wrong, and either way cannot tell you why. "A clinically oriented and interpretable AI framework for classifying dentin caries severity on CBCT images," published in *The Journal of Prosthetic Dentistry* by Qi, Shan, and colleagues at Tongji University, is a paper that takes this problem seriously. The field has accumulated a cheerful stack of high-accuracy claims, and uptake at the chairside has been, to put it diplomatically, measured. When a model is a black box, there is no rational basis for trust beyond track record, and most track records in dental AI are short.

CariesAI-3D trains simultaneously on caries and pulp segmentation so that the anatomical features driving its classification decisions are the same ones a clinician would use. Class activation mapping (CAM) then makes this visible, highlighting the regions that influenced each prediction. The result is a model that can, unusually, show its work.

One constraint bears stating upfront: CBCT should not be ordered for caries diagnosis. This tool extracts value from scans already acquired for orthodontic or surgical indications, which is a meaningful distinction.

> The authors are explicit: CariesAI-3D is intended to leverage existing CBCT scans obtained for clinically appropriate purposes, not to generate new radiation exposure.

### The Data Anchor

The dataset comprised **2,148 CBCT images of single teeth**, collected retrospectively from 2022 to 2024 at Tongji University's affiliated hospital under orthodontic or maxillofacial surgery indications. Two dental experts (mean 16 years' experience) and a radiologist annotated by consensus using ICCMS criteria consolidated into four categories: Sound, Moderate (outer or middle dentin third), Deep (inner dentin third), and Extremely Deep (into the pulp). Enamel caries were excluded for low CBCT contrast. Split: 1,826 cases for 5-fold cross-validation, 322 for independent testing.

The architecture fused a U-Net segmentation branch with a ResNet-18 classification branch via a spatial-attention feature fusion module (SA-FFM), using cross-attention to emphasise clinically relevant features.

### Key Findings

- **CariesAI-3D outperformed all six comparator models** (ResNet-18/34/50, DenseNet-121/169, MobileNet-V2) on cross-validation: accuracy **0.886**, precision **0.882**, recall **0.873**, F1-score **0.876**. Statistically significant differences at P < .05 to P < .001 across primary metrics.
- **Independent test set generalisation was robust.** Micro-average AUC of **0.981** (95% CI: 0.972–0.988); class-wise AUC from **0.947 to 0.998**. MAD between cross-validation and test set: 0.011 to 0.033, indicating low overfitting.
- **Harder categories were, predictably, harder.** Sound and Moderate lesions exceeded 0.916 class-wise accuracy; Deep and Extremely Deep were lower, with most misclassifications occurring between adjacent severity classes where radiographic distinction is genuinely ambiguous.
- **CAM visualisations showed anatomical coherence.** Model attention corresponded strongly with caries and pulp regions, supporting the interpretability claim at the heart of the architecture.
- **Limitations worth noting.** Single-centre data; no histological or micro-CT validation; no comparison against clinicians of varying experience. The authors acknowledge all three.

### 💡 The Clinical Bottom Line

The more interesting claim here is not the accuracy figure but what the architecture implies: that interpretability is a design choice, not a post-hoc reassurance. Building segmentation and classification into the same multitask framework means the model reasons, at least partly, as a clinician would. That is the prerequisite for genuine clinical uptake, as distinct from polite acknowledgement.

Used within its appropriate scope — secondary analysis of scans already acquired for other indications — an 88.6% accurate classifier that can show its reasoning is meaningfully more useful than one that cannot. The black box problem in dental AI is apparently a matter of making interpretability a requirement from the first line of code.

*Dr Samuel Rosehill is a general dentist with a prosthodontic focus, practising at Ethical Dental in Coffs Harbour, NSW. He holds a BDSc (Hons) from the University of Queensland, an MBA, an MMktg, and an MClinDent in Fixed & Removable Prosthodontics (Distinction) from King's College London.*

**Reference:** [Qi S, Shan H, Fu Y, Chen Y, Zhang Q. A clinically oriented and interpretable AI framework for classifying dentin caries severity on CBCT images. *The Journal of Prosthetic Dentistry*, 2026. DOI: 10.1016/j.prosdent.2025.10.034](https://doi.org/10.1016/j.prosdent.2025.10.034)
