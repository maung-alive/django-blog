module.exports = {
  content: [
      './templates/**/*.html',
  ],
  theme: {
    extend: {
      fontFamily: {
        'sans': ['ui-sans-serif', 'system-ui', 'Helvetica', 'Arial', 'sans-serif'],
        'serif': ['ui-serif', 'Georgia', 'Helvetica', 'Arial', 'serif'],
        'mono': ['ui-monospace', 'SFMono-Regular'],
        'josefin': ['Josefin Sans', 'Helvetica', 'Arial', 'sans-serif'],
        'mukta': ['Mukta', 'Helvetica', 'Arial', 'sans-serif'],
        'nunito': ['Nunito', 'Helvetica', 'Arial', 'sans-serif'],
        'poppins': ['Poppins', 'Helvetica', 'Arial', 'sans-serif'],
      }  
    },
  },
  plugins: [
  ],
}