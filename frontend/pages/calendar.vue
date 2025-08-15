<template>
  <div>
    <h1 class="text-3xl font-bold mb-4">Calendar & Scheduling</h1>
    <form @submit.prevent="queue" class="card bg-base-200 shadow">
      <div class="card-body">
        <textarea v-model="payload" class="textarea textarea-bordered h-40"></textarea>
        <button class="btn btn-secondary">Queue Publish</button>
      </div>
    </form>
    <div v-if="job" class="mt-4 alert alert-success">Queued job: {{ job }}</div>
    <div v-if="job" class="mt-4">
      <button class="btn btn-sm" @click="check">Check Status</button>
      <pre class="mt-2 text-xs bg-base-200 p-2 rounded">{{ status }}</pre>
    </div>
  </div>
</template>

<script setup lang="ts">
const payload = ref(JSON.stringify({ platform:"instagram", caption:"Hello world", mediaUrl:"/path/to.mp4" }, null, 2))
const job = ref('')
const status = ref<any>('')
const { $api } = useNuxtApp() as any
async function queue(){
  const { data } = await $api.post('/schedule/publish', JSON.parse(payload.value))
  job.value = data.job_id
  status.value = 'queued'
}
async function check(){
  if (!job.value) return
  const { data } = await $api.get(`/schedule/status/${job.value}`)
  status.value = data
}
</script>
