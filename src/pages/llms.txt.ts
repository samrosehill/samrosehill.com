import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

export const GET: APIRoute = async () => {
  const reviews = (await getCollection('reviews'))
    .sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());

  const reviewLines = reviews
    .map((r) => `- [${r.data.title}](https://samrosehill.com/reviews/${r.id})`)
    .join('\n');

  const body = `# samrosehill.com

> A clinical archive of dental research reviews and case notes by Dr. Samuel Rosehill. Each review distils a recent peer-reviewed paper into its clinical essentials — data anchor, key findings, and a bottom-line verdict for practising clinicians.

## Author

Dr. Samuel Rosehill is a dentist practising at Ethical Dental and Orthodontics in Coffs Harbour, NSW, Australia. He holds a BDSc (Hons) from the University of Queensland and an MClinDent in Fixed & Removable Prosthodontics (Distinction) from King's College London. He is a Fellow of the Pierre Fauchard Academy and the International College of Dentists.

## Topics Covered

- Prosthodontics (fixed and removable)
- Dental implantology
- Digital dentistry and 3D printing
- Guided implant surgery (static and dynamic)
- Bone grafting and ridge preservation
- Soft tissue management
- Shade matching and colour science
- Biomaterials (zirconia, lithium disilicate, collagen matrices)

## Pages

- [Home](https://samrosehill.com/)
- [Journal — All Reviews](https://samrosehill.com/reviews/)
- [About the Author](https://samrosehill.com/about/)

## Dental Research Reviews

${reviewLines}
`;

  return new Response(body, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
};
