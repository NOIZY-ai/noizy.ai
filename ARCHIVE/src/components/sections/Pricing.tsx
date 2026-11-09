'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'
import { pricingTiers } from '@/config/navigation'
import { SectionHeading } from '@/components/ui/SectionHeading'
import { GradientOrb } from '@/components/ui/GradientOrb'
import { formatPrice, cn } from '@/lib/utils'

const containerVariants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.12 } },
}

const cardVariants = {
  hidden: { opacity: 0, y: 30, scale: 0.97 },
  visible: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: { duration: 0.6, ease: [0.25, 0.46, 0.45, 0.94] },
  },
}

export function Pricing() {
  return (
    <section className="relative py-32 overflow-hidden" id="pricing">
      <GradientOrb color="violet" size="lg" className="top-1/3 left-1/2 -translate-x-1/2 opacity-20" />

      <div className="relative z-10 mx-auto max-w-7xl px-6">
        <SectionHeading
          badge="Pricing"
          title="Invest in Your"
          titleHighlight="Creative Future"
          description="Simple, transparent pricing. Start free, scale when you're ready. No hidden fees, no creative limits."
        />

        <motion.div
          className="mt-16 grid md:grid-cols-3 gap-6 max-w-5xl mx-auto"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.1 }}
        >
          {pricingTiers.map((tier) => (
            <motion.div
              key={tier.name}
              variants={cardVariants}
              className={cn(
                'relative p-8 rounded-2xl transition-all duration-500',
                tier.highlighted
                  ? 'glass-heavy border-violet-500/30 scale-[1.02] shadow-glow-violet'
                  : 'glass',
              )}
            >
              {tier.highlighted && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-4 py-1 text-xs font-mono uppercase tracking-wider text-white bg-gradient-to-r from-violet-600 to-pink-600 rounded-full">
                  Most Popular
                </div>
              )}

              <h3 className="text-lg font-bold text-noizy-white">{tier.name}</h3>

              <div className="mt-4 flex items-baseline gap-1">
                <span className="text-4xl font-bold text-noizy-white">
                  {formatPrice(tier.price, tier.currency)}
                </span>
                {tier.price > 0 && (
                  <span className="text-sm text-noizy-silver">
                    /{tier.interval}
                  </span>
                )}
              </div>

              <ul className="mt-8 space-y-3">
                {tier.features.map((feature) => (
                  <li key={feature} className="flex items-start gap-3 text-sm text-noizy-silver">
                    <svg className="w-4 h-4 mt-0.5 text-violet-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                    </svg>
                    {feature}
                  </li>
                ))}
              </ul>

              <Link
                href={tier.name === 'Enterprise' ? '/contact' : '/pricing'}
                className={cn(
                  'mt-8 block w-full py-3 text-center text-sm font-medium rounded-xl transition-all duration-300',
                  tier.highlighted
                    ? 'text-white bg-gradient-to-r from-violet-600 to-pink-600 hover:from-violet-500 hover:to-pink-500 hover:shadow-glow-violet'
                    : 'text-noizy-silver border border-white/10 hover:text-noizy-white hover:border-white/20 hover:bg-white/[0.04]'
                )}
              >
                {tier.cta}
              </Link>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  )
}
