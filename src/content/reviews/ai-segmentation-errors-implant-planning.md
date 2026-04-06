---
title: "When the AI Gets the Anatomy Wrong"
description: "A narrative review from the University of Florida catalogues the ways AI segmentation in implant planning software can fail — from misidentifying the inferior alveolar nerve to hallucinating anatomy that isn't there — and why clinicians must verify before they trust."
pubDate: 2026-04-07
paperTitle: "Artificial Intelligence Segmentation Errors in Implant Planning Software Programs: An Overview"
paperAuthors: "Lawand G, Gonzaga L, Issa J, Revilla-Leon M, Tohme H, Saleh A, Martin W"
paperJournal: "Clinical Implant Dentistry and Related Research"
paperYear: 2025
tags: ["artificial intelligence", "CBCT segmentation", "implant planning", "digital dentistry", "surgical guides", "computer-assisted surgery", "AI errors"]
clinicalRelevance: "Catalogues common AI segmentation failure patterns across four major implant planning platforms and provides a framework for clinician verification before surgical guide fabrication"
verdict: "AI segments fast but still gets it wrong"
pdfPath: "2MP Project/journals/Clinical Implant Dentistry and Related Research/2025/CIDR_Lawand_cid.70095.pdf"
---

Artificial intelligence in implant planning software has developed the professional reputation of a very keen junior associate: fast, confident, and occasionally spectacularly wrong about something that matters. It will segment your CBCT in seconds, conjure a 3D model of the mandible before you have finished your coffee, and sometimes label a radiolucent artefact in the maxilla as the inferior alveolar nerve canal with the quiet assurance of someone who has never opened an anatomy textbook. Lawand and colleagues from the University of Florida, in "Artificial Intelligence Segmentation Errors in Implant Planning Software Programs: An Overview" (*Clinical Implant Dentistry and Related Research*, 2025), have catalogued the ways AI segmentation can fail across four major planning platforms and produced something clinicians urgently need: a taxonomy of errors and a framework for catching them before they reach the surgical guide.

### The Data Anchor

This narrative review and educational practice overview evaluated AI-based segmentation across four implant planning software programs: coDiagnostiX, BlueSkyPlan, Atomica, and Relu. The authors performed direct use and exploration of each platform, qualitatively documenting common error patterns and demonstrating the editing functionalities available for correction. Error types were classified into four categories: boundary errors, over-segmentation and under-segmentation, misidentification errors, and partial volume effects. The review also synthesised literature on the deep learning architectures underpinning these tools, including U-Net, generative adversarial networks (GANs), and the SISTR framework. This is not a formal comparative study; the software demonstrations are illustrative rather than reproducible performance benchmarks.

### Key Findings

- **Boundary errors are the most common failure mode.** CBCT's limited soft-tissue contrast causes AI algorithms to blur the boundaries between structures of similar radiodensity, particularly the inferior alveolar nerve canal and surrounding cortical bone.
- **Misidentification errors can be clinically dangerous.** The authors documented cases where the AI segmented a maxillary radiolucent region as the inferior alveolar nerve canal (an anatomical impossibility) and where metallic restorations generated streak artefacts that the algorithm incorporated into the bone model.
- **Over-segmentation inflates anatomy; under-segmentation erases it.** Over-segmentation merges adjacent structures (teeth fused with bone), while under-segmentation misses thin cortical plates or small anatomical features entirely.
- **Editing capabilities vary dramatically between platforms.** Some software offers robust manual correction tools; others provide minimal options to fix what the AI gets wrong, leaving clinicians with a take-it-or-leave-it model.
- **Caveat:** This is a qualitative, non-systematic review. The error examples are drawn from clinical use rather than a controlled dataset, and the findings should not be read as a comparative ranking of the four platforms.

> The speed of AI segmentation creates a dangerous cognitive trap: the faster and smoother the output looks, the less inclined the clinician is to check it.

### 💡 The Clinical Bottom Line

AI segmentation is a tool for efficiency, not a substitute for anatomical competence. Before any surgical guide leaves the digital design phase, clinicians should scroll through the axial, coronal, and sagittal slices to verify that the segmented anatomy matches reality, particularly around the IAN canal, sinus floor, and thin buccal plates. The platforms that offer the best editing tools deserve preference, because it is not a question of *whether* the AI will get something wrong; it is a question of whether you will catch it before the drill does.

*Dr Samuel Rosehill is a general dentist with a prosthodontic focus, practising at Ethical Dental in Coffs Harbour, NSW. He holds a BDSc (Hons) from the University of Queensland, an MBA, an MMktg, and an MClinDent in Fixed & Removable Prosthodontics (Distinction) from King's College London.*

**Reference:** Lawand G, Gonzaga L, Issa J, Revilla-Leon M, Tohme H, Saleh A, Martin W. Artificial intelligence segmentation errors in implant planning software programs: An overview. *Clin Implant Dent Relat Res.* 2025;27:e70095. doi: [10.1111/cid.70095](https://doi.org/10.1111/cid.70095)
