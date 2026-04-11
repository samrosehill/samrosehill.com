---
title: "The Machine That Picks Shades Better Than You Do (and Faster, and More Consistently)"
description: "A prospective study of 150 patients finds that a deep neural network combined with grey relational analysis achieves 93.2% shade matching accuracy for anterior restorations — outperforming both visual assessment and spectrophotometry alone."
pubDate: 2026-03-24
paperTitle: "Integration of grey relational analysis and deep neural networks for optimized dental shade selection in aesthetic restorations"
paperAuthors: "Ruan C, Yang H, Li Z, Wu Z, Wang L, Xiong J"
paperJournal: "Journal of Prosthodontics"
paperYear: 2026
tags: ["shade matching", "artificial intelligence", "deep neural network", "grey relational analysis", "dental aesthetics", "VITA shade guide", "colour matching", "digital dentistry", "spectrophotometry"]
clinicalRelevance: "An integrated AI system combining grey relational analysis with deep learning achieved significantly higher shade matching accuracy than visual or spectrophotometric methods alone — suggesting that multi-variable AI systems considering skin tone, age, and patient preferences may become the next evolution in aesthetic shade selection."
verdict: "AI beats the eyeball"
pdfPath: "2MP Project/journals/Journal of Prosthodontics/2025/JProsth_Ruan_jopr.70119.pdf"
---

The word "shade" entered dental vocabulary from the textile industry, where it described gradations of dyed fabric held up to natural light by someone with good eyes and, ideally, no hangover. Two centuries later, the process for selecting the colour of a porcelain crown remains essentially the same: a clinician holding a small plastic tab next to a tooth, squinting under fluorescent lighting that bears no relationship to daylight, and announcing with unwarranted confidence that the patient is an A2. Ruan and colleagues, in "Integration of grey relational analysis and deep neural networks for optimized dental shade selection in aesthetic restorations" (*Journal of Prosthodontics*, 2026), have demonstrated what happens when you replace this charmingly artisanal method with an algorithm that considers the fifteen variables that actually determine whether a restoration looks right in a human face.

### The Data Anchor

This single-centre prospective study enrolled 150 patients (70 male, 80 female; mean age 31.5 years) stratified across three age groups, each requiring four or more consecutive maxillary anterior ceramic restorations. The system collects 15 input variables: spectrophotometric tooth colour (VITA Easyshade V), standardised facial and gingival photography, plus patient demographics and preferences. Grey relational analysis (GRA) weights these variables, then feeds the result into a deep neural network (four hidden layers, 16 VITA Classical shade output). Clinical accuracy was defined as agreement with a consensus panel of three blinded prosthodontists.

### Key Findings

- **The integrated AI system achieved 93.2% clinical accuracy** (95% CI: 90.6–95.8%), significantly outperforming spectrophotometry alone (82.7%), standalone GRA (85.4%), standalone DNN (89.3%), and visual assessment (68.5%; all p < 0.001 vs visual)
- **Processing time dropped by 75%**: 45 seconds versus 180 seconds for traditional visual matching
- **Patient satisfaction rose from 72.3% to 91.4%** (p < 0.001), with colour match accuracy as the strongest predictor (β = 0.62)
- **Skin tone was the most powerful predictor** of optimal shade selection (r = 0.842), followed by age (r = 0.763) and gender (r = 0.685), reinforcing that shade matching is a facial harmony problem, not merely a tooth colour problem
- **Younger patients strongly preferred brighter shades** (B1: 45.2%, A1: 35.6%), while older patients accepted more natural variation (χ² = 24.7, p < 0.001); females preferred brighter shades than males across all age groups (p = 0.002)
- **Technical accuracy was 94.7%** (ΔE₀₀ ≤ 2.0), consistently below the threshold of clinically perceptible colour difference
- **Key limitation: single-centre, Han Chinese population.** Cross-ethnic validation (n = 30) showed 87.3% accuracy (p = 0.14 vs primary cohort), but formal multicenter validation across diverse skin types is essential before broader adoption

> The uncomfortable truth here is not that AI is better at shade matching than clinicians; it is that shade matching was never really about the shade tab at all. It is about how a tooth sits within a face, and the tab-and-squint method captures approximately none of that context.

### 💡 The Clinical Bottom Line

This study will not change your Monday morning workflow immediately (the system is not commercially available), but it should change how you think about shade selection. The finding that skin tone, age, and patient preferences collectively matter more than isolated tooth colour measurements validates what experienced ceramists have always intuited: a technically perfect colour match can still look wrong in the wrong face. For now, photograph under standardised conditions, consider the patient's complexion, and accept that spectrophotometry alone captures only part of the story. When AI shade systems do arrive in the clinic, the evidence suggests they will not just be faster; they will be looking at things we were never trained to measure.

*Dr Samuel Rosehill is a general dentist with a prosthodontic focus, practising at Ethical Dental in Coffs Harbour, NSW. He holds a BDSc (Hons) from the University of Queensland, an MBA, an MMktg, and an MClinDent in Fixed & Removable Prosthodontics (Distinction) from King's College London.*

**Reference:** Ruan C, Yang H, Li Z, et al. Integration of grey relational analysis and deep neural networks for optimized dental shade selection in aesthetic restorations. *J Prosthodont*. 2026;1–10. doi:10.1111/jopr.70119
