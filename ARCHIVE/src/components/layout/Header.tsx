'use client'

import { useState, useEffect, useRef } from 'react'
import Link from 'next/link'
import { motion, AnimatePresence } from 'framer-motion'
import { navigation } from '@/config/navigation'
import { NOIZYLogo } from '@/components/ui/NOIZYLogo'
import { cn } from '@/lib/utils'

export function Header() {
  const [scrolled, setScrolled] = useState(false)
  const [mobileOpen, setMobileOpen] = useState(false)
  const [brandsOpen, setBrandsOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20)
    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setBrandsOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  return (
    <header
      className={cn(
        'fixed top-0 left-0 right-0 z-50 transition-all duration-500',
        scrolled
          ? 'bg-noizy-black/80 backdrop-blur-2xl border-b border-white/[0.06] py-3'
          : 'bg-transparent py-6'
      )}
    >
      <div className="mx-auto max-w-7xl px-6 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-3 group">
          <NOIZYLogo size={40} />
          <div className="flex flex-col">
            <span className="text-lg font-bold tracking-tight text-noizy-white">
              NOIZY<span className="text-violet-400">.AI</span>
            </span>
            <span className="text-[10px] uppercase tracking-[0.2em] text-noizy-silver -mt-0.5">
              Creative Hub
            </span>
          </div>
        </Link>

        {/* Desktop nav */}
        <nav className="hidden md:flex items-center gap-1">
          {navigation.map((item) =>
            item.children ? (
              <div key={item.href} className="relative" ref={dropdownRef}>
                <button
                  onClick={() => setBrandsOpen(!brandsOpen)}
                  className="flex items-center gap-1 px-4 py-2 text-sm text-noizy-silver hover:text-noizy-white transition-colors duration-300 rounded-lg hover:bg-white/[0.04]"
                >
                  {item.label}
                  <svg
                    className={cn('w-3.5 h-3.5 transition-transform duration-300', brandsOpen && 'rotate-180')}
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={2}
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                <AnimatePresence>
                  {brandsOpen && (
                    <motion.div
                      initial={{ opacity: 0, y: -8, scale: 0.95 }}
                      animate={{ opacity: 1, y: 0, scale: 1 }}
                      exit={{ opacity: 0, y: -8, scale: 0.95 }}
                      transition={{ duration: 0.2 }}
                      className="absolute top-full left-0 mt-2 w-56 p-2 rounded-2xl bg-noizy-dark/95 backdrop-blur-2xl border border-white/[0.08] shadow-enterprise"
                    >
                      {item.children.map((child) => (
                        <Link
                          key={child.href}
                          href={child.href}
                          onClick={() => setBrandsOpen(false)}
                          className="block px-4 py-2.5 text-sm text-noizy-silver hover:text-noizy-white hover:bg-white/[0.06] rounded-xl transition-all duration-200"
                        >
                          {child.label}
                        </Link>
                      ))}
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            ) : (
              <Link
                key={item.href}
                href={item.href}
                className="px-4 py-2 text-sm text-noizy-silver hover:text-noizy-white transition-colors duration-300 rounded-lg hover:bg-white/[0.04]"
              >
                {item.label}
              </Link>
            )
          )}
          <div className="ml-4 flex items-center gap-3">
            <Link
              href="/pricing"
              className="px-5 py-2.5 text-sm font-medium text-noizy-white bg-gradient-to-r from-violet-600 to-pink-600 rounded-xl hover:from-violet-500 hover:to-pink-500 transition-all duration-300 hover:shadow-glow-violet"
            >
              Get Started
            </Link>
          </div>
        </nav>

        {/* Mobile hamburger */}
        <button
          onClick={() => setMobileOpen(!mobileOpen)}
          className="md:hidden relative w-10 h-10 flex items-center justify-center"
          aria-label="Toggle menu"
        >
          <div className="flex flex-col gap-1.5">
            <span className={cn('w-6 h-0.5 bg-noizy-light transition-all duration-300', mobileOpen && 'rotate-45 translate-y-2')} />
            <span className={cn('w-6 h-0.5 bg-noizy-light transition-all duration-300', mobileOpen && 'opacity-0')} />
            <span className={cn('w-6 h-0.5 bg-noizy-light transition-all duration-300', mobileOpen && '-rotate-45 -translate-y-2')} />
          </div>
        </button>
      </div>

      {/* Mobile menu */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
            className="md:hidden overflow-hidden bg-noizy-black/95 backdrop-blur-2xl border-b border-white/[0.06]"
          >
            <nav className="flex flex-col p-6 gap-2">
              {navigation.map((item) =>
                item.children ? (
                  <div key={item.href}>
                    <div className="px-4 py-2 text-xs font-mono uppercase tracking-[0.2em] text-noizy-silver/50">
                      {item.label}
                    </div>
                    {item.children.map((child) => (
                      <Link
                        key={child.href}
                        href={child.href}
                        onClick={() => setMobileOpen(false)}
                        className="block px-6 py-2.5 text-base text-noizy-silver hover:text-noizy-white transition-colors rounded-xl hover:bg-white/[0.04]"
                      >
                        {child.label}
                      </Link>
                    ))}
                  </div>
                ) : (
                  <Link
                    key={item.href}
                    href={item.href}
                    onClick={() => setMobileOpen(false)}
                    className="px-4 py-3 text-lg text-noizy-silver hover:text-noizy-white transition-colors rounded-xl hover:bg-white/[0.04]"
                  >
                    {item.label}
                  </Link>
                )
              )}
              <Link
                href="/pricing"
                onClick={() => setMobileOpen(false)}
                className="mt-4 px-5 py-3 text-center font-medium text-noizy-white bg-gradient-to-r from-violet-600 to-pink-600 rounded-xl"
              >
                Get Started
              </Link>
            </nav>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  )
}
