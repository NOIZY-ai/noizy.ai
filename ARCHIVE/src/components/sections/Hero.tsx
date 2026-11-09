'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'
import { TypeWriter } from '@/components/ui/TypeWriter'
import { AudioVisualizer } from '@/components/ui/AudioVisualizer'
import { cn } from '@/lib/utils'

const heroWords = [
  'Authentic Creativity',
  'Human Artistry',
  'Sonic Innovation',
  'Creative Revolution',
  'Artistic Vision',
]

const stats = [
  { value: '4', label: 'Brands' },
  { value: '5', label: 'AI Agents' },
  { value: '6', label: 'Platforms' },
  { value: '24/7', label: 'Collaboration' },
]

export function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden noise-overlay">
      {/* Animated gradient blobs */}
      <div className="absolute inset-0 overflow-hidden" aria-hidden="true">
        <motion.div
          className="absolute -top-40 -left-40 w-[600px] h-[600px] rounded-full bg-violet-500/15 blur-[120px]"
          animate={{
            x: [0, 50, -30, 0],
            y: [0, -30, 40, 0],
            scale: [1, 1.1, 0.9, 1],
          }}
          transition={{ duration: 20, repeat: Infinity, ease: 'easeInOut' }}
        />
        <motion.div
          className="absolute top-1/3 -right-20 w-[500px] h-[500px] rounded-full bg-pink-500/15 blur-[120px]"
          animate={{
            x: [0, -40, 30, 0],
            y: [0, 40, -20, 0],
            scale: [1, 0.9, 1.1, 1],
          }}
          transition={{ duration: 18, repeat: Infinity, ease: 'easeInOut' }}
        />
        <motion.div
          className="absolute bottom-20 left-1/4 w-[400px] h-[400px] rounded-full bg-amber-500/10 blur-[120px]"
          animate={{
            x: [0, 30, -40, 0],
            y: [0, -40, 20, 0],
          }}
          transition={{ duration: 22, repeat: Infinity, ease: 'easeInOut' }}
        />
      </div>

      {/* Grid overlay */}
      <div
        className="absolute inset-0 opacity-[0.03]"
        style={{
          backgroundImage: `linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)`,
          backgroundSize: '60px 60px',
        }}
        aria-hidden="true"
      />

      <div className="relative z-10 mx-auto max-w-7xl px-6 py-32 sm:py-40 text-center">
        {/* Badge */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <span className="inline-flex items-center gap-2 px-4 py-2 text-xs font-mono uppercase tracking-[0.2em] text-violet-300 bg-violet-500/10 border border-violet-500/20 rounded-full">
            <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
            The Creative Hub
          </span>
        </motion.div>

        {/* Main headline */}
        <motion.h1
          className="mt-8 text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-bold tracking-tight leading-[0.9]"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.15 }}
        >
          <span className="text-noizy-white block">Where AI Meets</span>
          <span className="block mt-2 min-h-[1.1em]">
            <TypeWriter
              words={heroWords}
              className="text-gradient-noizy"
              typingSpeed={70}
              deletingSpeed={35}
              pauseDuration={2500}
            />
          </span>
        </motion.h1>

        {/* Sub-headline */}
        <motion.p
          className="mt-8 max-w-2xl mx-auto text-lg sm:text-xl text-noizy-silver leading-relaxed"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
        >
          Four brands. Five AI agents. One creative revolution. NOIZY.AI is the home
          where{' '}
          <span className="text-noizy-white font-medium">
            HEAVEN, NOIZYLAB, ANTHROPIC NOIZE & DREAM ENGINE
          </span>{' '}
          empower artists to wield AI as an instrument to elevate their craft.
        </motion.p>

        {/* Audio visualizer */}
        <motion.div
          className="mt-10 max-w-md mx-auto"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1, delay: 0.5 }}
        >
          <AudioVisualizer barCount={40} color="#8B5CF6" height={50} />
        </motion.div>

        {/* CTA Buttons */}
        <motion.div
          className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.5 }}
        >
          <Link
            href="#brands"
            className="group relative px-8 py-4 text-base font-medium text-white bg-gradient-to-r from-violet-600 to-pink-600 rounded-2xl hover:from-violet-500 hover:to-pink-500 transition-all duration-500 hover:shadow-glow-violet hover:scale-[1.02]"
          >
            Explore the Brands
            <div className="absolute inset-0 rounded-2xl bg-white/10 opacity-0 group-hover:opacity-100 transition-opacity" />
          </Link>
          <Link
            href="/agents"
            className="px-8 py-4 text-base font-medium text-noizy-silver border border-white/10 rounded-2xl hover:text-noizy-white hover:border-white/20 hover:bg-white/[0.04] transition-all duration-300"
          >
            Meet the Agents
          </Link>
        </motion.div>

        {/* Stats bar */}
        <motion.div
          className="mt-20 grid grid-cols-2 md:grid-cols-4 gap-8 max-w-3xl mx-auto"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.7 }}
        >
          {stats.map((stat) => (
            <div key={stat.label} className="text-center">
              <div className="text-2xl sm:text-3xl font-bold text-noizy-white font-mono">
                {stat.value}
              </div>
              <div className="mt-1 text-xs uppercase tracking-wider text-noizy-silver">
                {stat.label}
              </div>
            </div>
          ))}
        </motion.div>
      </div>

      {/* Bottom gradient fade */}
      <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-noizy-black to-transparent" />
    </section>
  )
}
