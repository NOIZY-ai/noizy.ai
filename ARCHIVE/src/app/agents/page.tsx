'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'
import { agents } from '@/config/agents'
import { AudioVisualizer } from '@/components/ui/AudioVisualizer'
import { cn } from '@/lib/utils'

const agentColors: Record<string, string> = {
  gabriel: '#8B5CF6',
  shirl: '#EC4899',
  pops: '#F59E0B',
  engr_keith: '#06B6D4',
  dream: '#6366F1',
}

const stagger = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.12 } },
}

const fadeUp = {
  hidden: { opacity: 0, y: 40, scale: 0.97 },
  visible: { opacity: 1, y: 0, scale: 1, transition: { duration: 0.7, ease: [0.25, 0.46, 0.45, 0.94] } },
}

export default function AgentsPage() {
  return (
    <div className="relative min-h-screen pt-32 pb-20">
      {/* Background effects */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none" aria-hidden="true">
        <motion.div
          className="absolute -top-40 -left-40 w-[500px] h-[500px] rounded-full bg-violet-500/10 blur-[150px]"
          animate={{ x: [0, 30, -20, 0], y: [0, -20, 30, 0] }}
          transition={{ duration: 20, repeat: Infinity, ease: 'easeInOut' }}
        />
        <motion.div
          className="absolute top-1/2 -right-20 w-[400px] h-[400px] rounded-full bg-pink-500/10 blur-[120px]"
          animate={{ x: [0, -30, 20, 0], y: [0, 20, -30, 0] }}
          transition={{ duration: 18, repeat: Infinity, ease: 'easeInOut' }}
        />
      </div>

      <div className="relative z-10 mx-auto max-w-7xl px-6">
        <motion.span
          className="inline-block px-4 py-1.5 text-xs font-mono uppercase tracking-[0.2em] text-violet-400 bg-violet-500/10 border border-violet-500/20 rounded-full mb-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          The Collective
        </motion.span>

        <motion.h1
          className="text-4xl sm:text-5xl lg:text-6xl font-bold text-noizy-white leading-tight"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.1 }}
        >
          Meet Your Creative{' '}
          <span className="text-gradient-noizy">Partners</span>
        </motion.h1>

        <motion.p
          className="mt-6 text-lg text-noizy-silver max-w-2xl leading-relaxed"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.2 }}
        >
          Five AI agents, each with a distinct creative philosophy. They don&apos;t just
          assist — they challenge, inspire, and push you to discover ideas you never
          knew you had.
        </motion.p>

        {/* Agent detail cards */}
        <motion.div
          className="mt-16 space-y-8"
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.05 }}
        >
          {agents.map((agent, i) => (
            <motion.div
              key={agent.id}
              variants={fadeUp}
              className={cn(
                'group relative rounded-3xl bg-white/[0.02] border border-white/[0.06]',
                'hover:bg-white/[0.04] hover:border-white/[0.1] transition-all duration-700',
                'overflow-hidden'
              )}
            >
              {/* Top gradient line */}
              <div className={cn('absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r opacity-30 group-hover:opacity-60 transition-opacity duration-700', agent.gradient)} />

              <div className="p-8 sm:p-10">
                <div className="flex flex-col lg:flex-row gap-8">
                  <div className="shrink-0">
                    <div className={cn(
                      'w-20 h-20 rounded-2xl bg-gradient-to-br flex items-center justify-center text-4xl',
                      'group-hover:scale-110 group-hover:shadow-lg transition-all duration-500',
                      agent.gradient
                    )}>
                      {agent.icon}
                    </div>
                    <div className="mt-4 text-xs font-mono text-noizy-silver/40 uppercase tracking-wider">
                      Agent #{String(i + 1).padStart(2, '0')}
                    </div>
                    {/* Per-agent audio visualizer */}
                    <div className="mt-3 w-20 opacity-40 group-hover:opacity-70 transition-opacity duration-500">
                      <AudioVisualizer
                        barCount={10}
                        color={agentColors[agent.id] || '#8B5CF6'}
                        height={30}
                      />
                    </div>
                  </div>

                  <div className="flex-1">
                    <div className="flex items-baseline gap-3 flex-wrap">
                      <h2 className="text-3xl font-bold text-noizy-white group-hover:text-gradient-noizy transition-all duration-500">
                        {agent.name}
                      </h2>
                      <span className="text-sm font-mono text-violet-400 uppercase tracking-wider">
                        {agent.role}
                      </span>
                    </div>

                    <p className="mt-4 text-lg text-noizy-silver leading-relaxed max-w-2xl">
                      {agent.description}
                    </p>

                    <div className="mt-6 flex flex-wrap gap-2">
                      {agent.capabilities.map((cap) => (
                        <span
                          key={cap}
                          className="px-4 py-2 text-sm text-noizy-silver bg-white/[0.04] rounded-xl border border-white/[0.06] hover:bg-white/[0.08] hover:border-white/[0.1] transition-all duration-300"
                        >
                          {cap}
                        </span>
                      ))}
                    </div>

                    <div className="mt-6 flex items-center gap-6">
                      <div className="text-sm text-noizy-silver/50 font-mono uppercase tracking-wider">
                        Personality: {agent.personality}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* Synergy section */}
        <motion.div
          className="mt-20 p-10 rounded-3xl bg-white/[0.02] border border-white/[0.06] text-center overflow-hidden relative"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <h2 className="text-3xl font-bold text-noizy-white mb-4">
            The Power of <span className="text-gradient-noizy">Synergy</span>
          </h2>
          <p className="text-lg text-noizy-silver max-w-2xl mx-auto leading-relaxed">
            Each agent is powerful alone, but together they create an unprecedented
            creative collaboration engine. Mix and match agents to find the perfect
            creative partnership for every project.
          </p>

          <div className="mt-8 flex justify-center gap-3">
            {agents.map((agent) => (
              <motion.div
                key={agent.id}
                className={cn('w-14 h-14 rounded-xl bg-gradient-to-br flex items-center justify-center text-2xl', agent.gradient)}
                whileHover={{ scale: 1.15, rotate: 5 }}
                transition={{ type: 'spring', stiffness: 400, damping: 15 }}
              >
                {agent.icon}
              </motion.div>
            ))}
          </div>

          {/* Audio visualizer accent */}
          <div className="mt-8 max-w-sm mx-auto opacity-30">
            <AudioVisualizer barCount={24} color="#8B5CF6" height={30} />
          </div>

          <motion.div className="mt-8">
            <Link
              href="/pricing"
              className="inline-block px-8 py-3.5 text-sm font-medium text-white bg-gradient-to-r from-violet-600 to-pink-600 rounded-xl hover:from-violet-500 hover:to-pink-500 transition-all duration-300 hover:shadow-glow-violet"
            >
              Start Working with Agents
            </Link>
          </motion.div>
        </motion.div>
      </div>
    </div>
  )
}
