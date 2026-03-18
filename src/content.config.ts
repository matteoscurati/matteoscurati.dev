import { defineCollection, z } from "astro:content";
import { file, glob } from "astro/loaders";

const projects = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "src/content/projects" }),
  schema: z.object({
    name: z.string(),
    category: z.enum(["independent", "consulting", "career"]),
    role: z.string(),
    period: z.string(),
    status: z.enum(["live", "beta", "wip", "shipped", "archived"]),
    description: z.string(),
    tech: z.array(z.string()),
    link: z.string().optional(),
    order: z.number(),
  }),
});

const lab = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "src/content/lab" }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    tags: z.array(z.string()),
  }),
});

export const collections = { projects, lab };
