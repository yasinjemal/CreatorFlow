<template>
  <div>
    <h1 class="text-3xl font-bold mb-4">Composer</h1>
    <div class="grid md:grid-cols-2 gap-6">
      <section class="card bg-base-200 shadow">
        <div class="card-body">
          <h2 class="card-title">Brand Voice</h2>
          <textarea v-model="voice" class="textarea textarea-bordered h-40"></textarea>
        </div>
      </section>
      <section class="card bg-base-200 shadow">
        <div class="card-body">
          <h2 class="card-title">Preview</h2>
          <div class="text-sm whitespace-pre-wrap p-3 bg-base-300 rounded min-h-40">{{ output }}</div>
        </div>
      </section>
    </div>
    <div class="mt-4 flex gap-2">
      <input v-model="topic" placeholder="Topic..." class="input input-bordered w-full" />
      <select v-model="platform" class="select select-bordered">
        <option>instagram</option><option>tiktok</option><option>youtube</option>
        <option>linkedin</option><option>twitter</option><option>facebook</option><option>pinterest</option>
      </select>
      <button class="btn btn-primary" @click="compose">Compose</button>
    </div>
  </div>
</template>

<script setup lang="ts">
const voice = ref('confident, witty, practical')
const topic = ref('Batching content for busy creators')
const platform = ref('tiktok')
const output = ref('')
const { $api } = useNuxtApp() as any
async function compose(){
  const { data } = await $api.post('/content/generate', { topic: topic.value, platform: platform.value, brand_voice: voice.value, cta: 'Save & share!' })
  output.value = data.caption + "\n\n" + data.hashtags.join(' ')
}
</script>
