'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'
import { GradientOrb } from '@/components/ui/GradientOrb'
import { AudioVisualizer } from '@/components/ui/AudioVisualizer'

export function CTA() {
  return (
    <section className="relative py-32 overflow-hidden">
      <GradientOrb color="violet" size="xl" className="top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 opacity-20" />

      <div className="relative z-10 mx-auto max-w-4xl px-6 text-center">
        <motion.div
          className="p-12 sm:p-16 rounded-3xl glass-heavy"
          initial={{ opacity: 0, y: 30, scale: 0.98 }}
          whileInView={{ opacity: 1, y: 0, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-noizy-white leading-tight">
            Ready to{' '}
            <span className="text-gradient-noizy">Amplify</span>
            <br />Your Creative Voice?
          </h2>
          <p className="mt-6 text-lg text-noizy-silver max-w-xl mx-auto">
            Join the movement of artists who chose to embrace AI not as a crutch,
            but as an instrument to elevate their craft.
          </p>

          {/* Audio visualizer accent */}
          <div className="mt-8 max-w-sm mx-auto opacity-50">
            <AudioVisualizer barCount={28} color="#8B5CF6" height={35} />
          </div>

          <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              href="/pricing"
              className="px-10 py-4 text-base font-medium text-white bg-gradient-to-r from-violet-600 to-pink-600 rounded-2xl hover:from-violet-500 hover:to-pink-500 transition-all duration-500 hover:shadow-glow-violet hover:scale-[1.02]"
            >
              Start Your Journey
            </Link>
            <Link
              href="/contact"
              className="px-10 py-4 text-base font-medium text-noizy-silver border border-white/10 rounded-2xl hover:text-noizy-white hover:border-white/20 hover:bg-white/[0.04] transition-all duration-300"
            >
              Talk to Us
            </Link>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
