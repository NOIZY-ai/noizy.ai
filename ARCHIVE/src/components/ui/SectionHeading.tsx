'use client'

import { cn } from '@/lib/utils'
import { useInView } from '@/hooks/useInView'

interface SectionHeadingProps {
  badge?: string
  title: string
  titleHighlight?: string
  description?: string
  className?: string
  align?: 'left' | 'center'
}

export function SectionHeading({
  badge,
  title,
  titleHighlight,
  description,
  className,
  align = 'center',
}: SectionHeadingProps) {
  const { ref, isInView } = useInView()

  return (
    <div
      ref={ref}
      className={cn(
        'max-w-3xl',
        align === 'center' && 'mx-auto text-center',
        className
      )}
    >
      {badge && (
        <span
          className={cn(
            'inline-block px-4 py-1.5 text-xs font-mono uppercase tracking-[0.2em] text-violet-400 bg-violet-500/10 border border-violet-500/20 rounded-full mb-6 transition-all duration-700',
            isInView ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
          )}
        >
          {badge}
        </span>
      )}
      <h2
        className={cn(
          'text-3xl sm:text-4xl lg:text-5xl font-bold text-noizy-white leading-tight transition-all duration-700 delay-100',
          isInView ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
        )}
      >
        {title}
        {titleHighlight && (
          <span className="text-gradient-noizy"> {titleHighlight}</span>
        )}
      </h2>
      {description && (
        <p
          className={cn(
            'mt-6 text-lg text-noizy-silver leading-relaxed transition-all duration-700 delay-200',
            isInView ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
          )}
        >
          {description}
        </p>
      )}
    </div>
  )
}
