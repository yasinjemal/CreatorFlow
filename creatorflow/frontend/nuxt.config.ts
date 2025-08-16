// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
	ssr: true,
	modules: [
		'@nuxtjs/tailwindcss',
	],
	runtimeConfig: {
		public: {
			apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000',
		}
	},
	app: {
		head: {
			title: 'CreatorFlow',
			meta: [
				{ name: 'viewport', content: 'width=device-width, initial-scale=1' },
			]
		}
	},
	routeRules: {
		'/': { swr: 60 },
	}
})