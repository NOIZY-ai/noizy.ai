'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'
import { agents } from '@/config/agents'
import { AudioVisualizer } from '@/components/ui/AudioVisualizer'
import { cn } from '@/lib/utils'

const features = [
  {
    title: 'Agent Training & Customization',
    description: 'Train AI agents to understand your unique creative language. NOIZYLAB is the forge where agents evolve to match your artistic vision.',
    icon: '01',
  },
  {
    title: 'Experimental Sound Design',
    description: 'Push sonic boundaries with AI-powered experimental tools. Create sounds that have never existed before.',
    icon: '02',
  },
  {
    title: 'Boundary-Pushing Creative Tools',
    description: 'Tools designed not for comfort but for breakthrough. NOIZYLAB challenges you to go beyond what you thought possible.',
    icon: '03',
  },
  {
    title: 'Real-Time Agent Collaboration',
    description: 'Watch your agents think, iterate, and create in real time. Multi-agent sessions where creative sparks fly.',
    icon: '04',
  },
]

const stagger = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.1 } },
}

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6 } },
}

export default function NoizyLabPage() {
  return (
    <div className="relative min-h-screen pt-32 pb-20">
      {/* Brand-specific gradient background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none" aria-hidden="true">
        <div className="absolute -top-40 right-1/4 w-[600px] h-[600px] rounded-full bg-pink-500/10 blur-[150px]" />
        <div className="absolute top-1/2 -left-20 w-[500px] h-[500px] rounded-full bg-rose-500/10 blur-[120px]" />
      </div>

      <div className="relative z-10 mx-auto max-w-7xl px-6">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="flex items-center gap-4 mb-8">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-pink-500 via-rose-500 to-red-600 flex items-center justify-center text-white font-bold text-xl">
              NL
            </div>
            <span className="px-3 py-1 text-[10px] font-mono uppercase tracking-wider text-green-400 bg-green-500/10 border border-green-500/20 rounded-full">
              LIVE
            </span>
          </div>
        </motion.div>

        <motion.h1
          className="text-5xl sm:text-6xl lg:text-7xl font-bold text-noizy-white leading-[0.9]"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.1 }}
        >
          NOIZYLAB
        </motion.h1>
        <motion.p
          className="mt-2 text-xl font-mono uppercase tracking-[0.15em] bg-clip-text text-transparent bg-gradient-to-r from-pink-400 via-rose-400 to-red-400"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          The Experimental Forge
        </motion.p>

        <motion.p
          className="mt-8 text-lg text-noizy-silver max-w-3xl leading-relaxed"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
        >
          The experimental forge where technology and creativity collide at full velocity.
          NOIZYLAB is where five AI agents are trained, refined, and unleashed — each
          designed to push artists beyond their perceived limitations into uncharted
          creative territory.
        </motion.p>

        {/* Audio visualizer */}
        <motion.div
          className="mt-10 max-w-lg"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1, delay: 0.5 }}
        >
          <AudioVisualizer barCount={36} color="#EC4899" height={55} />
        </motion.div>

        {/* Agents grid */}
        <motion.div
          className="mt-20"
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.1 }}
        >
          <h2 className="text-3xl font-bold text-noizy-white mb-8">
            The <span className="bg-clip-text text-transparent bg-gradient-to-r from-pink-400 to-rose-400">Five Agents</span>
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {agents.map((agent) => (
              <motion.div
                key={agent.id}
                variants={fadeUp}
                className="group p-6 rounded-2xl bg-white/[0.03] border border-white/[0.06] hover:bg-white/[0.05] transition-all duration-500"
              >
                <div className="flex items-center gap-3 mb-3">
                  <div className={cn('w-10 h-10 rounded-xl bg-gradient-to-br flex items-center justify-center text-xl', agent.gradient)}>
                    {agent.icon}
                  </div>
                  <div>
                    <h3 className="font-bold text-noizy-white">{agent.name}</h3>
                    <p className="text-xs font-mono text-noizy-silver uppercase">{agent.role}</p>
                  </div>
                </div>
                <p className="text-sm text-noizy-silver leading-relaxed">{agent.description}</p>
              </motion.div>
            ))}
          </div>
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
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-pink-500 to-rose-600 flex items-center justify-center text-white text-sm font-bold font-mono mb-4">
                {feature.icon}
              </div>
              <h3 className="text-xl font-bold text-noizy-white mb-3">{feature.title}</h3>
              <p className="text-noizy-silver leading-relaxed">{feature.description}</p>
            </motion.div>
          ))}
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
            className="px-8 py-4 text-base font-medium text-white bg-gradient-to-r from-pink-600 to-rose-600 rounded-2xl hover:from-pink-500 hover:to-rose-500 transition-all duration-500 hover:shadow-glow-pink"
          >
            Enter NOIZYLAB
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
