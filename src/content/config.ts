import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    summary: z.string(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

const posters = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    venue: z.string(),
    date: z.coerce.date(),
    authors: z.string(),
    tags: z.array(z.string()).default([]),
    pdf: z.string().optional(),
    link: z.string().url().optional(),
  }),
});

export const collections = { blog, posters };
