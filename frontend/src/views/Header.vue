<script setup>
import { NLayoutHeader, NButton, NSwitch } from 'naive-ui'
import { useGlobalState } from '../store'

const { themeSwitch } = useGlobalState()

</script>

<template>
    <n-layout-header>
        <div>
            <h2>GPT Toys</h2>
        </div>
        <div>
            <n-switch v-model:value="themeSwitch">
                <template #checked>
                    暗色
                </template>
                <template #unchecked>
                    亮色
                </template>
            </n-switch>
            <n-button tag="a" target="_blank" tertiary type="primary" round href="https://github.com/dreamhunter2333">Star
                on Github
            </n-button>
        </div>
    </n-layout-header>
</template>

<style scoped>
.n-layout-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}
</style>
