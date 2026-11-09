'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'
import { AudioVisualizer } from '@/components/ui/AudioVisualizer'

const features = [
  {
    title: 'Immersive Sonic Environments',
    description: 'Step into AI-crafted soundscapes that respond to your creative energy. HEAVEN builds the atmosphere where your best ideas emerge naturally.',
    icon: '01',
  },
  {
    title: 'Voice-Driven Artistry',
    description: 'Your voice is your instrument. HEAVEN\'s voice integration captures the raw emotion and intention behind every creative impulse — including original TALESPIN performances.',
    icon: '02',
  },
  {
    title: 'Cross-Medium Fusion',
    description: 'Break the barriers between sound, vision, and text. HEAVEN seamlessly blends creative mediums into unified artistic expressions.',
    icon: '03',
  },
  {
    title: 'Sacred Creative Space',
    description: 'A distraction-free sanctuary designed for deep creative flow. HEAVEN protects the sacred space where authentic artistry is born.',
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

export default function HeavenPage() {
  return (
    <div className="relative min-h-screen pt-32 pb-20">
      {/* Brand-specific gradient background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none" aria-hidden="true">
        <div className="absolute -top-40 left-1/4 w-[600px] h-[600px] rounded-full bg-indigo-500/10 blur-[150px]" />
        <div className="absolute top-1/2 -right-20 w-[500px] h-[500px] rounded-full bg-violet-500/10 blur-[120px]" />
        <div className="absolute bottom-0 left-0 w-[400px] h-[400px] rounded-full bg-purple-500/8 blur-[100px]" />
      </div>

      <div className="relative z-10 mx-auto max-w-7xl px-6">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="flex items-center gap-4 mb-8">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-500 via-violet-500 to-purple-600 flex items-center justify-center text-white font-bold text-2xl">
              H
            </div>
            <div>
              <span className="px-3 py-1 text-[10px] font-mono uppercase tracking-wider text-green-400 bg-green-500/10 border border-green-500/20 rounded-full">
                LIVE
              </span>
            </div>
          </div>
        </motion.div>

        <motion.h1
          className="text-5xl sm:text-6xl lg:text-7xl font-bold text-noizy-white leading-[0.9]"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.1 }}
        >
          HEAVEN
        </motion.h1>
        <motion.p
          className="mt-2 text-xl font-mono uppercase tracking-[0.15em] text-gradient-heaven"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          The Creative Sanctuary
        </motion.p>

        <motion.p
          className="mt-8 text-lg text-noizy-silver max-w-3xl leading-relaxed"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
        >
          Where human intuition meets machine intelligence. HEAVEN is the sacred creative
          space where authentic artistry is born, nurtured, and elevated beyond what either
          human or AI could achieve alone. The spiritual home of the Anthropic Noize movement.
        </motion.p>

        {/* Audio visualizer */}
        <motion.div
          className="mt-10 max-w-lg"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1, delay: 0.5 }}
        >
          <AudioVisualizer barCount={36} color="#8B5CF6" height={55} />
          <p className="mt-2 text-xs font-mono text-noizy-silver/40 uppercase tracking-wider">
            Audio visualizer — TALESPIN voice performances coming soon
          </p>
        </motion.div>

        {/* Features */}
        <motion.div
          className="mt-20 grid md:grid-cols-2 gap-6"
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.1 }}
        >
          {features.map((feature) => (
            <motion.div
              key={feature.title}
              variants={fadeUp}
              className="group p-8 rounded-2xl bg-white/[0.03] border border-white/[0.06] hover:bg-white/[0.05] hover:border-white/[0.1] transition-all duration-500"
            >
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center text-white text-sm font-bold font-mono mb-4">
                {feature.icon}
              </div>
              <h3 className="text-xl font-bold text-noizy-white mb-3 group-hover:text-gradient-heaven transition-all">
                {feature.title}
              </h3>
              <p className="text-noizy-silver leading-relaxed">{feature.description}</p>
            </motion.div>
          ))}
        </motion.div>

        {/* Manifesto section */}
        <motion.div
          className="mt-20 p-10 rounded-3xl bg-white/[0.02] border border-white/[0.06] text-center"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <blockquote className="text-xl sm:text-2xl font-medium text-noizy-white leading-relaxed italic max-w-3xl mx-auto">
            &ldquo;HEAVEN is not a place you go — it&apos;s a state you create. When the noise
            of the world fades and all that remains is pure creative intention,
            you&apos;ve found HEAVEN.&rdquo;
          </blockquote>
          <cite className="mt-6 block text-sm text-noizy-silver not-italic font-mono uppercase tracking-wider">
            — Robert Stephen Plowman
          </cite>
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
            href="/pricing"
            className="px-8 py-4 text-base font-medium text-white bg-gradient-to-r from-indigo-600 to-violet-600 rounded-2xl hover:from-indigo-500 hover:to-violet-500 transition-all duration-500 hover:shadow-glow-violet"
          >
            Enter HEAVEN
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
