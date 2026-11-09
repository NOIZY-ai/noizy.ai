'use client'

import { motion } from 'framer-motion'
import { agents } from '@/config/agents'
import { SectionHeading } from '@/components/ui/SectionHeading'
import { GradientOrb } from '@/components/ui/GradientOrb'
import { cn } from '@/lib/utils'

const containerVariants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.1 } },
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

export function AgentsShowcase() {
  return (
    <section className="relative py-32 overflow-hidden" id="agents">
      <GradientOrb color="violet" size="lg" className="top-0 right-0 opacity-30" />

      <div className="relative z-10 mx-auto max-w-7xl px-6">
        <SectionHeading
          badge="AI Agents"
          title="Five Minds,"
          titleHighlight="One Vision"
          description="Each agent brings a unique creative perspective. Together, they form an unprecedented collaboration engine that amplifies your artistic voice."
        />

        <motion.div
          className="mt-16 grid md:grid-cols-2 lg:grid-cols-3 gap-6"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.1 }}
        >
          {agents.map((agent) => (
            <motion.div
              key={agent.id}
              variants={cardVariants}
              className="group relative p-6 rounded-2xl glass hover:glass-heavy transition-all duration-500 hover:scale-[1.02]"
            >
              {/* Gradient accent top */}
              <div className={cn('absolute top-0 left-6 right-6 h-px bg-gradient-to-r', agent.gradient, 'opacity-50')} />

              <div className="flex items-start gap-4 mb-4">
                <div className={cn('w-12 h-12 rounded-xl bg-gradient-to-br flex items-center justify-center text-2xl shrink-0', agent.gradient)}>
                  {agent.icon}
                </div>
                <div>
                  <h3 className="text-lg font-bold text-noizy-white group-hover:text-gradient-noizy transition-all">
                    {agent.name}
                  </h3>
                  <p className="text-xs font-mono uppercase tracking-wider text-noizy-silver">
                    {agent.role}
                  </p>
                </div>
              </div>

              <p className="text-sm text-noizy-silver leading-relaxed mb-4">
                {agent.description}
              </p>

              <div className="flex flex-wrap gap-1.5">
                {agent.capabilities.map((cap) => (
                  <span
                    key={cap}
                    className="px-2.5 py-1 text-[10px] font-mono uppercase tracking-wider text-noizy-silver bg-white/[0.04] rounded-md border border-white/[0.06]"
                  >
                    {cap}
                  </span>
                ))}
              </div>

              <div className="text-xs text-noizy-silver/40 font-mono mt-4 uppercase tracking-wider">
                {agent.personality}
              </div>
            </motion.div>
          ))}

          {/* CTA card */}
          <motion.div
            variants={cardVariants}
            className="relative p-6 rounded-2xl border border-dashed border-white/10 flex flex-col items-center justify-center text-center min-h-[280px]"
          >
            <div className="text-4xl mb-4">🚀</div>
            <h3 className="text-lg font-bold text-noizy-white mb-2">
              Your Agent, Your Rules
            </h3>
            <p className="text-sm text-noizy-silver mb-4">
              Enterprise plans include custom agent training tailored to your creative workflow.
            </p>
            <span className="px-4 py-2 text-xs font-mono uppercase tracking-wider text-violet-400 bg-violet-500/10 border border-violet-500/20 rounded-full">
              Coming Soon
            </span>
          </motion.div>
        </motion.div>
      </div>
    </section>
  )
}
