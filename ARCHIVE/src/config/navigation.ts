import type { NavItem, Platform, PricingTier } from '@/types'

export const navigation: NavItem[] = [
  {
    label: 'Brands',
    href: '#brands',
    children: [
      { label: 'HEAVEN', href: '/heaven' },
      { label: 'NOIZYLAB', href: '/noizylab' },
      { label: 'ANTHROPIC NOIZE', href: '/anthropic-noize' },
      { label: 'DREAM ENGINE', href: '/dream-engine' },
    ],
  },
  { label: 'Agents', href: '/agents' },
  { label: 'Pricing', href: '/pricing' },
  { label: 'About', href: '/about' },
  { label: 'Contact', href: '/contact' },
]

export const platforms: Platform[] = [
  { name: 'macOS', icon: 'macos', available: true },
  { name: 'Windows', icon: 'windows', available: true },
  { name: 'Linux', icon: 'linux', available: true },
  { name: 'iOS', icon: 'ios', available: true },
  { name: 'Android', icon: 'android', available: true },
]

export const pricingTiers: PricingTier[] = [
  {
    name: 'Explorer',
    price: 0,
    currency: 'CAD',
    interval: 'forever',
    features: [
      '1 AI Agent access',
      '10 creative sessions/month',
      'Basic collaboration tools',
      'Community support',
      'Standard export formats',
    ],
    highlighted: false,
    cta: 'Start Free',
  },
  {
    name: 'Creator',
    price: 89,
    currency: 'CAD',
    interval: 'month',
    features: [
      'All 5 AI Agents',
      'Unlimited creative sessions',
      'Advanced collaboration suite',
      'Priority support',
      'All export formats',
      'Custom agent personalities',
      'Cross-platform sync',
      'Voice integration',
    ],
    highlighted: true,
    cta: 'Start Creating',
  },
  {
    name: 'Enterprise',
    price: 449,
    currency: 'CAD',
    interval: 'month',
    features: [
      'Everything in Creator',
      'Custom AI Agent training',
      'Dedicated infrastructure',
      'SSO & team management',
      'API access & webhooks',
      'White-label options',
      'SLA guarantee',
      'Dedicated account manager',
      'On-premise deployment option',
    ],
    highlighted: false,
    cta: 'Contact Sales',
  },
]
