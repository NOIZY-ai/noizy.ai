'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'
import { pricingTiers } from '@/config/navigation'
import { formatPrice, cn } from '@/lib/utils'

const faqs = [
  {
    q: 'Can I switch plans anytime?',
    a: 'Absolutely. Upgrade or downgrade at any time. Changes take effect immediately, and we prorate billing automatically.',
  },
  {
    q: 'Is there a free trial for Creator?',
    a: 'Yes! Start with Explorer for free, then upgrade to Creator with a 14-day free trial. No credit card required to start.',
  },
  {
    q: 'What counts as a creative session?',
    a: 'A creative session is an interaction with one or more AI agents. Explorer gets 10/month, Creator and Enterprise get unlimited.',
  },
  {
    q: 'Do you offer student or artist discounts?',
    a: 'Yes. We offer 50% off Creator plans for verified students and independent artists. Contact us for details.',
  },
  {
    q: 'What about enterprise custom deployments?',
    a: 'Enterprise plans include custom AI agent training, dedicated infrastructure, API access, SSO, and optional on-premise deployment.',
  },
  {
    q: 'How does voice integration work?',
    a: 'Creator and Enterprise plans include voice-powered creative sessions. Speak naturally with your AI agents for a more intuitive collaboration experience.',
  },
  {
    q: 'Which brands are included?',
    a: 'All plans grant access to HEAVEN and NOIZYLAB. ANTHROPIC NOIZE community features are free. DREAM ENGINE production tools are available on Creator and Enterprise.',
  },
]

const stagger = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.1 } },
}

const fadeUp = {
  hidden: { opacity: 0, y: 30, scale: 0.97 },
  visible: { opacity: 1, y: 0, scale: 1, transition: { duration: 0.6, ease: [0.25, 0.46, 0.45, 0.94] } },
}

const faqStagger = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.06 } },
}

const faqItem = {
  hidden: { opacity: 0, y: 15 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.4 } },
}

export default function PricingPage() {
  return (
    <div className="relative min-h-screen pt-32 pb-20">
      {/* Background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none" aria-hidden="true">
        <motion.div
          className="absolute top-1/3 left-1/2 -translate-x-1/2 w-[600px] h-[600px] rounded-full bg-violet-500/10 blur-[150px]"
          animate={{ scale: [1, 1.1, 1], opacity: [0.1, 0.15, 0.1] }}
          transition={{ duration: 12, repeat: Infinity, ease: 'easeInOut' }}
        />
      </div>

      <div className="relative z-10 mx-auto max-w-7xl px-6">
        <div className="text-center">
          <motion.span
            className="inline-block px-4 py-1.5 text-xs font-mono uppercase tracking-[0.2em] text-violet-400 bg-violet-500/10 border border-violet-500/20 rounded-full mb-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            Pricing
          </motion.span>
          <motion.h1
            className="text-4xl sm:text-5xl lg:text-6xl font-bold text-noizy-white leading-tight"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.1 }}
          >
            Simple, Transparent{' '}
            <span className="text-gradient-noizy">Pricing</span>
          </motion.h1>
          <motion.p
            className="mt-6 text-lg text-noizy-silver max-w-xl mx-auto"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.2 }}
          >
            Start free, scale when ready. All plans include updates, new agent releases, and access to all four brands.
          </motion.p>
        </div>

        {/* Pricing Cards */}
        <motion.div
          className="mt-16 grid md:grid-cols-3 gap-6 max-w-5xl mx-auto"
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.1 }}
        >
          {pricingTiers.map((tier) => (
            <motion.div
              key={tier.name}
              variants={fadeUp}
              whileHover={{ y: -4, transition: { duration: 0.3 } }}
              className={cn(
                'relative p-8 rounded-2xl transition-all duration-500',
                tier.highlighted
                  ? 'bg-white/[0.06] backdrop-blur-2xl border border-violet-500/30 shadow-glow-violet scale-[1.02]'
                  : 'bg-white/[0.03] backdrop-blur-xl border border-white/[0.06] hover:border-white/[0.1]'
              )}
            >
              {tier.highlighted && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-4 py-1 text-xs font-mono uppercase tracking-wider text-white bg-gradient-to-r from-violet-600 to-pink-600 rounded-full">
                  Most Popular
                </div>
              )}

              <h3 className="text-lg font-bold text-noizy-white">{tier.name}</h3>
              <div className="mt-4 flex items-baseline gap-1">
                <span className="text-5xl font-bold text-noizy-white">
                  {formatPrice(tier.price, tier.currency)}
                </span>
                {tier.price > 0 && (
                  <span className="text-sm text-noizy-silver">/{tier.interval}</span>
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
                href={tier.name === 'Enterprise' ? '/contact' : '#'}
                className={cn(
                  'mt-8 block w-full py-3.5 text-center text-sm font-medium rounded-xl transition-all duration-300',
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

        {/* Brand access table */}
        <motion.div
          className="mt-20 max-w-4xl mx-auto"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <h2 className="text-2xl font-bold text-noizy-white text-center mb-8">
            Brand Access by <span className="text-gradient-noizy">Plan</span>
          </h2>
          <div className="rounded-2xl bg-white/[0.02] border border-white/[0.06] overflow-hidden">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-white/[0.06]">
                  <th className="px-6 py-4 text-left font-mono text-xs uppercase tracking-wider text-noizy-silver">Brand</th>
                  <th className="px-6 py-4 text-center font-mono text-xs uppercase tracking-wider text-noizy-silver">Explorer</th>
                  <th className="px-6 py-4 text-center font-mono text-xs uppercase tracking-wider text-violet-400 bg-violet-500/5">Creator</th>
                  <th className="px-6 py-4 text-center font-mono text-xs uppercase tracking-wider text-noizy-silver">Enterprise</th>
                </tr>
              </thead>
              <tbody>
                {[
                  { brand: 'HEAVEN', explorer: 'Basic', creator: 'Full', enterprise: 'Full + Custom' },
                  { brand: 'NOIZYLAB', explorer: '1 Agent', creator: 'All 5 Agents', enterprise: 'All + Custom Training' },
                  { brand: 'ANTHROPIC NOIZE', explorer: 'Community', creator: 'Full Access', enterprise: 'Full + Events' },
                  { brand: 'DREAM ENGINE', explorer: '—', creator: 'Full Suite', enterprise: 'Full + API' },
                ].map((row, i) => (
                  <tr key={row.brand} className={cn('border-b border-white/[0.04]', i % 2 === 0 && 'bg-white/[0.01]')}>
                    <td className="px-6 py-4 font-bold text-noizy-white">{row.brand}</td>
                    <td className="px-6 py-4 text-center text-noizy-silver">{row.explorer}</td>
                    <td className="px-6 py-4 text-center text-noizy-white bg-violet-500/5 font-medium">{row.creator}</td>
                    <td className="px-6 py-4 text-center text-noizy-silver">{row.enterprise}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </motion.div>

        {/* FAQ */}
        <div className="mt-32 max-w-3xl mx-auto">
          <motion.h2
            className="text-3xl font-bold text-noizy-white text-center mb-12"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            Frequently Asked <span className="text-gradient-noizy">Questions</span>
          </motion.h2>
          <motion.div
            className="space-y-4"
            variants={faqStagger}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.1 }}
          >
            {faqs.map((faq) => (
              <motion.div
                key={faq.q}
                variants={faqItem}
                className="p-6 rounded-2xl bg-white/[0.03] border border-white/[0.06] hover:bg-white/[0.05] hover:border-white/[0.08] transition-all duration-300"
              >
                <h3 className="text-base font-bold text-noizy-white">{faq.q}</h3>
                <p className="mt-2 text-sm text-noizy-silver leading-relaxed">{faq.a}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </div>
    </div>
  )
}
