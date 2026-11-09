import Link from 'next/link'
import { siteConfig } from '@/config/site'
import { brands } from '@/config/brands'

const footerLinks = {
  brands: brands.map((b) => ({ label: b.name, href: b.href })),
  product: [
    { label: 'Agents', href: '/agents' },
    { label: 'Pricing', href: '/pricing' },
    { label: 'Platforms', href: '/#platforms' },
    { label: 'Changelog', href: '#' },
  ],
  company: [
    { label: 'About', href: '/about' },
    { label: 'Contact', href: '/contact' },
    { label: 'Careers', href: '#' },
    { label: 'Press', href: '#' },
  ],
  legal: [
    { label: 'Privacy Policy', href: '#' },
    { label: 'Terms of Service', href: '#' },
    { label: 'Cookie Policy', href: '#' },
  ],
}

export function Footer() {
  return (
    <footer className="border-t border-white/[0.06] bg-noizy-black">
      <div className="mx-auto max-w-7xl px-6 py-16">
        <div className="grid grid-cols-2 md:grid-cols-6 gap-8 md:gap-12">
          {/* Brand */}
          <div className="col-span-2">
            <Link href="/" className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-500 via-pink-500 to-amber-500 flex items-center justify-center">
                <span className="text-white font-bold text-lg">N</span>
              </div>
              <div className="flex flex-col">
                <span className="text-lg font-bold tracking-tight text-noizy-white">
                  NOIZY<span className="text-violet-400">.AI</span>
                </span>
                <span className="text-[10px] uppercase tracking-[0.2em] text-noizy-silver -mt-0.5">
                  Creative Hub
                </span>
              </div>
            </Link>
            <p className="text-sm text-noizy-silver max-w-xs leading-relaxed">
              The home of four interconnected brands where AI meets authentic human
              creativity. Empowering artists to reclaim their creative authority.
            </p>
            {/* Brand pills */}
            <div className="mt-4 flex flex-wrap gap-2">
              {brands.map((brand) => (
                <Link
                  key={brand.id}
                  href={brand.href}
                  className="px-2.5 py-1 text-[10px] font-mono uppercase tracking-wider text-noizy-silver bg-white/[0.04] rounded-md border border-white/[0.06] hover:text-noizy-white hover:border-white/[0.12] transition-all"
                >
                  {brand.name}
                </Link>
              ))}
            </div>
          </div>

          {/* Brands */}
          <div>
            <h4 className="text-sm font-semibold text-noizy-white mb-4 uppercase tracking-wider">
              Brands
            </h4>
            <ul className="space-y-3">
              {footerLinks.brands.map((link) => (
                <li key={link.label}>
                  <Link href={link.href} className="text-sm text-noizy-silver hover:text-noizy-white transition-colors">
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Product */}
          <div>
            <h4 className="text-sm font-semibold text-noizy-white mb-4 uppercase tracking-wider">
              Product
            </h4>
            <ul className="space-y-3">
              {footerLinks.product.map((link) => (
                <li key={link.label}>
                  <Link href={link.href} className="text-sm text-noizy-silver hover:text-noizy-white transition-colors">
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Company */}
          <div>
            <h4 className="text-sm font-semibold text-noizy-white mb-4 uppercase tracking-wider">
              Company
            </h4>
            <ul className="space-y-3">
              {footerLinks.company.map((link) => (
                <li key={link.label}>
                  <Link href={link.href} className="text-sm text-noizy-silver hover:text-noizy-white transition-colors">
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h4 className="text-sm font-semibold text-noizy-white mb-4 uppercase tracking-wider">
              Legal
            </h4>
            <ul className="space-y-3">
              {footerLinks.legal.map((link) => (
                <li key={link.label}>
                  <Link href={link.href} className="text-sm text-noizy-silver hover:text-noizy-white transition-colors">
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="mt-16 pt-8 border-t border-white/[0.06] flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-xs text-noizy-silver">
            &copy; {new Date().getFullYear()} {siteConfig.name}. All rights reserved.
            A vision by {siteConfig.creator}.
          </p>
          <div className="flex items-center gap-6">
            <span className="text-xs text-noizy-silver/60 font-mono uppercase tracking-wider">
              HEAVEN &middot; NOIZYLAB &middot; ANTHROPIC NOIZE &middot; DREAM ENGINE
            </span>
          </div>
        </div>
      </div>
    </footer>
  )
}
