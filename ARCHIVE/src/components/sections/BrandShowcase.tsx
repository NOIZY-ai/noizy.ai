'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'
import { brands } from '@/config/brands'
import { SectionHeading } from '@/components/ui/SectionHeading'
import { AudioVisualizer } from '@/components/ui/AudioVisualizer'
import { cn } from '@/lib/utils'

const statusLabels = {
  'live': { text: 'LIVE', color: 'text-green-400 bg-green-500/10 border-green-500/20' },
  'coming-soon': { text: 'COMING SOON', color: 'text-amber-400 bg-amber-500/10 border-amber-500/20' },
  'in-development': { text: 'IN DEVELOPMENT', color: 'text-blue-400 bg-blue-500/10 border-blue-500/20' },
}

const containerVariants = {
  hidden: {},
  visible: {
    transition: { staggerChildren: 0.15 },
  },
}

const cardVariants = {
  hidden: { opacity: 0, y: 40, scale: 0.95 },
  visible: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: { duration: 0.7, ease: [0.25, 0.46, 0.45, 0.94] },
  },
}

export function BrandShowcase() {
  return (
    <section className="relative py-32 overflow-hidden" id="brands">
      <div className="relative z-10 mx-auto max-w-7xl px-6">
        <SectionHeading
          badge="The Ecosystem"
          title="Four Brands,"
          titleHighlight="One Vision"
          description="NOIZY.AI is the home of four interconnected brands — each a different dimension of the creative revolution where AI amplifies authentic human artistry."
        />

        <motion.div
          className="mt-16 grid md:grid-cols-2 gap-6"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.1 }}
        >
          {brands.map((brand) => {
            const status = statusLabels[brand.status]
            return (
              <motion.div key={brand.id} variants={cardVariants}>
                <Link
                  href={brand.href}
                  className={cn(
                    'group relative block p-8 sm:p-10 rounded-3xl',
                    'bg-white/[0.02] border border-white/[0.06]',
                    'hover:bg-white/[0.05] hover:border-white/[0.12]',
                    'transition-all duration-700',
                    'overflow-hidden'
                  )}
                >
                  {/* Top gradient line */}
                  <div
                    className={cn(
                      'absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r opacity-40 group-hover:opacity-80 transition-opacity duration-700',
                      brand.gradient
                    )}
                  />

                  {/* Background glow on hover */}
                  <div
                    className={cn(
                      'absolute -top-20 -right-20 w-60 h-60 rounded-full blur-[100px] opacity-0 group-hover:opacity-20 transition-opacity duration-700',
                      `bg-[${brand.accentColor}]`
                    )}
                    style={{ backgroundColor: brand.accentColor }}
                  />

                  <div className="relative z-10">
                    {/* Header */}
                    <div className="flex items-start justify-between mb-6">
                      <div className="flex items-center gap-4">
                        <div
                          className={cn(
                            'w-14 h-14 rounded-2xl bg-gradient-to-br flex items-center justify-center text-white font-bold text-lg shrink-0',
                            'group-hover:scale-110 group-hover:shadow-lg transition-all duration-500',
                            brand.gradient
                          )}
                        >
                          {brand.icon}
                        </div>
                        <div>
                          <h3 className="text-2xl font-bold text-noizy-white group-hover:text-gradient-noizy transition-all duration-500">
                            {brand.name}
                          </h3>
                          <p className="text-xs font-mono uppercase tracking-[0.15em] text-noizy-silver mt-0.5">
                            {brand.tagline}
                          </p>
                        </div>
                      </div>
                      <span
                        className={cn(
                          'px-3 py-1 text-[10px] font-mono uppercase tracking-wider rounded-full border shrink-0',
                          status.color
                        )}
                      >
                        {status.text}
                      </span>
                    </div>

                    {/* Description */}
                    <p className="text-noizy-silver leading-relaxed mb-6">
                      {brand.description}
                    </p>

                    {/* Features */}
                    <div className="flex flex-wrap gap-2 mb-6">
                      {brand.features.map((feature) => (
                        <span
                          key={feature}
                          className="px-3 py-1.5 text-[11px] font-mono uppercase tracking-wider text-noizy-silver bg-white/[0.04] rounded-lg border border-white/[0.06]"
                        >
                          {feature}
                        </span>
                      ))}
                    </div>

                    {/* Audio visualizer */}
                    <div className="opacity-40 group-hover:opacity-70 transition-opacity duration-700">
                      <AudioVisualizer
                        barCount={24}
                        color={brand.accentColor}
                        height={40}
                      />
                    </div>

                    {/* Enter arrow */}
                    <div className="mt-6 flex items-center gap-2 text-sm font-medium text-noizy-silver group-hover:text-noizy-white transition-colors">
                      <span>Explore {brand.name}</span>
                      <svg
                        className="w-4 h-4 transform group-hover:translate-x-1 transition-transform"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        strokeWidth={2}
                      >
                        <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                      </svg>
                    </div>
                  </div>
                </Link>
              </motion.div>
            )
          })}
        </motion.div>

        {/* Ecosystem connection */}
        <motion.div
          className="mt-16 p-10 rounded-3xl bg-white/[0.02] border border-white/[0.06] text-center"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: 0.3 }}
        >
          <div className="flex items-center justify-center gap-3 mb-6">
            {brands.map((brand, i) => (
              <div key={brand.id} className="flex items-center gap-3">
                <div
                  className={cn(
                    'w-10 h-10 rounded-xl bg-gradient-to-br flex items-center justify-center text-white text-xs font-bold',
                    brand.gradient
                  )}
                >
                  {brand.icon}
                </div>
                {i < brands.length - 1 && (
                  <div className="w-8 h-px bg-gradient-to-r from-white/20 to-white/5" />
                )}
              </div>
            ))}
          </div>
          <h3 className="text-xl font-bold text-noizy-white mb-2">
            The Complete <span className="text-gradient-noizy">Creative Ecosystem</span>
          </h3>
          <p className="text-noizy-silver max-w-2xl mx-auto leading-relaxed">
            Each brand is a pillar of the NOIZY.AI vision. Together they form a complete
            creative ecosystem — from ideation to production, from solo exploration to
            community movement.
          </p>
        </motion.div>
      </div>
    </section>
  )
}
