<template>
	<div>
		<h1 class="text-3xl font-bold mb-4">Brand</h1>
		<div class="card bg-base-200 shadow">
			<div class="card-body grid md:grid-cols-2 gap-4">
				<div>
					<label class="label">Brand Name</label>
					<input v-model="profile.name" class="input input-bordered"/>
					<label class="label mt-4">Voice</label>
					<textarea v-model="profile.voice" class="textarea textarea-bordered h-32" placeholder="confident, witty, practical"></textarea>
					<label class="label mt-4">Primary Color</label>
					<input v-model="profile.color" type="color" class="input input-bordered w-24"/>
					<label class="label mt-4">CTA</label>
					<input v-model="profile.cta" class="input input-bordered" placeholder="Follow for more!"/>
					<div class="mt-4 flex gap-2">
						<button class="btn btn-primary" @click="save">Save</button>
						<button class="btn" @click="load">Reload</button>
					</div>
				</div>
				<div>
					<label class="label">Tone Check</label>
					<textarea v-model="sample" class="textarea textarea-bordered h-40" placeholder="Paste content to analyze..."></textarea>
					<button class="btn mt-2" @click="toneCheck">Analyze Tone</button>
					<div v-if="tone" class="alert alert-info mt-3">
						<div>
							<div class="font-semibold">Score: {{ tone.score }}</div>
							<div class="text-sm opacity-80">{{ tone.summary }}</div>
						</div>
					</div>
					<ul class="mt-2 list-disc pl-5 text-sm" v-if="tone?.issues?.length">
						<li v-for="i in tone.issues" :key="i">{{ i }}</li>
					</ul>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
const { $api } = useNuxtApp() as any
const user = useUser()
const profile = reactive({ name: 'My Brand', voice: 'confident, witty, practical', color: '#00FFAA', cta: 'Follow for more!' })
const sample = ref('This is a quick sample to check tone.')
const tone = ref<any>(null)

async function save(){
	await $api.post('/assets/brand', { user_id: user.email || 'demo', profile })
}

async function load(){
	const { data } = await $api.get('/assets/brand', { params: { user_id: user.email || 'demo' }})
	Object.assign(profile, data.profile || {})
}

async function toneCheck(){
	const { data } = await $api.post('/assets/brand/tone-check', { text: sample.value, brand_voice: profile.voice })
	tone.value = data.analysis
}

onMounted(load)
</script>
