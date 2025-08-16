<template>
	<div>
		<header class="border-b">
			<nav class="max-w-7xl mx-auto flex items-center justify-between p-4">
				<div class="text-xl font-semibold">CreatorFlow</div>
				<div class="flex gap-4 text-sm">
					<NuxtLink to="/">Dashboard</NuxtLink>
					<NuxtLink to="/brand">Brand</NuxtLink>
					<NuxtLink to="/content">Content</NuxtLink>
					<NuxtLink to="/schedule">Schedule</NuxtLink>
					<NuxtLink to="/analytics">Analytics</NuxtLink>
				</div>
			</nav>
		</header>
		<main class="max-w-7xl mx-auto p-4">
			<NuxtPage />
		</main>
	</div>
</template>