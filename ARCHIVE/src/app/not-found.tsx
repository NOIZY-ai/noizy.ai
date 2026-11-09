'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'
import { AudioVisualizer } from '@/components/ui/AudioVisualizer'

export default function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center px-6 relative overflow-hidden">
      {/* Background glitch effect */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none" aria-hidden="true">
        <motion.div
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] rounded-full bg-violet-500/10 blur-[120px]"
          animate={{ scale: [1, 1.3, 1], opacity: [0.1, 0.2, 0.1] }}
          transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
        />
      </div>

      <div className="relative z-10 text-center">
        <motion.div
          className="text-[120px] sm:text-[160px] font-bold leading-none mb-2 relative"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, ease: [0.25, 0.46, 0.45, 0.94] }}
        >
          {/* Glitch layers */}
          <span className="text-gradient-noizy relative inline-block">
            404
          </span>
        </motion.div>

        <motion.h1
          className="text-2xl sm:text-3xl font-bold text-noizy-white mb-4"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          Lost in the Noise
        </motion.h1>

        <motion.p
          className="text-noizy-silver mb-6 max-w-md mx-auto leading-relaxed"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
        >
          This frequency doesn&apos;t exist yet. The signal you&apos;re looking for
          might be in another dimension of the NOIZY.AI creative hub.
        </motion.p>

        {/* Audio visualizer as "static noise" */}
        <motion.div
          className="max-w-xs mx-auto mb-8 opacity-40"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.4 }}
          transition={{ duration: 1, delay: 0.5 }}
        >
          <AudioVisualizer barCount={20} color="#8B5CF6" height={35} />
        </motion.div>

        <motion.div
          className="flex flex-col sm:flex-row gap-3 justify-center"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.5 }}
        >
          <Link
            href="/"
            className="inline-block px-8 py-3 text-sm font-medium text-white bg-gradient-to-r from-violet-600 to-pink-600 rounded-xl hover:from-violet-500 hover:to-pink-500 transition-all hover:shadow-glow-violet"
          >
            Back to Hub
          </Link>
          <Link
            href="#brands"
            className="inline-block px-8 py-3 text-sm font-medium text-noizy-silver border border-white/10 rounded-xl hover:text-noizy-white hover:border-white/20 transition-all"
          >
            Explore Brands
          </Link>
        </motion.div>
      </div>
    </div>
  )
}
