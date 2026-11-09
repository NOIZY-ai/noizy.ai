'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'
import { AudioVisualizer } from '@/components/ui/AudioVisualizer'

const capabilities = [
  {
    title: 'AI-Assisted Production',
    description: 'From rough sketch to polished masterpiece. Dream Engine\'s AI understands your creative intent and helps you produce work at the highest professional standard.',
    icon: '01',
  },
  {
    title: 'Multi-Format Mastering',
    description: 'Audio mastering, video rendering, image processing — Dream Engine handles every output format with intelligent optimization for each medium.',
    icon: '02',
  },
  {
    title: 'Visual Content Creation',
    description: 'Generate album artwork, music videos, social content, and visual experiences that match the emotional DNA of your creative work.',
    icon: '03',
  },
  {
    title: 'Distribution & Publishing',
    description: 'One-click multi-platform distribution. Get your work to every major platform with optimized metadata, descriptions, and promotional assets.',
    icon: '04',
  },
]

const stagger = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.12 } },
}

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6 } },
}

export default function DreamEnginePage() {
  return (
    <div className="relative min-h-screen pt-32 pb-20">
      {/* Brand-specific gradient background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none" aria-hidden="true">
        <div className="absolute -top-40 right-1/3 w-[600px] h-[600px] rounded-full bg-cyan-500/10 blur-[150px]" />
        <div className="absolute bottom-1/4 -left-20 w-[500px] h-[500px] rounded-full bg-blue-500/10 blur-[120px]" />
      </div>

      <div className="relative z-10 mx-auto max-w-7xl px-6">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="flex items-center gap-4 mb-8">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-cyan-500 via-blue-500 to-indigo-600 flex items-center justify-center text-white font-bold text-xl">
              DE
            </div>
            <span className="px-3 py-1 text-[10px] font-mono uppercase tracking-wider text-amber-400 bg-amber-500/10 border border-amber-500/20 rounded-full">
              COMING SOON
            </span>
          </div>
        </motion.div>

        <motion.h1
          className="text-5xl sm:text-6xl lg:text-7xl font-bold text-noizy-white leading-[0.9]"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.1 }}
        >
          DREAM ENGINE
        </motion.h1>
        <motion.p
          className="mt-2 text-xl font-mono uppercase tracking-[0.15em] bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 via-blue-400 to-indigo-400"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          The Production Suite
        </motion.p>

        <motion.p
          className="mt-8 text-lg text-noizy-silver max-w-3xl leading-relaxed"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
        >
          The full-spectrum production powerhouse. Dream Engine takes the creative sparks
          from HEAVEN and NOIZYLAB and transforms them into polished, production-ready
          works. AI-assisted mastering, mixing, visual production, and multi-platform distribution.
        </motion.p>

        {/* Audio visualizer */}
        <motion.div
          className="mt-10 max-w-lg"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1, delay: 0.5 }}
        >
          <AudioVisualizer barCount={36} color="#06B6D4" height={55} />
        </motion.div>

        {/* Coming Soon Banner */}
        <motion.div
          className="mt-20 p-10 rounded-3xl bg-gradient-to-br from-cyan-500/5 via-blue-500/5 to-indigo-500/5 border border-cyan-500/10 text-center"
          initial={{ opacity: 0, scale: 0.98 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <div className="text-6xl mb-4">🚀</div>
          <h2 className="text-3xl font-bold text-noizy-white mb-4">
            Under <span className="bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-blue-400">Construction</span>
          </h2>
          <p className="text-lg text-noizy-silver max-w-2xl mx-auto leading-relaxed">
            Dream Engine is being forged. The production suite that will transform raw
            creative energy into polished, professional-grade work across every medium.
            Be the first to know when it launches.
          </p>
        </motion.div>

        {/* Capabilities preview */}
        <motion.div
          className="mt-20 grid md:grid-cols-2 gap-6"
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.1 }}
        >
          {capabilities.map((cap) => (
            <motion.div
              key={cap.title}
              variants={fadeUp}
              className="group p-8 rounded-2xl bg-white/[0.03] border border-white/[0.06] hover:bg-white/[0.05] hover:border-white/[0.1] transition-all duration-500"
            >
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center text-white text-sm font-bold font-mono mb-4">
                {cap.icon}
              </div>
              <h3 className="text-xl font-bold text-noizy-white mb-3">{cap.title}</h3>
              <p className="text-noizy-silver leading-relaxed">{cap.description}</p>
            </motion.div>
          ))}
        </motion.div>

        {/* Pipeline diagram */}
        <motion.div
          className="mt-20 p-10 rounded-3xl bg-white/[0.02] border border-white/[0.06]"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <h3 className="text-xl font-bold text-noizy-white mb-6 text-center">The Creative Pipeline</h3>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            {[
              { brand: 'HEAVEN', desc: 'Ideation', color: 'from-indigo-500 to-violet-500' },
              { brand: 'NOIZYLAB', desc: 'Experimentation', color: 'from-pink-500 to-rose-500' },
              { brand: 'DREAM ENGINE', desc: 'Production', color: 'from-cyan-500 to-blue-500' },
            ].map((step, i) => (
              <div key={step.brand} className="flex items-center gap-4">
                <div className="text-center">
                  <div className={`w-14 h-14 mx-auto rounded-2xl bg-gradient-to-br ${step.color} flex items-center justify-center text-white text-xs font-bold mb-2`}>
                    {String(i + 1).padStart(2, '0')}
                  </div>
                  <div className="text-sm font-bold text-noizy-white">{step.brand}</div>
                  <div className="text-xs text-noizy-silver font-mono">{step.desc}</div>
                </div>
                {i < 2 && (
                  <svg className="w-6 h-6 text-white/20 hidden sm:block" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                  </svg>
                )}
              </div>
            ))}
          </div>
        </motion.div>

        {/* CTA */}
        <motion.div
          className="mt-16 flex flex-col sm:flex-row items-center gap-4"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <Link
            href="/contact"
            className="px-8 py-4 text-base font-medium text-white bg-gradient-to-r from-cyan-600 to-blue-600 rounded-2xl hover:from-cyan-500 hover:to-blue-500 transition-all duration-500"
          >
            Get Notified at Launch
          </Link>
          <Link
            href="/"
            className="px-8 py-4 text-base font-medium text-noizy-silver border border-white/10 rounded-2xl hover:text-noizy-white hover:border-white/20 transition-all"
          >
            Back to Hub
          </Link>
        </motion.div>
      </div>
    </div>
  )
}
