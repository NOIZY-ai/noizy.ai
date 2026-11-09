'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'
import { brands } from '@/config/brands'
import { AudioVisualizer } from '@/components/ui/AudioVisualizer'
import { cn } from '@/lib/utils'

const stagger = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.12 } },
}

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6 } },
}

export default function AboutPage() {
  return (
    <div className="relative min-h-screen pt-32 pb-20">
      <div className="mx-auto max-w-4xl px-6">
        {/* Header */}
        <motion.span
          className="inline-block px-4 py-1.5 text-xs font-mono uppercase tracking-[0.2em] text-violet-400 bg-violet-500/10 border border-violet-500/20 rounded-full mb-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          Our Story
        </motion.span>
        <motion.h1
          className="text-4xl sm:text-5xl lg:text-6xl font-bold text-noizy-white leading-tight"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.1 }}
        >
          The Anthropic Noize{' '}
          <span className="text-gradient-noizy">Origin</span>
        </motion.h1>

        {/* Audio visualizer */}
        <motion.div
          className="mt-8 max-w-md"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1, delay: 0.3 }}
        >
          <AudioVisualizer barCount={32} color="#8B5CF6" height={40} />
        </motion.div>

        {/* Narrative */}
        <motion.div
          className="mt-12 space-y-8 text-lg text-noizy-silver leading-relaxed"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
        >
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
            Artists could indeed create solo or lean on AI to generate content.
            However, nothing compares to the electric synergy of interacting with
            a counterpart who pushes one to uncover their most brilliant ideas.
          </p>

          <p>
            This essence was the catalyst behind NOIZY.AI and its four transformative
            brands. They revolutionized the perception of AI among artists,
            empowering them to{' '}
            <strong className="text-noizy-white">
              reclaim their creative authority
            </strong>.
          </p>

          <div className="p-8 rounded-2xl bg-white/[0.03] border border-white/[0.06]">
            <p className="text-xl text-noizy-white font-medium italic">
              &ldquo;The era of soulless, greed-driven creations — masquerading mediocrity
              as gold — began to wane. While some individuals surrendered their
              curiosity and imagination, others chose a different path.&rdquo;
            </p>
          </div>

          <p>
            They embraced AI not as a crutch but as a tool to amplify and nurture
            their unique creative talents and passions. Harnessing the data and
            technological knowledge of the time, they fused traditional methods
            with cutting-edge approaches, constantly seeking the most effective
            paths. This fusion became the new norm, resonating with creators
            everywhere.
          </p>

          <p>
            When did Anthropic Noize originate? It began the moment artists
            decided to wield AI not as a replacement but as an instrument to
            elevate their craft — a pivotal juncture where technology met
            authentic human creativity, and{' '}
            <strong className="text-noizy-white">
              the world of art was forever transformed
            </strong>.
          </p>
        </motion.div>

        {/* Brand Cards */}
        <motion.div
          className="mt-20 grid md:grid-cols-2 gap-6"
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.1 }}
        >
          {brands.map((brand) => (
            <motion.div key={brand.id} variants={fadeUp}>
              <Link
                href={brand.href}
                className="group block p-8 rounded-2xl bg-white/[0.03] border border-white/[0.06] hover:bg-white/[0.05] hover:border-white/[0.1] transition-all duration-500"
              >
                <div className="flex items-center gap-3 mb-3">
                  <div className={cn(
                    'w-10 h-10 rounded-xl bg-gradient-to-br flex items-center justify-center text-white text-sm font-bold',
                    brand.gradient
                  )}>
                    {brand.icon}
                  </div>
                  <h3 className="text-xl font-bold text-noizy-white group-hover:text-gradient-noizy transition-all">
                    {brand.name}
                  </h3>
                </div>
                <p className="text-xs font-mono uppercase tracking-wider text-noizy-silver/60 mb-3">
                  {brand.tagline}
                </p>
                <p className="text-noizy-silver leading-relaxed">
                  {brand.description}
                </p>
              </Link>
            </motion.div>
          ))}
        </motion.div>

        {/* Founder */}
        <motion.div
          className="mt-20 text-center"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <div className="inline-block p-8 rounded-2xl bg-white/[0.03] border border-white/[0.06]">
            <div className="w-20 h-20 mx-auto rounded-full bg-gradient-to-br from-violet-500 via-pink-500 to-amber-500 flex items-center justify-center text-3xl mb-4">
              🎤
            </div>
            <h3 className="text-xl font-bold text-noizy-white">
              Robert Stephen Plowman
            </h3>
            <p className="text-sm text-noizy-silver mt-1 font-mono uppercase tracking-wider">
              Founder & Creative Visionary
            </p>
            <p className="text-noizy-silver mt-4 max-w-md leading-relaxed">
              A Canadian innovator who saw the future where AI and human creativity
              don&apos;t compete — they collaborate, creating something neither could
              achieve alone. Voice performer, artist, and the driving force behind
              TALESPIN and the Anthropic Noize movement.
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  )
}
