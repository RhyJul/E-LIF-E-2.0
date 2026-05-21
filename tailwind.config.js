/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./elife_app/**/*.{py,html}",
    ],
    theme: {
        extend: {
            colors: {
                primary: "#22c55e",
                secondary: "#16a34a",
                dark: "#0f4c23",
            },
            fontFamily: {
                sans: ["Source Sans 3", "sans-serif"],
                display: ["Space Grotesk", "sans-serif"],
            },
            backdropFilter: {
                'none': 'none',
                'blur': 'blur(10px)',
            },
        },
    },
    plugins: [],
}
