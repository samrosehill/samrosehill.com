---
title: "An Open-Source AI Tool That Generates Dynamic Jaw Motion from Static Scans"
description: "A scanner-agnostic Python workflow interpolates dynamic mandibular motion paths from four static interocclusal records, exporting motion files compatible with dental CAD software — no proprietary jaw tracker required."
pubDate: 2025-12-03
paperTitle: "Scanner-agnostic dynamic jaw motion generation from virtual static excursive records using open-source Python-based artificial intelligence (AI) interpolation"
paperAuthors: "Omar MS, Yang CC, Morton D, Lin WS"
paperJournal: "Journal of Prosthodontics"
paperYear: 2025
tags: ["digital prosthodontics", "jaw motion tracking", "artificial intelligence", "CAD/CAM", "virtual articulator", "open-source"]
clinicalRelevance: "Clinicians using any intraoral scanner can now generate patient-specific dynamic jaw motion paths for CAD software using free, open-source tools — eliminating the need for expensive proprietary jaw tracking hardware."
verdict: "Open-source motion paths"
pdfPath: "2MP Project/journals/Journal of Prosthodontics/2025/JProsth_Omar_jopr.70051.pdf"
---

The virtual articulator has always had a slightly tragic quality. It sits inside your CAD software looking tremendously sophisticated, ready to simulate mandibular excursions with mathematical precision, and yet the data it runs on is almost always a set of average anatomical parameters that belong to nobody in particular. Your patient's condylar inclination, their specific lateral envelope of motion, the particular way their mandible tracks during protrusion: none of this makes it into most digital workflows, because recording it has traditionally required expensive proprietary hardware that exports to exactly one CAD platform. Omar and colleagues, in "Scanner-agnostic dynamic jaw motion generation from virtual static excursive records using open-source Python-based artificial intelligence (AI) interpolation" (*Journal of Prosthodontics*, 2025), have built something rather elegant: a free, open-source Python tool that generates individualised dynamic jaw motion from four simple static bite records you can capture with any intraoral scanner.

### The Data Anchor

This is a technique paper describing a complete digital workflow, so there are no patient outcomes or statistical comparisons to report. The workflow begins with capturing intraoral scans of both arches using any IOS (the authors demonstrated with 3Shape TRIOS 4, but the method is deliberately scanner-agnostic). The mandibular scan is duplicated three times and registered in four interocclusal positions: maximum intercuspation, left laterotrusion, right laterotrusion, and full protrusion. These static STL files are imported into the custom Python interface, which uses a point-tracking AI algorithm to interpolate continuous motion paths between the four recorded positions. The output is an XML motion file directly compatible with exocad CAD software (with a simple file extension change to .jawMotion for certain versions).

### Key Findings

- **The entire workflow requires only standard intraoral scans** — no jaw tracking hardware, no face-bow, no proprietary recording device. Four static interocclusal records captured with any IOS provide the input data
- **The Python tool is fully open-source**, eliminating vendor lock-in and reducing cost to zero for the motion generation step. The algorithm and user interface code are provided as supplementary material
- **Output files are CAD-compatible**, specifically formatted for exocad, which is one of the most widely used open-architecture dental design platforms
- **The AI interpolation generates a continuous motion trajectory** from discrete static positions, simulating the functional envelope of mandibular movement rather than relying on average condylar parameters
- **The technique is inherently scanner-agnostic** — because the input is standard STL files, any IOS that exports STL can feed the workflow
- **Limitation: this is a proof-of-concept technique description** with no validation against actual jaw tracking data, no accuracy measurements comparing interpolated paths to recorded movements, and no clinical outcome data. The fidelity of the interpolation algorithm remains unproven

> The honest caveat here is significant: interpolating between four static positions is a mathematical approximation of actual mandibular dynamics, and nobody has yet demonstrated how closely this approximation matches reality. But as a first step toward democratising patient-specific jaw motion data, the concept is sound and the barriers to entry are essentially zero.

### 💡 The Clinical Bottom Line

If you have been designing restorations on average-value virtual articulators because jaw tracking hardware was too expensive or too workflow-intensive, this technique removes the cost and vendor barriers entirely. Capture four bite records with your existing IOS, run the free Python script, and import the motion file into exocad. Whether the interpolated motion is accurate enough to reduce chairside occlusal adjustments remains an open question — but at minimum, you are now working with patient-specific data rather than population averages, and the price of admission is a Python installation.

*Dr Samuel Rosehill is a general dentist with a prosthodontic focus, practising at Ethical Dental in Coffs Harbour, NSW. He holds a BDSc (Hons) from the University of Queensland, an MBA, an MMktg, and an MClinDent in Fixed & Removable Prosthodontics (Distinction) from King's College London.*

**Reference:** Omar MS, et al. Scanner-agnostic dynamic jaw motion generation from virtual static excursive records using open-source Python-based artificial intelligence (AI) interpolation. *J Prosthodont*. 2026;35:407–413. DOI: [10.1111/jopr.70051](https://doi.org/10.1111/jopr.70051)
