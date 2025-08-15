<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<script setup lang="ts">
const ui = useUi()
onMounted(() => ui.init())
</script>
