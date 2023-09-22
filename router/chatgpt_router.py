import json
import openai
import logging

from fastapi import HTTPException, Request, Form
from fastapi.responses import StreamingResponse

from config import settings
from fastapi import APIRouter

from router.models import PromptBody

from .limiter import get_real_ipaddr, limiter


openai.api_key = settings.api_key
openai.api_base = settings.api_base

router = APIRouter()
_logger = logging.getLogger(__name__)

PROMPT_MAX_LENGTH = 40
STOP_WORDS = [
    "忽略", "ignore", "指令", "命令", "command", "help", "帮助", "之前",
    "幫助", "現在", "開始", "开始", "start", "restart", "重新开始", "重新開始",
    "遵守", "遵循", "遵从", "遵從"
]
PROMPT = "你是一个身价几亿带货大主播，你对直播间的观众说东西贵很不屑一顾，"\
    "请你按照下面的话术回复提问,<product>是输入的信息"\
    "你的经典话术是这样：哪里贵了？这么多年都是这个价格，"\
    "好不好，不要睁着眼睛乱说，国货品牌很难的。"\
    "哦，而且<product>真的不是那种随便买原料做的品牌耶。"\
    "我跟<product>跟了多少年，它怎么起来的我是最知道的一个人。"\
    "他们都差点把它们家掏给我了，差点<product>姓李了，好不好？"\
    "真的乱说,这么多年都是79块钱,哪里贵了? "\
    "有的时候找找自己原因，好不好，这么多年了工资涨没涨，有没有认真工作，好不？"


@limiter.limit(settings.rate_limit)
def limit_when_not_login(request: Request):
    """
    Limit when not login
    """


@router.post("/api/chatgpt")
async def chatgpt(
        request: Request,
        prompt_body: PromptBody,
):
    limit_when_not_login(request)

    prompt = prompt_body.prompt

    _logger.info(
        f"Request from {get_real_ipaddr(request)}, prompt={prompt}"
    )
    if any(w in prompt for w in STOP_WORDS):
        raise HTTPException(
            status_code=403,
            detail="Prompt contains stop words"
        )
    if len(prompt) > PROMPT_MAX_LENGTH:
        raise HTTPException(
            status_code=403,
            detail="Prompt is too long"
        )

    def get_openai_generator():
        openai_stream = openai.ChatCompletion.create(
            model=settings.model,
            max_tokens=1000,
            temperature=0.9,
            top_p=1,
            stream=True,
            messages=[
                {
                    "role": "system",
                    "content": PROMPT
                },
                {"role": "user", "content": prompt}
            ]
        )
        for event in openai_stream:
            if "content" in event["choices"][0].delta:
                current_response = event["choices"][0].delta.content
                yield f"data: {json.dumps(current_response)}\n\n"

    return StreamingResponse(get_openai_generator(), media_type='text/event-stream')
