'use client'

import { cn } from '@/lib/utils'

interface GradientOrbProps {
  className?: string
  color?: 'violet' | 'pink' | 'blue' | 'amber'
  size?: 'sm' | 'md' | 'lg' | 'xl'
}

const colorMap = {
  violet: 'bg-violet-500/20',
  pink: 'bg-pink-500/20',
  blue: 'bg-blue-500/20',
  amber: 'bg-amber-500/20',
}

const sizeMap = {
  sm: 'w-[200px] h-[200px]',
  md: 'w-[400px] h-[400px]',
  lg: 'w-[600px] h-[600px]',
  xl: 'w-[800px] h-[800px]',
}

export function GradientOrb({ className, color = 'violet', size = 'lg' }: GradientOrbProps) {
  return (
    <div
      className={cn(
        'absolute rounded-full blur-[120px] pointer-events-none animate-pulse-glow',
        colorMap[color],
        sizeMap[size],
        className
      )}
      aria-hidden="true"
    />
  )
}
