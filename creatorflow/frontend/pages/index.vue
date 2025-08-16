<script setup lang="ts">
const config = useRuntimeConfig()
const apiBase = config.public.apiBase
const { data: health } = await useFetch(`${apiBase}/health`)
</script>

<template>
	<div>
		<h1 class="text-2xl font-semibold mb-4">Dashboard</h1>
		<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
			<div class="p-4 border rounded">
				<h2 class="font-medium">System</h2>
				<p class="text-sm text-gray-600">API: {{ health?.status || 'unknown' }}</p>
			</div>
			<div class="p-4 border rounded">
				<h2 class="font-medium">Create Content</h2>
				<NuxtLink class="text-blue-600" to="/content">Start</NuxtLink>
			</div>
			<div class="p-4 border rounded">
				<h2 class="font-medium">Manage Brand</h2>
				<NuxtLink class="text-blue-600" to="/brand">Open</NuxtLink>
			</div>
		</div>
	</div>
</template>