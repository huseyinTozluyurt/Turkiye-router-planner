import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  base: '/Turkiye-router-planner/', // must match your repo name
  plugins: [react()],
})
