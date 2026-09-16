import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: resolve(__dirname, 'core/static/core/js/dist'),
    emptyOutDir: true,
    rollupOptions: {
      input: resolve(__dirname, 'core/static/core/js/index.jsx'),
      output: {
        entryFileNames: 'main.js',
      },
    },
  },
});