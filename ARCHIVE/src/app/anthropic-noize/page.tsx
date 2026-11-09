'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'
import { AudioVisualizer } from '@/components/ui/AudioVisualizer'

const timeline = [
  {
    era: 'The Spark',
    description: 'Artists first confronted the reality of AI — fear, uncertainty, and the threat of creative obsolescence. But one Canadian visionary saw a different path.',
  },
  {
    era: 'The Pivot',
    description: 'Rather than resist, artists chose to embrace AI as a creative partner. Not a replacement but an instrument to elevate craft. The era of soulless mediocrity began to wane.',
  },
  {
    era: 'The Fusion',
    description: 'Traditional methods merged with cutting-edge AI approaches. This fusion became the new norm, resonating with creators everywhere and birthing a movement.',
  },
  {
    era: 'The Movement',
    description: 'Anthropic Noize exploded into existence — a global creative revolution where technology meets authentic human creativity and the world of art is forever transformed.',
  },
]

const stagger = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.15 } },
}

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6 } },
}

export default function AnthropicNoizePage() {
  return (
    <div className="relative min-h-screen pt-32 pb-20">
      {/* Brand-specific gradient background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none" aria-hidden="true">
        <div className="absolute -top-40 left-1/3 w-[600px] h-[600px] rounded-full bg-amber-500/10 blur-[150px]" />
        <div className="absolute bottom-1/4 -right-20 w-[500px] h-[500px] rounded-full bg-orange-500/10 blur-[120px]" />
      </div>

      <div className="relative z-10 mx-auto max-w-7xl px-6">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="flex items-center gap-4 mb-8">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-amber-500 via-orange-500 to-red-500 flex items-center justify-center text-white font-bold text-xl">
              AN
            </div>
            <span className="px-3 py-1 text-[10px] font-mono uppercase tracking-wider text-blue-400 bg-blue-500/10 border border-blue-500/20 rounded-full">
              IN DEVELOPMENT
            </span>
          </div>
        </motion.div>

        <motion.h1
          className="text-5xl sm:text-6xl lg:text-7xl font-bold text-noizy-white leading-[0.9]"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.1 }}
        >
          ANTHROPIC NOIZE
        </motion.h1>
        <motion.p
          className="mt-2 text-xl font-mono uppercase tracking-[0.15em] bg-clip-text text-transparent bg-gradient-to-r from-amber-400 via-orange-400 to-red-400"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          The Movement
        </motion.p>

        <motion.p
          className="mt-8 text-lg text-noizy-silver max-w-3xl leading-relaxed"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
        >
          More than a brand — a creative revolution. Anthropic Noize is the philosophy
          that drives everything: the belief that AI amplifies rather than replaces human
          creativity. This is the manifesto, the community, the movement that changes
          how artists relate to technology.
        </motion.p>

        {/* Audio visualizer */}
        <motion.div
          className="mt-10 max-w-lg"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1, delay: 0.5 }}
        >
          <AudioVisualizer barCount={36} color="#F59E0B" height={55} />
        </motion.div>

        {/* The Manifesto */}
        <motion.div
          className="mt-20 p-10 rounded-3xl bg-white/[0.02] border border-white/[0.06]"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <h2 className="text-3xl font-bold text-noizy-white mb-6">
            The <span className="bg-clip-text text-transparent bg-gradient-to-r from-amber-400 to-orange-400">Manifesto</span>
          </h2>
          <div className="space-y-6 text-lg text-noizy-silver leading-relaxed">
            <p>
              In an era where many believed creativity was on the brink of extinction,
              and artists faced obsolescence, one Canadian visionary held firm to an
              enduring belief: that{' '}
              <strong className="text-noizy-white">
                creativity thrives not in isolation but in collaboration
              </strong>.
            </p>
            <p>
              Just as Lennon needed McCartney, and Richards complemented Jagger,
              artists flourish when challenged and inspired by dynamic partnerships.
              Nothing compares to the electric synergy of interacting with a counterpart
              who pushes one to uncover their most brilliant ideas.
            </p>
            <p>
              They embraced AI not as a crutch but as a tool to amplify and nurture
              their unique creative talents and passions — and{' '}
              <strong className="text-noizy-white">
                the world of art was forever transformed
              </strong>.
            </p>
          </div>
        </motion.div>

        {/* Timeline */}
        <motion.div
          className="mt-20"
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.1 }}
        >
          <h2 className="text-3xl font-bold text-noizy-white mb-12">
            The <span className="bg-clip-text text-transparent bg-gradient-to-r from-amber-400 to-orange-400">Origin Story</span>
          </h2>
          <div className="space-y-8">
            {timeline.map((event, i) => (
              <motion.div
                key={event.era}
                variants={fadeUp}
                className="flex gap-8"
              >
                <div className="shrink-0 w-16 text-right">
                  <span className="text-sm font-mono text-amber-400/60 uppercase tracking-wider">
                    {String(i + 1).padStart(2, '0')}
                  </span>
                </div>
                <div className="relative pb-8 border-l border-white/[0.08] pl-8">
                  <div className="absolute -left-[5px] top-1.5 w-[10px] h-[10px] rounded-full bg-gradient-to-br from-amber-500 to-orange-500" />
                  <h3 className="text-xl font-bold text-noizy-white mb-2">{event.era}</h3>
                  <p className="text-noizy-silver leading-relaxed">{event.description}</p>
                </div>
              </motion.div>
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
            href="/about"
            className="px-8 py-4 text-base font-medium text-white bg-gradient-to-r from-amber-600 to-orange-600 rounded-2xl hover:from-amber-500 hover:to-orange-500 transition-all duration-500"
          >
            Read the Full Story
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
