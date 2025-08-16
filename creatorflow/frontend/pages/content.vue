<script setup lang="ts">
const config = useRuntimeConfig()
const apiBase = config.public.apiBase
const token = useCookie('token')
const headers = computed(()=>({ Authorization: `Bearer ${token.value}` }))

const form = reactive({ platform: 'instagram', topic: 'New product launch', brand_id: '', count: 10, duration_seconds: 30 })
const caption = ref('')
const hashtags = ref<string[]>([])
const script = ref('')

const { data: brands } = await useFetch(`${apiBase}/brand`, { headers: headers.value })
watchEffect(()=>{ if (!form.brand_id && (brands.value||[])[0]) form.brand_id = (brands.value as any[])[0].id })

async function genCaption(){
	const res = await $fetch(`${apiBase}/content/generate/caption`, { method: 'POST', body: { platform: form.platform, topic: form.topic, brand_id: form.brand_id }, headers: headers.value })
	caption.value = (res as any).caption
}
async function genHashtags(){
	const res = await $fetch(`${apiBase}/content/generate/hashtags`, { method: 'POST', body: { platform: form.platform, topic: form.topic, brand_id: form.brand_id, count: form.count }, headers: headers.value })
	hashtags.value = (res as any).hashtags
}
async function genScript(){
	const res = await $fetch(`${apiBase}/content/generate/script`, { method: 'POST', body: { platform: form.platform, topic: form.topic, brand_id: form.brand_id, duration_seconds: form.duration_seconds }, headers: headers.value })
	script.value = (res as any).script
}
</script>

<template>
	<div>
		<h1 class="text-2xl font-semibold mb-4">Content Generation</h1>
		<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
			<div class="p-4 border rounded space-y-2">
				<label class="block text-sm">Brand</label>
				<select v-model="form.brand_id" class="border p-2 w-full">
					<option v-for="b in brands||[]" :key="b.id" :value="b.id">{{ b.name }}</option>
				</select>
				<label class="block text-sm">Platform</label>
				<select v-model="form.platform" class="border p-2 w-full">
					<option>instagram</option>
					<option>tiktok</option>
					<option>youtube</option>
					<option>linkedin</option>
					<option>twitter</option>
				</select>
				<label class="block text-sm">Topic</label>
				<input v-model="form.topic" class="border p-2 w-full"/>
				<button @click="genCaption" class="bg-blue-600 text-white px-4 py-2 rounded w-full">Generate Caption</button>
				<button @click="genHashtags" class="bg-blue-600 text-white px-4 py-2 rounded w-full">Generate Hashtags</button>
				<button @click="genScript" class="bg-blue-600 text-white px-4 py-2 rounded w-full">Generate Script</button>
			</div>
			<div class="p-4 border rounded">
				<h2 class="font-medium mb-2">Caption</h2>
				<p class="whitespace-pre-wrap">{{ caption }}</p>
			</div>
			<div class="p-4 border rounded">
				<h2 class="font-medium mb-2">Hashtags</h2>
				<p>{{ hashtags.join(' ') }}</p>
				<h2 class="font-medium mt-4 mb-2">Script</h2>
				<p class="whitespace-pre-wrap">{{ script }}</p>
			</div>
		</div>
	</div>
</template>