import { siteConfig } from '@/config/site'

export function JsonLd() {
  const structuredData = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: 'NOIZY.AI',
    url: siteConfig.url,
    logo: `${siteConfig.url}/icons/icon-512.png`,
    description: siteConfig.description,
    founder: {
      '@type': 'Person',
      name: siteConfig.creator,
      nationality: 'Canadian',
    },
    brand: [
      {
        '@type': 'Brand',
        name: 'HEAVEN',
        description: 'The Creative Sanctuary — where human intuition meets machine intelligence.',
        url: `${siteConfig.url}/heaven`,
      },
      {
        '@type': 'Brand',
        name: 'NOIZYLAB',
        description: 'The Experimental Forge — where five AI agents are trained, refined, and unleashed.',
        url: `${siteConfig.url}/noizylab`,
      },
      {
        '@type': 'Brand',
        name: 'ANTHROPIC NOIZE',
        description: 'The Movement — the philosophy that AI amplifies rather than replaces human creativity.',
        url: `${siteConfig.url}/anthropic-noize`,
      },
      {
        '@type': 'Brand',
        name: 'DREAM ENGINE',
        description: 'The Production Suite — AI-assisted mastering, mixing, and multi-platform distribution.',
        url: `${siteConfig.url}/dream-engine`,
      },
    ],
    sameAs: [],
    knowsAbout: [
      'Artificial Intelligence',
      'Creative Technology',
      'Music Production',
      'AI-Human Collaboration',
    ],
    offers: {
      '@type': 'AggregateOffer',
      lowPrice: '0',
      highPrice: '449',
      priceCurrency: 'CAD',
      offerCount: 3,
    },
  }

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
    />
  )
}
