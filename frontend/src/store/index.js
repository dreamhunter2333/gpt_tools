import { ref } from "vue";
import { createGlobalState, useStorage } from '@vueuse/core'

export const useGlobalState = createGlobalState(
    () => {
        const loading = ref(false);
        const result = ref('');
        const themeSwitch = useStorage('themeSwitch', false);
        return {
            loading,
            themeSwitch,
            result
        }
    },
)
