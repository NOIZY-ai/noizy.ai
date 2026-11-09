import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'NOIZYLAB — The Experimental Forge',
  description: 'The experimental forge where technology and creativity collide. Five AI agents trained, refined, and unleashed to push artists beyond their limits. A NOIZY.AI brand.',
  keywords: ['NOIZYLAB', 'AI agents', 'experimental', 'creative tools', 'NOIZY.AI', 'sound design'],
}

export default function NoizyLabLayout({ children }: { children: React.ReactNode }) {
  return children
}
