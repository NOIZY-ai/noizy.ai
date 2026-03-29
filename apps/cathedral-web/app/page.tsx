export default function CathedralPage() {
  return (
    <main>
      {/* ═══ HERO ═══ */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
        <div className="absolute inset-0 bg-gradient-radial from-cathedral-amber/5 via-transparent to-transparent animate-pulse-slow" />
        <div className="relative z-10 text-center px-8 max-w-4xl">
          <h1 className="font-display text-6xl md:text-8xl font-bold text-cathedral-amber mb-8">
            TOGETHER, WE RISE.
          </h1>
          <p className="font-ui text-xl md:text-2xl text-cathedral-white mb-2">
            Protect the human signal.
          </p>
          <p className="font-ui text-base text-cathedral-muted mb-16">
            The infrastructure for sovereign human creativity in the age of AI.
          </p>
          <div className="flex gap-6 justify-center">
            <a href="#dreamchamber" className="px-8 py-3 bg-cathedral-amber text-cathedral-black font-ui font-semibold rounded-lg hover:shadow-[0_0_20px_rgba(255,159,28,0.4)] transition-all">
              Enter DreamChamber
            </a>
            <a href="#system" className="px-8 py-3 border border-cathedral-cyan/40 text-cathedral-muted font-ui rounded-lg hover:text-cathedral-cyan hover:border-cathedral-cyan transition-all">
              See the System
            </a>
          </div>
        </div>
      </section>

      {/* ═══ SIGNAL VS NOISE ═══ */}
      <section className="py-32 px-8 max-w-6xl mx-auto">
        <div className="grid md:grid-cols-2 gap-16">
          <div className="opacity-50">
            <h3 className="font-display text-2xl text-cathedral-muted mb-6">The Noise</h3>
            <p className="font-ui text-cathedral-muted leading-relaxed mb-8">
              The world is flooding with synthetic signal.<br />
              Most of it belongs to no one.
            </p>
            <div className="space-y-3 font-ui text-sm text-cathedral-muted">
              <p>No consent.</p>
              <p>No lineage.</p>
              <p>No control.</p>
              <p>No permanence.</p>
            </div>
          </div>
          <div>
            <h3 className="font-display text-2xl text-cathedral-amber mb-6">The Signal</h3>
            <p className="font-ui text-cathedral-white leading-relaxed mb-8">
              We do not answer decline with noise.<br />
              We answer it with infrastructure.
            </p>
            <div className="space-y-3 font-ui text-sm text-cathedral-white">
              <p>One human.</p>
              <p>One voice.</p>
              <p>One identity.</p>
              <p>One estate.</p>
            </div>
          </div>
        </div>
      </section>

      {/* ═══ GOSPEL ═══ */}
      <section className="py-24 px-8 max-w-3xl mx-auto text-center">
        <p className="font-ui text-lg text-cathedral-white leading-relaxed mb-8">
          Artists. Teachers. Mentors. Authors. Composers. Voice professionals.
        </p>
        <p className="font-ui text-base text-cathedral-muted">
          Not users. Not data. Human signal.
        </p>
      </section>

      {/* ═══ THE PLOWMAN STANDARD ═══ */}
      <section id="economics" className="py-32 flex items-center justify-center">
        <div className="text-center">
          <p className="font-display text-7xl md:text-9xl font-bold text-cathedral-amber animate-pulse-slow">
            75 / 25
          </p>
          <p className="font-ui text-lg text-cathedral-white mt-8">
            Perpetual. Auditable.
          </p>
        </div>
      </section>

      {/* ═══ ECOSYSTEM ═══ */}
      <section id="system" className="py-32 px-8 max-w-6xl mx-auto">
        <div className="grid md:grid-cols-3 gap-8">
          {[
            { name: 'NOIZY.AI', desc: 'Consent infrastructure. DreamChamber. GABRIEL.', color: 'border-cathedral-amber' },
            { name: 'NOIZYVOX', desc: 'Performance-grade voice agency. Characters, not samples.', color: 'border-cathedral-cyan' },
            { name: 'NOIZYFISH', desc: '888 titles. 34TB archive. Forty years of craft.', color: 'border-cathedral-amber' },
            { name: 'NOIZYLAB', desc: 'Tools. Repair. Experimental infrastructure.', color: 'border-cathedral-cyan' },
            { name: 'NOIZYKIDZ', desc: 'Music education. Accessibility. Haptics.', color: 'border-cathedral-amber' },
            { name: 'LIFELUV', desc: 'Peace, love, understanding. The human layer.', color: 'border-cathedral-cyan' },
          ].map((brand) => (
            <div key={brand.name} className={`bg-cathedral-card border-l-4 ${brand.color} p-8 rounded-lg hover:shadow-lg hover:translate-y-[-2px] transition-all duration-300`}>
              <h3 className="font-display text-xl font-bold text-cathedral-white mb-3">{brand.name}</h3>
              <p className="font-ui text-sm text-cathedral-muted">{brand.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ═══ DREAMCHAMBER ═══ */}
      <section id="dreamchamber" className="py-32 px-8 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-cathedral-cyan/5 to-transparent" />
        <div className="relative z-10 max-w-4xl mx-auto text-center">
          <h2 className="font-display text-4xl text-cathedral-cyan mb-6">DreamChamber</h2>
          <p className="font-ui text-lg text-cathedral-white mb-16">
            Where human signal becomes protected creative infrastructure.
          </p>
          <div className="grid md:grid-cols-5 gap-4 text-center">
            {['Threshold', 'Signal Capture', 'Character Forge', 'NOIZY PROOF', 'LIFELUV'].map((step, i) => (
              <div key={step} className="flex flex-col items-center">
                <div className="w-12 h-12 rounded-full border-2 border-cathedral-cyan flex items-center justify-center text-cathedral-cyan font-ui font-bold mb-3">
                  {i + 1}
                </div>
                <span className="font-ui text-xs text-cathedral-white">{step}</span>
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
            Consent does not exist for this use. Blocked.
          </p>
          <p className="font-ui text-sm text-cathedral-muted mt-6">
            The conscience of the system. Alive, not chatty.
          </p>
        </div>
      </section>

      {/* ═══ ECONOMICS ═══ */}
      <section className="py-32 px-8 max-w-6xl mx-auto">
        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-cathedral-card p-8 rounded-lg text-center">
            <p className="font-display text-3xl text-cathedral-amber mb-2">75%</p>
            <p className="font-ui text-cathedral-white mb-1">To the Artist</p>
            <p className="font-ui text-sm text-cathedral-muted">Real-time routing. No silent deductions.</p>
          </div>
          <div className="bg-cathedral-card p-8 rounded-lg text-center">
            <p className="font-display text-3xl text-cathedral-cyan mb-2">Estate</p>
            <p className="font-ui text-cathedral-white mb-1">Inheritable Value</p>
            <p className="font-ui text-sm text-cathedral-muted">Earns while you live. Passes when you don't.</p>
          </div>
          <div className="bg-cathedral-card p-8 rounded-lg text-center">
            <p className="font-display text-3xl text-cathedral-amber mb-2">$0</p>
            <p className="font-ui text-cathedral-white mb-1">To Say No</p>
            <p className="font-ui text-sm text-cathedral-muted">Unconditional revocation. Artist pays nothing.</p>
          </div>
        </div>
      </section>

      {/* ═══ THE EPOCHS ═══ */}
      <section className="py-32 px-8 max-w-4xl mx-auto">
        <div className="space-y-6">
          {[
            { epoch: 'I', era: 'Sheet Music', year: '1400s', who: 'Publishers profited.', dim: true },
            { epoch: 'II', era: 'Recording', year: '1920s', who: 'Labels profited.', dim: true },
            { epoch: 'III', era: 'Digital', year: '2000s', who: 'Platforms profited.', dim: true },
            { epoch: 'IV', era: 'Streaming', year: '2010s', who: 'Extractors profited.', dim: true },
            { epoch: 'V', era: 'NOIZY', year: '2026', who: 'CREATORS PROFIT.', dim: false },
          ].map((e) => (
            <div key={e.epoch} className={`flex items-center gap-6 ${e.dim ? 'opacity-30' : ''}`}>
              <span className={`font-display text-2xl w-12 ${e.dim ? 'text-cathedral-muted' : 'text-cathedral-amber'}`}>{e.epoch}</span>
              <span className={`font-ui flex-1 ${e.dim ? 'text-cathedral-muted' : 'text-cathedral-white text-xl font-semibold'}`}>{e.era}</span>
              <span className={`font-ui text-sm ${e.dim ? 'text-cathedral-muted' : 'text-cathedral-amber font-bold'}`}>{e.who}</span>
            </div>
          ))}
        </div>
      </section>

      {/* ═══ THREE LAWS ═══ */}
      <section className="py-24 px-8 max-w-3xl mx-auto text-center">
        <div className="space-y-4">
          <p className="font-ui text-lg text-cathedral-white">If it is not consented, it does not generate.</p>
          <p className="font-ui text-lg text-cathedral-white">If it is not attributable, it is not trusted.</p>
          <p className="font-ui text-lg text-cathedral-white">If it is not paid, it is not allowed.</p>
        </div>
      </section>

      {/* ═══ CLOSE ═══ */}
      <section className="py-32 px-8 max-w-3xl mx-auto text-center">
        <p className="font-display text-6xl md:text-8xl font-bold text-cathedral-amber animate-pulse-slow mb-12">
          GORUNFREE
        </p>
        <div className="space-y-2">
          <p className="font-ui text-cathedral-white">Your voice is identity.</p>
          <p className="font-ui text-cathedral-white">Your identity is sovereign.</p>
        </div>
      </section>

      {/* ═══ SILENCE ═══ */}
      <section className="h-32 bg-cathedral-black" />
    </main>
  )
}
