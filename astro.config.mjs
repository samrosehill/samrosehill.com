import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://samrosehill.com',
  markdown: {
    shikiConfig: {
      theme: 'github-light',
    },
  },
});
