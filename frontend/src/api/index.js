import { fetchEventSource, EventStreamContentType } from '@microsoft/fetch-event-source';

import { useGlobalState } from '../store'

const API_BASE = import.meta.env.VITE_API_BASE || "";
const { loading, result } = useGlobalState();


const generate = async (prompt_type, prompt, message) => {
    try {
        loading.value = true;
        result.value = '';
        await fetchEventSource(`${API_BASE}/api/chatgpt`, {
            method: "POST",
            body: JSON.stringify({
                prompt: prompt
            }),
            headers: {
                "Content-Type": "application/json"
            },
            async onopen(response) {
                if (response.ok && response.headers.get('content-type') === EventStreamContentType) {
                    return;
                } else if (response.status >= 400 && response.status < 500 && response.status !== 429) {
                    throw new Error(`失败: ${response.status}`);
                }
            },
            onmessage(msg) {
                if (msg.event === 'FatalError') {
                    throw new FatalError(msg.data);
                }
                if (!msg.data) {
                    return;
                }
                try {
                    result.value += JSON.parse(msg.data);
                } catch (error) {
                    console.error(error);
                }
            },
            onclose() { },
            onerror(err) {
                result.value = `占卜失败: ${err.message}`;
                throw new Error(`占卜失败: ${err.message}`);
            }
        });
    } catch (error) {
        console.error(error);
        message.error(error.message || "占卜失败");
        result.value = error.message || "占卜失败";
    } finally {
        loading.value = false;
    }
};

export const api = {
    generate: generate
}
