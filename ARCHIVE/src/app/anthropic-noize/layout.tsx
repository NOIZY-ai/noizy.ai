import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'ANTHROPIC NOIZE — The Movement',
  description: 'More than a brand — a creative revolution. The philosophy that AI amplifies rather than replaces human creativity. The manifesto and community. A NOIZY.AI brand.',
  keywords: ['Anthropic Noize', 'creative movement', 'AI art', 'manifesto', 'NOIZY.AI', 'Robert Stephen Plowman'],
}

export default function AnthropicNoizeLayout({ children }: { children: React.ReactNode }) {
  return children
}
