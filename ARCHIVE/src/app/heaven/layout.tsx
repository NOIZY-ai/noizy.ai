import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'HEAVEN — The Creative Sanctuary',
  description: 'Where human intuition meets machine intelligence. HEAVEN is the sacred creative space where authentic artistry is born, nurtured, and elevated. A NOIZY.AI brand.',
  keywords: ['HEAVEN', 'creative sanctuary', 'AI collaboration', 'NOIZY.AI', 'music production', 'TALESPIN'],
}

export default function HeavenLayout({ children }: { children: React.ReactNode }) {
  return children
}
