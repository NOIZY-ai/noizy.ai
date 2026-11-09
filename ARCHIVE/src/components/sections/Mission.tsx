'use client'

import { motion } from 'framer-motion'
import { SectionHeading } from '@/components/ui/SectionHeading'
import { GradientOrb } from '@/components/ui/GradientOrb'
import { cn } from '@/lib/utils'

const pillars = [
  {
    title: 'Collaboration Over Isolation',
    description: 'Just as Lennon needed McCartney and Richards complemented Jagger, artists flourish when challenged and inspired by dynamic partnerships. AI is your creative counterpart.',
    icon: '01',
    gradient: 'from-violet-500 to-purple-600',
  },
  {
    title: 'Amplify, Never Replace',
    description: 'We wield AI not as a crutch but as a tool to amplify and nurture unique creative talents. The era of soulless, greed-driven creations masquerading mediocrity as gold is over.',
    icon: '02',
    gradient: 'from-pink-500 to-rose-600',
  },
  {
    title: 'Tradition Meets Innovation',
    description: 'Fusing traditional methods with cutting-edge approaches, constantly seeking the most effective paths. This fusion is the new norm, resonating with creators everywhere.',
    icon: '03',
    gradient: 'from-amber-500 to-orange-600',
  },
  {
    title: 'Reclaim Creative Authority',
    description: 'In a world gripped by fear of AI, we empower artists to reclaim their creative authority. Technology meets authentic human creativity, and the world of art is forever transformed.',
    icon: '04',
    gradient: 'from-cyan-500 to-blue-600',
  },
]

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

export function Mission() {
  return (
    <section className="relative py-32 overflow-hidden" id="mission">
      <GradientOrb color="pink" size="lg" className="top-1/4 -left-40 opacity-20" />
      <GradientOrb color="amber" size="md" className="bottom-0 right-0 opacity-20" />

      <div className="relative z-10 mx-auto max-w-7xl px-6">
        <SectionHeading
          badge="Our Mission"
          title="The Anthropic Noize"
          titleHighlight="Movement"
          description="It began the moment artists decided to wield AI not as a replacement but as an instrument to elevate their craft — a pivotal juncture where technology met authentic human creativity."
        />

        <motion.div
          className="mt-16 grid md:grid-cols-2 gap-6"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.1 }}
        >
          {pillars.map((pillar) => (
            <motion.div
              key={pillar.title}
              variants={cardVariants}
              className="group p-8 rounded-2xl glass hover:glass-heavy transition-all duration-500"
            >
              <div className="flex items-start gap-4 mb-4">
                <div className={cn(
                  'w-12 h-12 rounded-xl bg-gradient-to-br flex items-center justify-center text-white text-sm font-bold font-mono shrink-0',
                  pillar.gradient
                )}>
                  {pillar.icon}
                </div>
                <h3 className="text-xl font-bold text-noizy-white group-hover:text-gradient-noizy transition-all pt-2.5">
                  {pillar.title}
                </h3>
              </div>
              <p className="text-noizy-silver leading-relaxed pl-16">
                {pillar.description}
              </p>
            </motion.div>
          ))}
        </motion.div>

        {/* Quote */}
        <motion.div
          className="mt-16 p-10 rounded-3xl glass text-center max-w-4xl mx-auto"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: 0.3 }}
        >
          <blockquote className="text-xl sm:text-2xl font-medium text-noizy-white leading-relaxed italic">
            &ldquo;Creativity thrives not in isolation but in collaboration. Nothing compares
            to the electric synergy of interacting with a counterpart who pushes you
            to uncover your most brilliant ideas.&rdquo;
          </blockquote>
          <cite className="mt-6 block text-sm text-noizy-silver not-italic font-mono uppercase tracking-wider">
            — The NOIZY Manifesto
          </cite>
        </motion.div>
      </div>
    </section>
  )
}
