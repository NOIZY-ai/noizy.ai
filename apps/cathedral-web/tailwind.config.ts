import type { Config } from 'tailwindcss'

const config: Config = {
  content: ['./app/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        cathedral: {
          black: '#050505',
          amber: '#FF9F1C',
          cyan: '#00E5FF',
          white: '#F5F5F5',
          muted: '#6B7280',
          card: '#0A0A0A',
          wisdomGold: '#C49000',
        },
      },
      fontFamily: {
        display: ['Cormorant Garamond', 'serif'],
        ui: ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 6s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        glow: {
          '0%': { opacity: '0.4' },
          '100%': { opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}

export default config
