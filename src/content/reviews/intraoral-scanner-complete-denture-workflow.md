---
title: "Your Intraoral Scanner Can Scan a Denture. Sort Of."
description: "A novel marker-assisted IOS workflow from the University of Michigan enables accurate complete denture digitisation using a TRIOS4 and free Meshmixer software, without modifying the denture's critical border or intaglio surface."
pubDate: 2025-05-11
paperTitle: "Workflow to facilitate complete denture scanning with an intraoral scanner: A technique report"
paperAuthors: "Jiayi Yu MS, Jiayi Lu DDS MS, Berna Saglik DDS MS, Junying Li DDS MS PhD"
paperJournal: "Journal of Prosthodontics"
paperYear: 2025
tags: ["complete denture", "intraoral scanner", "digital dentistry", "denture duplication", "digital workflow", "edentulous", "CAD/CAM"]
clinicalRelevance: "Apply polyvinyl siloxane strip markers to the denture flange before IOS scanning to improve stitching fidelity at borders, then use free Meshmixer software to remove markers and reconstruct the definitive digital duplicate — all without sending the denture to a lab."
verdict: "PVS markers fix denture scanning"
pdfPath: "2MP Project/journals/Journal of Prosthodontics/2025/JProsth_Yu_jopr.14063.pdf"
---

Intraoral scanners are remarkably good at scanning teeth. They are considerably less enthusiastic about scanning the smooth, featureless, uniformly curved surfaces of a complete denture. And yet the clinical need to digitise existing dentures keeps growing regardless of how the scanner feels about it.

Yu, Lu, Saglik, and Li from the University of Michigan School of Dentistry tackle this in *Workflow to facilitate complete denture scanning with an intraoral scanner: A technique report* (*Journal of Prosthodontics*, 2025). The premise is simple: the scanner struggles with complete dentures because there is nothing for its stitching algorithm to recognise. So give it something. The paper introduces a marker-assisted protocol that sidesteps the need for a laboratory desktop scanner, uses only free software for post-processing, and preserves the accuracy of the border and intaglio surface without modifying either.

### The Data Anchor

The workflow was demonstrated on a maxillary complete denture scanned with a TRIOS4 (3Shape). Polyvinyl siloxane material (Futar Fast; Kettenbach) was applied as continuous strips approximately 4 mm thick and 6 mm wide on the labial flange and posterior border, placed 1–2 mm from the peripheral border, plus a single drop marker approximately 5 mm in diameter centrally on the intaglio surface. The strips create recognisable features for the stitching algorithm; the drop marker anchors the otherwise featureless intaglio.

The scanning sequence followed a structured path: occlusal surface first, then cameo surfaces, then rotation around the labial flange border, then intaglio in a zigzag from anterior to posterior. The drop marker was trimmed in scanner software, the region re-scanned, and the STL exported. Post-processing in Autodesk Meshmixer (v3.5.474; free) used the Select, Bridge, Inspector, and Sculpt tools to remove markers and reconstruct the denture border with Smooth Fill.

Accuracy was assessed by 3D comparison against a desktop scanner reference in Geomagic Control X (3D Systems), with the clinically accepted threshold set at 0.3 mm (attributed to mucosal resilience by Deng et al.). The colour map demonstrated results within tolerance in the intaglio and peripheral border regions.

### Key Findings

- **Markers mimic the boxing impression technique**, adding bulk and distinct geometry so the IOS stitching algorithm has something to register across an otherwise continuous, featureless curve.
- **Critical surfaces are untouched.** Unlike earlier protocols that required modifying denture borders, this approach leaves the intaglio and peripheral borders unaltered; markers are applied externally and removed digitally.
- **Free software is sufficient.** Meshmixer requires no licence; Select, Bridge, Inspector, and Sculpt are basic functions accessible to any clinician willing to spend an afternoon with a tutorial.
- **Existing occlusion is preserved**, reducing the need for tooth repositioning or occlusal adjustment when fabricating a duplicate.
- **This is a single-case technique report.** The authors acknowledge the need for further research, and whether the 0.3 mm tolerance holds across different scanners, operators, or denture geometries remains untested.

### 💡 The Clinical Bottom Line

If you have a TRIOS4 and a patient whose denture needs duplicating, this workflow means you no longer have to choose between sending the prosthesis to a lab or accepting a distorted scan. Apply polyvinyl siloxane markers, follow the structured scanning sequence, clean up in free Meshmixer, and export an STL within clinical tolerance — all in-house, with equipment you already own. The logic is sound and the barrier to entry is genuinely low. Monday morning, this is worth trying before you reach for the courier bag.

*Dr Samuel Rosehill is a general dentist with a prosthodontic focus, practising at Ethical Dental in Coffs Harbour, NSW. He holds a BDSc (Hons) from the University of Queensland, an MBA, an MMktg, and an MClinDent in Fixed & Removable Prosthodontics (Distinction) from King's College London.*

**Reference:** [Yu J, Lu J, Saglik B, Li J. Workflow to facilitate complete denture scanning with an intraoral scanner: A technique report. *Journal of Prosthodontics*, 2025. DOI: 10.1111/jopr.14063](https://doi.org/10.1111/jopr.14063)
