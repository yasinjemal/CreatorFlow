<template>
  <div>
    <div class="hero bg-base-200 rounded-xl">
      <div class="hero-content text-center">
        <div class="max-w-xl">
          <h1 class="text-4xl font-bold">Welcome to CreatorFlow</h1>
          <p class="py-4 opacity-80">Generate, optimize, schedule, and analyze multi-platform content.</p>
          <div class="stats shadow w-full">
            <div class="stat">
              <div class="stat-title">Platforms</div>
              <div class="stat-value">7</div>
            </div>
            <div class="stat">
              <div class="stat-title">AI Drafts</div>
              <div class="stat-value">∞</div>
            </div>
            <div class="stat">
              <div class="stat-title">Queue</div>
              <div class="stat-value">Live</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
      <section class="card bg-base-200 shadow">
        <div class="card-body">
          <h2 class="card-title">Quick Login</h2>
          <form class="form-control" @submit.prevent="login">
            <input v-model="email" placeholder="email" class="input input-bordered mb-2"/>
            <input v-model="password" type="password" placeholder="password" class="input input-bordered mb-4"/>
            <button class="btn btn-primary">Login</button>
          </form>
        </div>
      </section>

      <section class="card bg-base-200 shadow">
        <div class="card-body">
          <h2 class="card-title">Generate a Caption</h2>
          <form @submit.prevent="gen" class="grid gap-2">
            <input v-model="topic" placeholder="Topic" class="input input-bordered"/>
            <select v-model="platform" class="select select-bordered">
              <option>instagram</option><option>tiktok</option><option>youtube</option>
              <option>linkedin</option><option>twitter</option><option>facebook</option><option>pinterest</option>
            </select>
            <button class="btn btn-secondary">Generate</button>
          </form>
          <div v-if="result" class="mt-4 whitespace-pre-wrap text-sm p-3 bg-base-300 rounded">{{ result }}</div>
          <div class="mt-6">
            <h3 class="font-semibold mb-2">Trending Topics</h3>
            <div class="flex gap-2 mb-2">
              <select v-model="platform" class="select select-bordered">
                <option>instagram</option><option>tiktok</option><option>youtube</option>
                <option>linkedin</option><option>twitter</option><option>facebook</option><option>pinterest</option>
              </select>
              <button class="btn" @click="loadTrends">Load</button>
            </div>
            <div class="grid gap-2 md:grid-cols-2">
              <div v-for="t in trends" :key="t" class="badge badge-outline p-4 justify-start">{{ t }}</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
const email = ref('demo@creatorflow.app')
const password = ref('demo1234')
const topic = ref('AI tools for creators')
const platform = ref('instagram')
const result = ref('')
const trends = ref<string[]>([])

const user = useUser()
const { $api } = useNuxtApp() as any

async function login() {
  const { data } = await $api.post('/auth/login', { email: email.value, password: password.value }).catch(async () => {
    // seed user if not exists
    await $api.post('/auth/register', { email: email.value, password: password.value, name: 'Demo' })
    return await $api.post('/auth/login', { email: email.value, password: password.value })
  })
  user.set(data)
}

async function gen() {
  try {
    const { data } = await $api.post('/content/generate', { topic: topic.value, platform: platform.value, cta: "Follow for more!" })
    result.value = data.caption + "\n\n" + (data.hashtags || []).join(' ')
  } catch (e:any) {
    result.value = 'Generation failed. Please check API is running.'
  }
}

async function loadTrends(){
  const { data } = await $api.get('/content/trending', { params: { platform: platform.value } })
  trends.value = data.topics
}
</script>
