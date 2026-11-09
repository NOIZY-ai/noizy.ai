'use client'

import { motion } from 'framer-motion'

interface NOIZYLogoProps {
  size?: number
  className?: string
  animate?: boolean
}

export function NOIZYLogo({ size = 40, className = '', animate = true }: NOIZYLogoProps) {
  return (
    <motion.div
      className={`relative rounded-xl overflow-hidden flex items-center justify-center ${className}`}
      style={{ width: size, height: size }}
      whileHover={animate ? { scale: 1.1, rotate: 3 } : undefined}
      transition={{ type: 'spring', stiffness: 400, damping: 15 }}
    >
      {/* Animated gradient background */}
      <motion.div
        className="absolute inset-0"
        style={{
          background: 'linear-gradient(135deg, #8B5CF6, #EC4899, #F59E0B, #06B6D4)',
          backgroundSize: '300% 300%',
        }}
        animate={animate ? {
          backgroundPosition: ['0% 0%', '100% 100%', '0% 0%'],
        } : undefined}
        transition={{ duration: 8, repeat: Infinity, ease: 'easeInOut' }}
      />

      {/* Inner glow pulse */}
      {animate && (
        <motion.div
          className="absolute inset-0 bg-white/20 rounded-xl"
          animate={{ opacity: [0, 0.3, 0] }}
          transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
        />
      )}

      {/* Letter */}
      <span
        className="relative z-10 text-white font-bold"
        style={{ fontSize: size * 0.45 }}
      >
        N
      </span>
    </motion.div>
  )
}
