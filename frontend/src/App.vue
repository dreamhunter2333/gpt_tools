<script setup>
import { NMessageProvider, NGrid, NBackTop, NSpin } from 'naive-ui'
import { NGi, NSpace, NButton, NConfigProvider, NCard } from 'naive-ui'
import { darkTheme, NGlobalStyle } from 'naive-ui'
import { zhCN } from 'naive-ui'
import { computed, onMounted } from 'vue'

import Content from './views/Content.vue'
import Header from './views/Header.vue'
import { useGlobalState } from './store'

const { themeSwitch, loading, result } = useGlobalState()
const theme = computed(() => themeSwitch.value ? darkTheme : null)

</script>

<template>
  <n-config-provider :locale="zhCN" :theme="theme">
    <n-global-style />
    <n-message-provider>
      <n-grid x-gap="12" :cols="8">
        <n-gi span="1"></n-gi>
        <n-gi span="6">
          <div class="main">
            <n-space vertical>
              <n-spin description="loading..." :show="loading">
                <Header />
                <Content />
              </n-spin>
              <n-card title="结果">
                {{ result }}
              </n-card>
            </n-space>
          </div>
        </n-gi>
        <n-gi span="1"></n-gi>
      </n-grid>
      <n-back-top :right="100" />
    </n-message-provider>
  </n-config-provider>
</template>


<style>
.n-button {
  margin-left: 10px;
  margin-right: 10px;
}

.n-switch {
  margin-left: 10px;
  margin-right: 10px;
}
</style>

<style scoped>
.side {
  height: 100vh;
}

.main {
  height: 100vh;
  text-align: center;
}

.n-grid {
  height: 100%;
}

.n-gi {
  height: 100%;
}

.n-space {
  height: 100%;
}
</style>
