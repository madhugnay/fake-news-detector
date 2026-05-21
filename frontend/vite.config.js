import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins:[react()],

  server:{
    proxy:{
      '/predict-image':{
        target:'http://localhost:10000',
        changeOrigin:true
      },

      '/predict-text':{
        target:'http://localhost:10000',
        changeOrigin:true
      },

      '/predict-audio':{
        target:'http://localhost:10000',
        changeOrigin:true
      },

      '/predict-multimodal':{
        target:'http://localhost:10000',
        changeOrigin:true
      }
    }
  }
})