export default function Loading() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        {/* Animated logo placeholder */}
        <div className="relative w-16 h-16 mx-auto mb-4">
          <div
            className="absolute inset-0 rounded-xl animate-pulse"
            style={{
              background: 'linear-gradient(135deg, #8B5CF6, #EC4899, #F59E0B)',
              backgroundSize: '300% 300%',
              animation: 'gradientShift 3s ease infinite, pulse 2s ease-in-out infinite',
            }}
          />
          <div className="absolute inset-0 rounded-xl flex items-center justify-center">
            <span className="text-white font-bold text-2xl">N</span>
          </div>
        </div>

        {/* Loading bars */}
        <div className="flex items-center justify-center gap-1">
          {Array.from({ length: 5 }).map((_, i) => (
            <div
              key={i}
              className="w-1 bg-violet-500/60 rounded-full"
              style={{
                height: '16px',
                animation: `loadingBar 1s ease-in-out infinite`,
                animationDelay: `${i * 0.1}s`,
              }}
            />
          ))}
        </div>

        <p className="mt-4 text-xs font-mono text-noizy-silver/50 uppercase tracking-wider">
          Loading
        </p>
      </div>
    </div>
  )
}
