'use client'

import { motion } from 'framer-motion'
import { platforms } from '@/config/navigation'
import { SectionHeading } from '@/components/ui/SectionHeading'
import { cn } from '@/lib/utils'

const platformIcons: Record<string, string> = {
  macos: '🍎',
  windows: '🪟',
  linux: '🐧',
  ios: '📱',
  android: '🤖',
}

const containerVariants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.08 } },
}

const itemVariants = {
  hidden: { opacity: 0, y: 20, scale: 0.95 },
  visible: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: { duration: 0.5 },
  },
}

export function Platforms() {
  return (
    <section className="relative py-32 overflow-hidden" id="platforms">
      <div className="relative z-10 mx-auto max-w-7xl px-6">
        <SectionHeading
          badge="Cross-Platform"
          title="Create Anywhere,"
          titleHighlight="Everywhere"
          description="Your creative studio travels with you. NOIZY.AI runs natively on every major platform with seamless cross-device synchronization."
        />

        <motion.div
          className="mt-16 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4 max-w-3xl mx-auto"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.2 }}
        >
          {platforms.map((platform) => (
            <motion.div
              key={platform.name}
              variants={itemVariants}
              className="group p-6 rounded-2xl glass hover:glass-heavy text-center transition-all duration-500 hover:scale-105"
            >
              <div className="text-4xl mb-3">{platformIcons[platform.icon]}</div>
              <div className="text-sm font-medium text-noizy-white">{platform.name}</div>
              <div className="mt-1 flex items-center justify-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-green-400" />
                <span className="text-[10px] text-green-400 font-mono uppercase">
                  Available
                </span>
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* Feature highlights */}
        <motion.div
          className="mt-16 grid md:grid-cols-3 gap-6 max-w-4xl mx-auto"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
        >
          {[
            {
              title: 'Real-time Sync',
              description: 'Start on your Mac, continue on your iPhone, finish on your PC. Your creative state syncs instantly.',
            },
            {
              title: 'Native Performance',
              description: 'Built with platform-native technologies for the fastest, most responsive creative experience.',
            },
            {
              title: 'Offline Capable',
              description: 'Keep creating even without internet. Your work syncs automatically when you reconnect.',
            },
          ].map((feature) => (
            <motion.div
              key={feature.title}
              variants={itemVariants}
              className="text-center p-6"
            >
              <h3 className="text-base font-bold text-noizy-white mb-2">{feature.title}</h3>
              <p className="text-sm text-noizy-silver leading-relaxed">{feature.description}</p>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  )
}
