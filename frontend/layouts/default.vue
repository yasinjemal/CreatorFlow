<template>
  <div class="min-h-screen bg-base-100 text-base-content">
    <div class="navbar bg-base-200">
      <div class="flex-1">
        <NuxtLink to="/" class="btn btn-ghost text-xl">CreatorFlow</NuxtLink>
      </div>
      <div class="flex-none">
        <ul class="menu menu-horizontal px-1">
          <li><NuxtLink to="/dashboard">Dashboard</NuxtLink></li>
          <li><NuxtLink to="/composer">Composer</NuxtLink></li>
          <li><NuxtLink to="/calendar">Calendar</NuxtLink></li>
          <li><NuxtLink to="/brand">Brand</NuxtLink></li>
          <li><NuxtLink to="/library">Library</NuxtLink></li>
          <li><NuxtLink to="/integrations">Integrations</NuxtLink></li>
          <li>
            <details>
              <summary>Theme</summary>
              <ul class="p-2 bg-base-100 rounded-t-none">
                <li v-for="t in themes" :key="t"><a @click="setTheme(t)">{{ t }}</a></li>
              </ul>
            </details>
          </li>
        </ul>
      </div>
    </div>
    <main class="p-6 max-w-6xl mx-auto">
      <slot />
    </main>
  </div>
  
</template>

<script setup lang="ts">
const themes = ['business','dark','light','emerald','dracula']
const ui = useUi()
function setTheme(t: string){ ui.setTheme(t) }
</script>
