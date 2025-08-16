<script setup lang="ts">
const config = useRuntimeConfig()
const apiBase = config.public.apiBase
const email = ref('demo@brand.com')
const token = useCookie('token')

async function ensureLogin() {
	if (!token.value) {
		const { data } = await $fetch(`${apiBase}/auth/signup`, { method: 'POST', body: { email, password: 'demo', name: 'Demo' } }).catch(()=>({data:null}))
		const login = await $fetch(`${apiBase}/auth/login`, { method: 'POST', body: { email, password: 'demo' } })
		token.value = (login as any).access_token
	}
}

await ensureLogin()

const headers = computed(()=>({ Authorization: `Bearer ${token.value}` }))

const { data: brands, refresh } = await useFetch(`${apiBase}/brand`, { headers: headers.value })

const form = reactive({ name: '', description: '', voice_characteristics: ['friendly','helpful'], style_guide: { punctuation: 'minimal' } })

async function createBrand() {
	await $fetch(`${apiBase}/brand`, { method: 'POST', body: form, headers: headers.value })
	await refresh()
	form.name = ''
}
</script>

<template>
	<div>
		<h1 class="text-2xl font-semibold mb-4">Brand</h1>
		<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
			<div class="p-4 border rounded">
				<h2 class="font-medium mb-2">Create Brand</h2>
				<input v-model="form.name" placeholder="Brand name" class="border p-2 w-full mb-2"/>
				<textarea v-model="form.description" placeholder="Description" class="border p-2 w-full mb-2"></textarea>
				<button @click="createBrand" class="bg-blue-600 text-white px-4 py-2 rounded">Create</button>
			</div>
			<div class="p-4 border rounded">
				<h2 class="font-medium mb-2">Your Brands</h2>
				<ul>
					<li v-for="b in brands || []" :key="b.id" class="py-1">{{ b.name }}</li>
				</ul>
			</div>
		</div>
	</div>
</template>