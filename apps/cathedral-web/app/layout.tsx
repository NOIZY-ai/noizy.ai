import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'NOIZY.AI — Creator Protection at Scale',
  description: 'The first performance-grade AI Voice Talent Agency. 75% Creator. 25% Platform. Forever. The 5th Epoch begins now.',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="font-ui antialiased">{children}</body>
    </html>
  )
}
