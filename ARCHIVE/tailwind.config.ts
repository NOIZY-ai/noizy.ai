import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        noizy: {
          black: '#0A0A0B',
          dark: '#111113',
          gray: '#1A1A1F',
          silver: '#8B8B9E',
          light: '#E4E4ED',
          white: '#F8F8FF',
          violet: '#8B5CF6',
          purple: '#7C3AED',
          indigo: '#6366F1',
          blue: '#3B82F6',
          cyan: '#06B6D4',
          pink: '#EC4899',
          rose: '#F43F5E',
          amber: '#F59E0B',
          green: '#10B981',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['JetBrains Mono', 'SF Mono', 'Fira Code', 'monospace'],
        display: ['Inter', 'system-ui', 'sans-serif'],
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'gradient-noizy': 'linear-gradient(135deg, #8B5CF6 0%, #EC4899 50%, #F59E0B 100%)',
        'gradient-heaven': 'linear-gradient(135deg, #6366F1 0%, #8B5CF6 33%, #EC4899 66%, #F43F5E 100%)',
        'gradient-lab': 'linear-gradient(135deg, #EC4899 0%, #F43F5E 50%, #EF4444 100%)',
        'gradient-noize': 'linear-gradient(135deg, #F59E0B 0%, #F97316 50%, #EF4444 100%)',
        'gradient-engine': 'linear-gradient(135deg, #06B6D4 0%, #3B82F6 50%, #6366F1 100%)',
        'gradient-dark': 'linear-gradient(180deg, #0A0A0B 0%, #111113 50%, #1A1A1F 100%)',
      },
      animation: {
        'fade-in': 'fadeIn 0.8s ease-out forwards',
        'fade-up': 'fadeUp 0.8s ease-out forwards',
        'slide-in-left': 'slideInLeft 0.8s ease-out forwards',
        'slide-in-right': 'slideInRight 0.8s ease-out forwards',
        'pulse-glow': 'pulseGlow 3s ease-in-out infinite',
        'float': 'float 6s ease-in-out infinite',
        'gradient-shift': 'gradientShift 8s ease infinite',
        'noise': 'noise 0.5s steps(10) infinite',
        'spin-slow': 'spin 12s linear infinite',
        'loading-bar': 'loadingBar 1s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        fadeUp: {
          '0%': { opacity: '0', transform: 'translateY(30px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideInLeft: {
          '0%': { opacity: '0', transform: 'translateX(-50px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        slideInRight: {
          '0%': { opacity: '0', transform: 'translateX(50px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        pulseGlow: {
          '0%, 100%': { opacity: '0.4' },
          '50%': { opacity: '1' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        gradientShift: {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
        noise: {
          '0%, 100%': { transform: 'translate(0, 0)' },
          '10%': { transform: 'translate(-5%, -10%)' },
          '30%': { transform: 'translate(3%, -15%)' },
          '50%': { transform: 'translate(-15%, 5%)' },
          '70%': { transform: 'translate(10%, 10%)' },
          '90%': { transform: 'translate(15%, -5%)' },
        },
        loadingBar: {
          '0%, 100%': { height: '8px', opacity: '0.4' },
          '50%': { height: '24px', opacity: '1' },
        },
      },
      boxShadow: {
        'glow-violet': '0 0 40px rgba(139, 92, 246, 0.3)',
        'glow-pink': '0 0 40px rgba(236, 72, 153, 0.3)',
        'glow-blue': '0 0 40px rgba(59, 130, 246, 0.3)',
        'glow-amber': '0 0 40px rgba(245, 158, 11, 0.3)',
        'glow-cyan': '0 0 40px rgba(6, 182, 212, 0.3)',
        'enterprise': '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
      },
    },
  },
  plugins: [],
}
export default config
