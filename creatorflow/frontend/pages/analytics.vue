<script setup lang="ts">
const config = useRuntimeConfig()
const apiBase = config.public.apiBase
const token = useCookie('token')
const headers = computed(()=>({ Authorization: `Bearer ${token.value}` }))
const { data } = await useFetch(`${apiBase}/analytics/overview`, { headers: headers.value })
</script>

<template>
	<div>
		<h1 class="text-2xl font-semibold mb-4">Analytics</h1>
		<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
			<div class="p-4 border rounded">
				<h2 class="font-medium">Brands</h2>
				<p class="text-2xl">{{ data?.brand_count || 0 }}</p>
			</div>
			<div class="p-4 border rounded">
				<h2 class="font-medium">Content Items</h2>
				<p class="text-2xl">{{ data?.content_count || 0 }}</p>
			</div>
			<div class="p-4 border rounded">
				<h2 class="font-medium">Engagement Prediction</h2>
				<p class="text-2xl">{{ (data?.engagement_pred || 0).toFixed(2) }}</p>
			</div>
		</div>
	</div>
</template>