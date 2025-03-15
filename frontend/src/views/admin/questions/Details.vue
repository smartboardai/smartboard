<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import { t } from '@/locales'

const route = useRoute()
const router = useRouter()
const message = useMessage()
const loading = ref(false)
const question = ref<any>(null)
const newAnswer = ref('')

const questionId = route.params.id as string

async function fetchQuestionDetails() {
  try {
    loading.value = true
    const response = await fetch(`/api/discussions/questions/${questionId}/`)
    const data = await response.json()
    question.value = data
  } catch (error) {
    message.error(t('common.errorSomeThing'))
  } finally {
    loading.value = false
  }
}

async function submitAnswer() {
  try {
    const response = await fetch(`/api/discussions/questions/${questionId}/answers/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ content: newAnswer.value }),
    })
    
    if (response.ok) {
      message.success(t('common.submitSuccess'))
      newAnswer.value = ''
      await fetchQuestionDetails()
    } else {
      throw new Error()
    }
  } catch (error) {
    message.error(t('common.submitFailed'))
  }
}

onMounted(() => {
  fetchQuestionDetails()
})
</script>

<template>
  <div class="p-4">
    <div class="mb-4">
      <NButton @click="router.back()">{{ t('common.back') }}</NButton>
    </div>

    <div v-if="loading" class="flex justify-center">
      <NSpin size="large" />
    </div>

    <template v-else-if="question">
      <NCard>
        <template #header>
          <div class="flex justify-between items-center">
            <h2 class="text-2xl font-bold">{{ question.title }}</h2>
            <NTag :type="question.category === 'technical' ? 'info' : 'success'">
              {{ question.category }}
            </NTag>
          </div>
        </template>

        <div class="space-y-4">
          <div class="question-content">
            {{ question.content }}
          </div>

          <div v-if="question.media?.length" class="attachments">
            <h4 class="font-semibold mb-2">{{ t('common.attachments') }}</h4>
            <div class="flex gap-2">
              <NButton v-for="file in question.media" :key="file.id" size="small" tag="a" :href="file.file" target="_blank">
                {{ file.file.split('/').pop() }}
              </NButton>
            </div>
          </div>
        </div>
      </NCard>

      <div class="mt-8">
        <h3 class="text-xl font-bold mb-4">{{ t('common.answers') }}</h3>
        <div class="space-y-4">
          <NCard v-for="answer in question.answers" :key="answer.id">
            {{ answer.content }}
            <template #footer>
              <NTime :time="new Date(answer.createdAt)" />
            </template>
          </NCard>
        </div>
      </div>

      <div class="mt-8">
        <h3 class="text-xl font-bold mb-4">{{ t('common.submitAnswer') }}</h3>
        <NForm>
          <NFormItem>
            <NInput
              v-model:value="newAnswer"
              type="textarea"
              :rows="4"
              :placeholder="t('common.writeYourAnswer')"
            />
          </NFormItem>
          <NButton type="primary" @click="submitAnswer" :disabled="!newAnswer">
            {{ t('common.submit') }}
          </NButton>
        </NForm>
      </div>
    </template>
  </div>
</template> 