<template>
	<div>
		<h1 class="text-3xl font-bold mb-4">Library</h1>
		<div class="card bg-base-200 shadow">
			<div class="card-body">
				<form class="grid md:grid-cols-3 gap-2" @submit.prevent="create">
					<input v-model="topic" placeholder="Topic" class="input input-bordered"/>
					<select v-model="platform" class="select select-bordered">
						<option>instagram</option><option>tiktok</option><option>youtube</option>
						<option>linkedin</option><option>twitter</option><option>facebook</option><option>pinterest</option>
					</select>
					<button class="btn btn-primary">Create</button>
				</form>
			</div>
		</div>

		<div class="grid md:grid-cols-2 gap-4 mt-4">
			<div v-for="it in items" :key="it._id" class="card bg-base-200 shadow">
				<div class="card-body">
					<div class="text-xs opacity-70">{{ it.platform }}</div>
					<div class="font-semibold">{{ it.topic }}</div>
					<div class="text-sm opacity-80">{{ it.caption }}</div>
					<div class="mt-2 flex gap-2">
						<button class="btn btn-sm" @click="approve(it._id)">Approve</button>
						<button class="btn btn-sm btn-outline" @click="comment(it._id)">Comment</button>
						<button class="btn btn-sm btn-accent" @click="postLinkedIn(it)">Post to LinkedIn</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
const { $api } = useNuxtApp() as any
const user = useUser()
const topic = ref('New post idea')
const platform = ref('instagram')
const items = ref<any[]>([])
const linkedinUrn = ref('')

async function load(){
	const { data } = await $api.get('/library/list', { params: { user_id: user.email || 'demo' }})
	items.value = data.items
}

async function loadProfile(){
	const { data } = await $api.get('/social/profile', { params: { user_id: user.email || 'demo@creatorflow.app' } })
	linkedinUrn.value = data.profile?.linkedin_urn || ''
}

async function create(){
	const { data } = await $api.post('/content/generate', { topic: topic.value, platform: platform.value, cta: 'Follow for more!' })
	await $api.post('/library/item', { user_id: user.email || 'demo', platform: platform.value, topic: topic.value, caption: data.caption, hashtags: data.hashtags })
	await load()
}

async function approve(id: string){
	await $api.post(`/library/item/${id}/approve`)
	await load()
}

async function comment(id: string){
	const text = prompt('Comment') || ''
	if (!text) return
	await $api.post(`/library/item/${id}/comment`, { text, author: user.email || 'demo' })
	await load()
}

async function postLinkedIn(it: any){
	if (!linkedinUrn.value){
		alert('LinkedIn not connected or URN missing. Connect via Integrations > LinkedIn, then click Fetch URN.')
		return
	}
	await $api.post('/schedule/publish', {
		user_id: user.email || 'demo@creatorflow.app',
		platform: 'linkedin',
		author: linkedinUrn.value,
		text: it.caption
	})
	alert('Queued to publish on LinkedIn (requires connected OAuth)')
}

onMounted(async () => { await Promise.all([load(), loadProfile()]) })
</script>
