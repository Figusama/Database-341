import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

const BACKEND = 'http://localhost:8000'
// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: { 
    proxy: {
      "/conferences": BACKEND,
      "/tracks": BACKEND,
      "/authors": BACKEND,
      "/reviewers": BACKEND,
      "/users": BACKEND,
      "/papers": BACKEND,
      "/reviews": BACKEND,
      "/sessions": BACKEND,
    }
  }
})
