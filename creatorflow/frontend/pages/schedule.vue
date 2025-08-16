<script setup lang="ts">
const config = useRuntimeConfig()
const apiBase = config.public.apiBase
const token = useCookie('token')
const headers = computed(()=>({ Authorization: `Bearer ${token.value}` }))

const form = reactive({ content_id: '', brand_id: '', platforms: ['instagram'], post_at: new Date(Date.now()+3600*1000).toISOString() })

const { data: brands } = await useFetch(`${apiBase}/brand`, { headers: headers.value })
watchEffect(()=>{ if (!form.brand_id && (brands.value||[])[0]) form.brand_id = (brands.value as any[])[0].id })

const { data: schedules, refresh } = await useFetch(`${apiBase}/schedule`, { headers: headers.value })

async function createSchedule(){
	await $fetch(`${apiBase}/schedule`, { method: 'POST', body: form, headers: headers.value })
	await refresh()
}
</script>

<template>
	<div>
		<h1 class="text-2xl font-semibold mb-4">Schedule</h1>
		<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
			<div class="p-4 border rounded space-y-2">
				<label class="block text-sm">Brand</label>
				<select v-model="form.brand_id" class="border p-2 w-full">
					<option v-for="b in brands||[]" :key="b.id" :value="b.id">{{ b.name }}</option>
				</select>
				<label class="block text-sm">Content ID</label>
				<input v-model="form.content_id" class="border p-2 w-full" placeholder="content id"/>
				<label class="block text-sm">Platforms (comma separated)</label>
				<input v-model="(form.platforms as any)" class="border p-2 w-full" />
				<label class="block text-sm">Post At (ISO)</label>
				<input v-model="form.post_at" class="border p-2 w-full" />
				<button @click="createSchedule" class="bg-blue-600 text-white px-4 py-2 rounded">Schedule</button>
			</div>
			<div class="p-4 border rounded">
				<h2 class="font-medium mb-2">Upcoming</h2>
				<ul>
					<li v-for="s in schedules||[]" :key="s.id" class="py-1">
						{{ s.post_at }} — {{ s.platforms.join(', ') }} (brand {{ s.brand_id }})
					</li>
				</ul>
			</div>
		</div>
	</div>
</template>