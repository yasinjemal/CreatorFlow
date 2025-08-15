<template>
	<div>
		<h1 class="text-3xl font-bold mb-4">Integrations</h1>
		<div class="card bg-base-200 shadow">
			<div class="card-body">
				<h2 class="card-title">LinkedIn</h2>
				<p class="opacity-80 text-sm">Connect your LinkedIn to publish posts.</p>
				<div class="join">
					<input v-model="userId" class="input input-bordered join-item" placeholder="user id/email"/>
					<a class="btn btn-primary join-item" :href="`${apiBase}/social/linkedin/start?user_id=${encodeURIComponent(userId)}`">Connect LinkedIn</a>
					<button class="btn join-item" @click="fetchMe">Fetch URN</button>
				</div>
				<div v-if="urn" class="mt-2 text-sm opacity-80">LinkedIn URN: <span class="badge badge-outline">{{ urn }}</span></div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
const apiBase = useRuntimeConfig().public.apiBase
const user = useUser()
const userId = ref(user.email || 'demo@creatorflow.app')
const urn = ref('')
const route = useRoute()
onMounted(async () => {
	if (route.query.connected === 'linkedin' && route.query.user_id) {
		userId.value = String(route.query.user_id)
		await fetchMe()
	}
})

async function fetchMe(){
	const { data } = await $fetch(`${apiBase}/social/linkedin/me`, { params: { user_id: userId.value } })
	urn.value = data.urn || ''
}
</script>


