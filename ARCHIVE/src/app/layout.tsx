import type { Metadata, Viewport } from 'next'
import { siteConfig } from '@/config/site'
import { Header } from '@/components/layout/Header'
import { Footer } from '@/components/layout/Footer'
import { ClientShell } from '@/components/layout/ClientShell'
import { JsonLd } from '@/components/ui/JsonLd'
import './globals.css'

export const metadata: Metadata = {
  metadataBase: new URL(siteConfig.url),
  title: {
    default: `${siteConfig.name} | HEAVEN + NOIZYLAB + ANTHROPIC NOIZE + DREAM ENGINE`,
    template: `%s | ${siteConfig.name}`,
  },
  description: siteConfig.description,
  keywords: [
    'AI creative collaboration',
    'AI music production',
    'creative AI agents',
    'NOIZY',
    'HEAVEN',
    'NOIZYLAB',
    'ANTHROPIC NOIZE',
    'DREAM ENGINE',
    'AI art platform',
    'creative technology',
    'Robert Stephen Plowman',
    'Anthropic Noize',
    'TALESPIN',
    'voice performance',
    'AI creative hub',
  ],
  authors: [{ name: siteConfig.creator }],
  creator: siteConfig.creator,
  openGraph: {
    type: 'website',
    locale: 'en_CA',
    url: siteConfig.url,
    title: siteConfig.name,
    description: siteConfig.description,
    siteName: siteConfig.name,
  },
  twitter: {
    card: 'summary_large_image',
    title: siteConfig.name,
    description: siteConfig.description,
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
}

export const viewport: Viewport = {
  themeColor: '#0A0A0B',
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/favicon.ico" sizes="any" />
        <link rel="manifest" href="/manifest.json" />
        <JsonLd />
      </head>
      <body className="font-sans antialiased bg-noizy-black text-noizy-light min-h-screen">
        <div className="relative flex min-h-screen flex-col">
          <Header />
          <ClientShell />
          <main className="flex-1">{children}</main>
          <Footer />
        </div>
      </body>
    </html>
  )
}
