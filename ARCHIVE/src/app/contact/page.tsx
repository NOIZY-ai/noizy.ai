'use client'

import { motion } from 'framer-motion'
import { AudioVisualizer } from '@/components/ui/AudioVisualizer'

const stagger = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.1 } },
}

const fadeUp = {
  hidden: { opacity: 0, y: 25 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
}

const contactCards = [
  {
    title: 'Enterprise Sales',
    description: 'Custom AI agent training, dedicated infrastructure, SSO, API access, and white-label solutions for teams and organizations.',
    email: 'enterprise@noizy.ai',
    color: '#8B5CF6',
  },
  {
    title: 'Partnerships',
    description: 'Interested in integrating NOIZY.AI into your platform or collaborating on creative technology across HEAVEN, NOIZYLAB, or DREAM ENGINE?',
    email: 'partners@noizy.ai',
    color: '#EC4899',
  },
  {
    title: 'Support',
    description: 'Need help with your creative sessions, agents, or account? Creator and Enterprise plans get priority support.',
    email: 'support@noizy.ai',
    color: '#06B6D4',
  },
]

export default function ContactPage() {
  return (
    <div className="relative min-h-screen pt-32 pb-20">
      {/* Background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none" aria-hidden="true">
        <motion.div
          className="absolute top-1/4 -right-20 w-[500px] h-[500px] rounded-full bg-violet-500/8 blur-[150px]"
          animate={{ y: [0, -30, 0] }}
          transition={{ duration: 15, repeat: Infinity, ease: 'easeInOut' }}
        />
      </div>

      <div className="relative z-10 mx-auto max-w-4xl px-6">
        <div className="text-center">
          <motion.span
            className="inline-block px-4 py-1.5 text-xs font-mono uppercase tracking-[0.2em] text-violet-400 bg-violet-500/10 border border-violet-500/20 rounded-full mb-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            Contact
          </motion.span>
          <motion.h1
            className="text-4xl sm:text-5xl lg:text-6xl font-bold text-noizy-white leading-tight"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.1 }}
          >
            Let&apos;s Create{' '}
            <span className="text-gradient-noizy">Together</span>
          </motion.h1>
          <motion.p
            className="mt-6 text-lg text-noizy-silver max-w-xl mx-auto"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.2 }}
          >
            Whether you&apos;re an independent artist, a studio, or an enterprise — we&apos;re here to help you amplify your creative vision across all four NOIZY.AI brands.
          </motion.p>
        </div>

        {/* Audio visualizer accent */}
        <motion.div
          className="mt-8 max-w-xs mx-auto opacity-40"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 0.4, scale: 1 }}
          transition={{ duration: 1, delay: 0.4 }}
        >
          <AudioVisualizer barCount={20} color="#8B5CF6" height={30} />
        </motion.div>

        <div className="mt-16 grid md:grid-cols-2 gap-8">
          {/* Contact Form */}
          <motion.div
            className="p-8 rounded-2xl bg-white/[0.03] border border-white/[0.06]"
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.7, delay: 0.3 }}
          >
            <h2 className="text-xl font-bold text-noizy-white mb-6">Send a Message</h2>
            <form className="space-y-4">
              <div>
                <label htmlFor="name" className="block text-sm text-noizy-silver mb-2">Name</label>
                <input
                  id="name"
                  type="text"
                  className="w-full px-4 py-3 rounded-xl bg-white/[0.04] border border-white/[0.08] text-noizy-white placeholder:text-noizy-silver/40 focus:outline-none focus:border-violet-500/50 focus:ring-1 focus:ring-violet-500/20 transition-all"
                  placeholder="Your name"
                />
              </div>
              <div>
                <label htmlFor="email" className="block text-sm text-noizy-silver mb-2">Email</label>
                <input
                  id="email"
                  type="email"
                  className="w-full px-4 py-3 rounded-xl bg-white/[0.04] border border-white/[0.08] text-noizy-white placeholder:text-noizy-silver/40 focus:outline-none focus:border-violet-500/50 focus:ring-1 focus:ring-violet-500/20 transition-all"
                  placeholder="you@example.com"
                />
              </div>
              <div>
                <label htmlFor="type" className="block text-sm text-noizy-silver mb-2">Inquiry Type</label>
                <select
                  id="type"
                  className="w-full px-4 py-3 rounded-xl bg-white/[0.04] border border-white/[0.08] text-noizy-silver focus:outline-none focus:border-violet-500/50 focus:ring-1 focus:ring-violet-500/20 transition-all"
                >
                  <option value="general">General Inquiry</option>
                  <option value="heaven">HEAVEN — Creative Collaboration</option>
                  <option value="noizylab">NOIZYLAB — Agent Training</option>
                  <option value="dream-engine">DREAM ENGINE — Production Suite</option>
                  <option value="enterprise">Enterprise</option>
                  <option value="partnership">Partnership</option>
                  <option value="support">Support</option>
                  <option value="press">Press</option>
                </select>
              </div>
              <div>
                <label htmlFor="message" className="block text-sm text-noizy-silver mb-2">Message</label>
                <textarea
                  id="message"
                  rows={5}
                  className="w-full px-4 py-3 rounded-xl bg-white/[0.04] border border-white/[0.08] text-noizy-white placeholder:text-noizy-silver/40 focus:outline-none focus:border-violet-500/50 focus:ring-1 focus:ring-violet-500/20 transition-all resize-none"
                  placeholder="Tell us about your creative vision..."
                />
              </div>
              <motion.button
                type="submit"
                className="w-full py-3.5 text-sm font-medium text-white bg-gradient-to-r from-violet-600 to-pink-600 rounded-xl hover:from-violet-500 hover:to-pink-500 transition-all duration-300 hover:shadow-glow-violet"
                whileHover={{ scale: 1.01 }}
                whileTap={{ scale: 0.99 }}
              >
                Send Message
              </motion.button>
            </form>
          </motion.div>

          {/* Contact Info Cards */}
          <motion.div
            className="space-y-4"
            variants={stagger}
            initial="hidden"
            animate="visible"
          >
            {contactCards.map((card) => (
              <motion.div
                key={card.title}
                variants={fadeUp}
                className="group p-6 rounded-2xl bg-white/[0.03] border border-white/[0.06] hover:bg-white/[0.05] hover:border-white/[0.08] transition-all duration-300"
              >
                <h3 className="text-lg font-bold text-noizy-white mb-2">{card.title}</h3>
                <p className="text-sm text-noizy-silver leading-relaxed">
                  {card.description}
                </p>
                <div className="mt-3 flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full" style={{ backgroundColor: card.color }} />
                  <span className="text-sm font-mono" style={{ color: card.color }}>
                    {card.email}
                  </span>
                </div>
              </motion.div>
            ))}

            {/* Location card */}
            <motion.div
              variants={fadeUp}
              className="p-6 rounded-2xl bg-white/[0.03] border border-white/[0.06]"
            >
              <h3 className="text-lg font-bold text-noizy-white mb-2">Based In</h3>
              <p className="text-sm text-noizy-silver leading-relaxed">
                Canada — serving artists and creators worldwide.
                The M2 Ultra never sleeps.
              </p>
              <span className="inline-block mt-3 text-sm text-amber-400 font-mono">
                🇨🇦 Canadian Innovation
              </span>
            </motion.div>
          </motion.div>
        </div>
      </div>
    </div>
  )
}
