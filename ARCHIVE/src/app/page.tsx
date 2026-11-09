'use client'

import { Hero } from '@/components/sections/Hero'
import { BrandShowcase } from '@/components/sections/BrandShowcase'
import { AgentsShowcase } from '@/components/sections/AgentsShowcase'
import { Mission } from '@/components/sections/Mission'
import { Pricing } from '@/components/sections/Pricing'
import { Platforms } from '@/components/sections/Platforms'
import { CTA } from '@/components/sections/CTA'
import { ParticleField } from '@/components/ui/ParticleField'

export default function Home() {
  return (
    <>
      <ParticleField />
      <Hero />
      <BrandShowcase />
      <AgentsShowcase />
      <Mission />
      <Pricing />
      <Platforms />
      <CTA />
    </>
  )
}
