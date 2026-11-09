import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'DREAM ENGINE — The Production Suite',
  description: 'The full-spectrum production powerhouse. AI-assisted mastering, mixing, visual production, and multi-platform distribution. Coming soon to NOIZY.AI.',
  keywords: ['Dream Engine', 'production suite', 'AI mastering', 'music production', 'NOIZY.AI', 'distribution'],
}

export default function DreamEngineLayout({ children }: { children: React.ReactNode }) {
  return children
}
