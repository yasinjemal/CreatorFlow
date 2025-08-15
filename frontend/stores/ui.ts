import { defineStore } from 'pinia'

export const useUi = defineStore('ui', {
	state: () => ({ theme: 'business' as string }),
	actions: {
		init(){
			if (process.client) {
				const saved = localStorage.getItem('cf_theme')
				if (saved) this.theme = saved
				document.documentElement.setAttribute('data-theme', this.theme)
			}
		},
		setTheme(t: string){
			this.theme = t
			if (process.client) {
				localStorage.setItem('cf_theme', t)
				document.documentElement.setAttribute('data-theme', t)
			}
		}
	}
})
