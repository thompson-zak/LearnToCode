/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './src/views/*.{html,js,vue}',
    './src/components/*.{html,js,vue}'
  ],
  theme: {
    extend: {
      colors: {
        'github-dark-theme': '#0d1117',
      }
    },
  },
  plugins: [],
}

