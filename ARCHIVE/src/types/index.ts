export interface Agent {
  id: string
  name: string
  role: string
  description: string
  personality: string
  gradient: string
  icon: string
  capabilities: string[]
}

export interface Brand {
  id: string
  name: string
  tagline: string
  description: string
  gradient: string
  accentColor: string
  icon: string
  href: string
  status: 'live' | 'coming-soon' | 'in-development'
  features: string[]
}

export interface PricingTier {
  name: string
  price: number
  currency: string
  interval: string
  features: string[]
  highlighted: boolean
  cta: string
}

export interface Platform {
  name: string
  icon: string
  available: boolean
  downloadUrl?: string
}

export interface NavItem {
  label: string
  href: string
  external?: boolean
  children?: NavItem[]
}

export interface SiteConfig {
  name: string
  description: string
  url: string
  ogImage: string
  creator: string
  brand: {
    primary: string
    secondary: string
  }
}
