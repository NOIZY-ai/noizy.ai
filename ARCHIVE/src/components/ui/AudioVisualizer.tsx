'use client'

import { useEffect, useRef } from 'react'

interface AudioVisualizerProps {
  className?: string
  barCount?: number
  color?: string
  height?: number
}

export function AudioVisualizer({
  className = '',
  barCount = 32,
  color = '#8B5CF6',
  height = 60,
}: AudioVisualizerProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    let animationId: number
    const bars: number[] = Array.from({ length: barCount }, () => Math.random() * 0.3)
    const targets: number[] = Array.from({ length: barCount }, () => Math.random() * 0.3)

    const resize = () => {
      const rect = canvas.getBoundingClientRect()
      canvas.width = rect.width * window.devicePixelRatio
      canvas.height = rect.height * window.devicePixelRatio
      ctx.scale(window.devicePixelRatio, window.devicePixelRatio)
    }

    const animate = () => {
      const rect = canvas.getBoundingClientRect()
      const w = rect.width
      const h = rect.height
      ctx.clearRect(0, 0, w, h)

      const barWidth = w / barCount
      const gap = 2

      bars.forEach((bar, i) => {
        // Smoothly approach target
        bars[i] += (targets[i] - bars[i]) * 0.08

        // Randomly shift targets
        if (Math.random() < 0.05) {
          // Create wave-like patterns
          const center = barCount / 2
          const distFromCenter = Math.abs(i - center) / center
          targets[i] = (Math.random() * 0.7 + 0.1) * (1 - distFromCenter * 0.4)
        }

        const barH = bars[i] * h
        const x = i * barWidth + gap / 2
        const bw = barWidth - gap

        // Gradient per bar
        const gradient = ctx.createLinearGradient(0, h, 0, h - barH)
        gradient.addColorStop(0, color + '40')
        gradient.addColorStop(0.5, color + '90')
        gradient.addColorStop(1, color + 'FF')

        ctx.fillStyle = gradient
        ctx.beginPath()
        const radius = Math.min(bw / 2, 3)
        ctx.roundRect(x, h - barH, bw, barH, [radius, radius, 0, 0])
        ctx.fill()

        // Reflection
        const reflectionGrad = ctx.createLinearGradient(0, h, 0, h + barH * 0.3)
        reflectionGrad.addColorStop(0, color + '15')
        reflectionGrad.addColorStop(1, color + '00')
        ctx.fillStyle = reflectionGrad
        ctx.fillRect(x, h, bw, barH * 0.3)
      })

      animationId = requestAnimationFrame(animate)
    }

    resize()
    animate()

    window.addEventListener('resize', resize)
    return () => {
      cancelAnimationFrame(animationId)
      window.removeEventListener('resize', resize)
    }
  }, [barCount, color])

  return (
    <canvas
      ref={canvasRef}
      className={className}
      style={{ width: '100%', height }}
      aria-hidden="true"
    />
  )
}
