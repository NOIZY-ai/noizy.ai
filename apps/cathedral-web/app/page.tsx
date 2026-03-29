export default function CathedralPage() {
  return (
    <main>
      {/* ═══ HERO ═══ */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
        <div className="absolute inset-0 bg-gradient-radial from-cathedral-amber/5 via-transparent to-transparent animate-pulse-slow" />
        <div className="relative z-10 text-center px-8 max-w-4xl">
          <h1 className="font-display text-6xl md:text-8xl font-bold text-cathedral-amber mb-6">
            THE CATHEDRAL
          </h1>
          <p className="font-ui text-xl md:text-2xl text-cathedral-cyan mb-4">
            Creator Protection at Scale
          </p>
          <p className="font-ui text-lg text-cathedral-muted mb-12">
            The 5th Epoch Begins Now
          </p>
          <div className="flex gap-6 justify-center">
            <a href="#ecosystem" className="px-8 py-3 bg-cathedral-amber text-cathedral-black font-ui font-semibold rounded-lg hover:shadow-[0_0_20px_rgba(255,159,28,0.4)] transition-all">
              Enter the Cathedral
            </a>
            <a href="#economics" className="px-8 py-3 border border-cathedral-cyan text-cathedral-cyan font-ui rounded-lg hover:shadow-[0_0_20px_rgba(0,229,255,0.3)] transition-all">
              See the Deal
            </a>
          </div>
        </div>
      </section>

      {/* ═══ SIGNAL VS NOISE ═══ */}
      <section className="py-32 px-8 max-w-6xl mx-auto">
        <div className="grid md:grid-cols-2 gap-16">
          <div className="opacity-60">
            <h3 className="font-display text-2xl text-cathedral-muted mb-4">The Noise</h3>
            <p className="font-ui text-cathedral-muted leading-relaxed">
              An industry that eats its young. That harvests voices like crops. That turns human genius into training data and calls it progress. That strips the name off the song, the face off the performance, the soul off the creation — and sells the husk back as content.
            </p>
          </div>
          <div>
            <h3 className="font-display text-2xl text-cathedral-amber mb-4">The Signal</h3>
            <p className="font-ui text-cathedral-white leading-relaxed">
              NOIZY doesn't reform that system. NOIZY replaces it. We are infrastructure. The pipes. The foundation. The cathedral floor upon which every creator stands sovereign.
            </p>
          </div>
        </div>
      </section>

      {/* ═══ THE PLOWMAN STANDARD ═══ */}
      <section id="economics" className="py-32 flex items-center justify-center">
        <div className="text-center">
          <p className="font-display text-7xl md:text-9xl font-bold text-cathedral-amber animate-pulse-slow">
            75 / 25
          </p>
          <p className="font-ui text-xl text-cathedral-cyan mt-6">
            In perpetuity. Forever.
          </p>
          <p className="font-ui text-sm text-cathedral-muted mt-4">
            The Plowman Standard
          </p>
        </div>
      </section>

      {/* ═══ ECOSYSTEM GRID ═══ */}
      <section id="ecosystem" className="py-32 px-8 max-w-6xl mx-auto">
        <h2 className="font-display text-4xl text-cathedral-amber text-center mb-16">The Empire</h2>
        <div className="grid md:grid-cols-3 gap-8">
          {[
            { name: 'NOIZY.AI', desc: 'Intelligence layer. Consent infrastructure. DreamChamber.', color: 'border-cathedral-amber' },
            { name: 'NOIZYVOX', desc: 'Performance-grade AI Voice Talent Agency. Characters, not voices.', color: 'border-cathedral-cyan' },
            { name: 'NOIZYFISH', desc: 'Fish Music Inc. 888 titles. 34TB archive. 40 years of craft.', color: 'border-cathedral-amber' },
            { name: 'NOIZYLAB', desc: 'Innovation. Tools. Repair. Experimental pipelines.', color: 'border-cathedral-cyan' },
            { name: 'NOIZYKIDZ', desc: 'Music education. Accessibility. Haptics. The future.', color: 'border-cathedral-amber' },
            { name: 'LIFELUV', desc: 'Peace, love, understanding. The human connection layer.', color: 'border-cathedral-cyan' },
          ].map((brand) => (
            <div key={brand.name} className={`bg-cathedral-card border-l-4 ${brand.color} p-8 rounded-lg hover:shadow-lg hover:translate-y-[-2px] transition-all duration-300`}>
              <h3 className="font-display text-xl font-bold text-cathedral-white mb-3">{brand.name}</h3>
              <p className="font-ui text-sm text-cathedral-muted">{brand.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ═══ DREAMCHAMBER ═══ */}
      <section className="py-32 px-8 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-cathedral-cyan/5 to-transparent" />
        <div className="relative z-10 max-w-4xl mx-auto text-center">
          <h2 className="font-display text-4xl text-cathedral-cyan mb-8">The DreamChamber</h2>
          <p className="font-ui text-lg text-cathedral-white mb-4">
            You don't use the DreamChamber. You enter it.
          </p>
          <p className="font-ui text-cathedral-muted mb-16">
            And when you leave, what you created belongs to you. Forever. Automatically. By design.
          </p>
          <div className="grid md:grid-cols-5 gap-4 text-center">
            {['Enter', 'Create', 'Capture', 'Prove', 'Earn'].map((step, i) => (
              <div key={step} className="flex flex-col items-center">
                <div className="w-12 h-12 rounded-full border-2 border-cathedral-cyan flex items-center justify-center text-cathedral-cyan font-ui font-bold mb-3">
                  {i + 1}
                </div>
                <span className="font-ui text-sm text-cathedral-white">{step}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ═══ GABRIEL ═══ */}
      <section className="py-32 px-8 max-w-3xl mx-auto">
        <div className="bg-cathedral-card border border-cathedral-amber/20 rounded-xl p-12">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-3 h-3 rounded-full bg-cathedral-amber animate-glow" />
            <span className="font-ui text-sm text-cathedral-amber">GABRIEL</span>
          </div>
          <p className="font-display text-2xl text-cathedral-white leading-relaxed">
            "Trust isn't promised. It's proven. Every time. Every use. Every creator."
          </p>
          <p className="font-ui text-sm text-cathedral-muted mt-6">
            The conscience of the system. The protector of every artist inside it.
          </p>
        </div>
      </section>

      {/* ═══ ECONOMICS DETAIL ═══ */}
      <section className="py-32 px-8 max-w-6xl mx-auto">
        <h2 className="font-display text-4xl text-cathedral-amber text-center mb-16">The Economics</h2>
        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-cathedral-card p-8 rounded-lg text-center">
            <p className="font-display text-3xl text-cathedral-amber mb-2">75%</p>
            <p className="font-ui text-cathedral-white mb-1">To the Creator</p>
            <p className="font-ui text-sm text-cathedral-muted">Always. Perpetual. Non-negotiable.</p>
          </div>
          <div className="bg-cathedral-card p-8 rounded-lg text-center">
            <p className="font-display text-3xl text-cathedral-cyan mb-2">Forever</p>
            <p className="font-ui text-cathedral-white mb-1">Voice Estate</p>
            <p className="font-ui text-sm text-cathedral-muted">Earns while you sleep. Passes to your family.</p>
          </div>
          <div className="bg-cathedral-card p-8 rounded-lg text-center">
            <p className="font-display text-3xl text-cathedral-amber mb-2">$0</p>
            <p className="font-ui text-cathedral-white mb-1">To Say No</p>
            <p className="font-ui text-sm text-cathedral-muted">Kill switch. Unconditional. Artist pays nothing.</p>
          </div>
        </div>
      </section>

      {/* ═══ THE EPOCHS ═══ */}
      <section className="py-32 px-8 max-w-4xl mx-auto">
        <div className="space-y-6">
          {[
            { epoch: 'I', era: 'Sheet Music', year: '1400s', who: 'Publishers profited', dim: true },
            { epoch: 'II', era: 'Recording', year: '1920s', who: 'Labels profited', dim: true },
            { epoch: 'III', era: 'Digital', year: '2000s', who: 'Platforms profited', dim: true },
            { epoch: 'IV', era: 'Streaming', year: '2010s', who: 'Extractors profited', dim: true },
            { epoch: 'V', era: 'NOIZY', year: '2026', who: 'CREATORS PROFIT.', dim: false },
          ].map((e) => (
            <div key={e.epoch} className={`flex items-center gap-6 ${e.dim ? 'opacity-40' : ''}`}>
              <span className={`font-display text-2xl w-12 ${e.dim ? 'text-cathedral-muted' : 'text-cathedral-amber'}`}>{e.epoch}</span>
              <span className={`font-ui flex-1 ${e.dim ? 'text-cathedral-muted' : 'text-cathedral-white text-xl font-semibold'}`}>{e.era} ({e.year})</span>
              <span className={`font-ui text-sm ${e.dim ? 'text-cathedral-muted' : 'text-cathedral-amber font-bold'}`}>{e.who}</span>
            </div>
          ))}
        </div>
        <p className="font-ui text-sm text-cathedral-muted text-center mt-12">
          Finally. Forever. By design.
        </p>
      </section>

      {/* ═══ BATTLE CRY ═══ */}
      <section className="py-32 px-8 max-w-3xl mx-auto text-center">
        <div className="space-y-4 mb-16">
          <p className="font-ui text-lg text-cathedral-muted">You were told your voice doesn't matter. <span className="text-cathedral-white font-semibold">It does.</span></p>
          <p className="font-ui text-lg text-cathedral-muted">You were told your art isn't worth anything. <span className="text-cathedral-white font-semibold">It's worth everything.</span></p>
          <p className="font-ui text-lg text-cathedral-muted">You were told AI will replace you. <span className="text-cathedral-white font-semibold">Not here. Not ever.</span></p>
        </div>
        <p className="font-display text-6xl md:text-8xl font-bold text-cathedral-amber animate-pulse-slow">
          GORUNFREE
        </p>
        <div className="mt-12 space-y-2">
          <p className="font-ui text-cathedral-cyan">noizy.ai</p>
          <p className="font-ui text-sm text-cathedral-muted">The 5th Epoch Begins Now</p>
        </div>
      </section>

      {/* ═══ FINAL SILENCE ═══ */}
      <section className="h-32 bg-cathedral-black" />
    </main>
  )
}
