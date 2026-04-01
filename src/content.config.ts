import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const reviews = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/reviews' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    paperTitle: z.string(),
    paperAuthors: z.string(),
    paperJournal: z.string(),
    paperYear: z.number(),
    tags: z.array(z.string()).default([]),
    clinicalRelevance: z.string().optional(),
    verdict: z.string().optional(),
    pdfPath: z.string().optional(),
    substackUrl: z.string().url().optional(),
  }),
});

const projects = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/projects' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    tags: z.array(z.string()).default([]),
    url: z.string().url().optional(),
    status: z.enum(['active', 'archived', 'wip']).default('active'),
  }),
});

export const collections = { reviews, projects };
