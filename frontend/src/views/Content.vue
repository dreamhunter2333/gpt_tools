<script setup>
import { NSpace, NRadioButton, NRadioGroup } from 'naive-ui'
import { NButton, NLayout, NInput, NCard } from 'naive-ui'
import { ref } from "vue";
import { useMessage } from 'naive-ui'
import { useGlobalState } from '../store'
import { api } from '../api'

const message = useMessage()
const prompt_type = ref('lipstick')
const prompt = ref('')

const generate = async () => {
  const { data } = await api.generate(
    prompt_type.value,
    prompt.value || '苹果手机怎么这么贵',
    message
  )
  result.value = data
}
</script>

<template>
  <div>
    <n-layout>
      <div class="block">
        <n-radio-group v-model:value="prompt_type">
          <n-radio-button label="李佳琦模拟" value="lipstick" />
        </n-radio-group>
      </div>
      <div class="block">
        <n-input v-model:value="prompt" type="textarea" round maxlength="40" :autosize="{ minRows: 3 }"
          placeholder="苹果手机怎么这么贵" />
      </div>
      <div class="block">
        <n-button @click="generate" tertiary round type="primary">
          生成
        </n-button>
      </div>
    </n-layout>
  </div>
</template>

<style scoped>
.block {
  margin-top: 10px;
}
</style>
