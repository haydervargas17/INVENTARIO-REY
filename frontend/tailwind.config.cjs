module.exports = {
  content: ["./index.html", "./src/**/*.{ts,tsx,js,jsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#EEF2FF',
          100: '#E0E7FF',
          500: '#6366F1'
        },
        accent: {
          500: '#10B981'
        }
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui'],
        street: ['Hanken Grotesk', 'ui-sans-serif', 'system-ui'],
        mono: ['JetBrains Mono', 'ui-monospace', 'SFMono-Regular'],
        blackletter: ['Pirata One', 'serif']
      }
    },
  },
  plugins: [],
}
