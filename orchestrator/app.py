import os, asyncio
import openai
from tools.rag_server import search_faq_core
from tools.booking_server import get_booking_core, change_booking_core
from tools.ocr_server import extract_ticket_info_core
from tools.speech_server import transcribe_audio_core

openai.api_key = "sk-xxxxx" # Thay bằng API key của bạn
BOOKING_FLOW = {}
USER_STATE = {}

async def classify_intent(user_msg: str) -> str:
    if not openai.api_key:
        raise RuntimeError("⚠️ OPENAI_API_KEY chưa được cấu hình!")

    try:
        resp = await openai.ChatCompletion.acreate(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Bạn là bộ phân loại intent. "
                        "Luôn trả về đúng 1 intent duy nhất trong danh sách: "
                        "[FAQ, GET_BOOKING, CHANGE_BOOKING, BOOK_TICKET, UNKNOWN]. "
                        "Trả về đúng chữ, không kèm giải thích."
                    )
                },
                {"role": "user", "content": user_msg}
            ]
        )
        content = resp.choices[0].message["content"].strip().upper()
        return content
    except Exception as e:
        print("⚠️ OpenAI error:", e)
        return "UNKNOWN"

async def handle_booking_flow(user_id: str, msg: str) -> str:
    """
    Dẫn dắt quy trình đặt vé từng bước:
    0. Bắt đầu
    1. Hỏi ngày
    2. Hỏi tuyến
    3. Hỏi ghế
    4. Hỏi thanh toán
    5. Xác nhận
    """
    state = BOOKING_FLOW.get(user_id, {"step": 0, "data": {}})
    step = state["step"]
    data = state["data"]

    if step == 0:
        state["step"] = 1
        BOOKING_FLOW[user_id] = state
        return "Bạn muốn đi ngày nào?"

    elif step == 1:
        data["date"] = msg
        state["step"] = 2
        return "Bạn muốn đi tuyến nào? (VD: SG-HN, SG-DN)"

    elif step == 2:
        data["route"] = msg
        state["step"] = 3
        return "Bạn muốn chọn ghế nào?"

    elif step == 3:
        data["seat"] = msg
        state["step"] = 4
        return "Bạn muốn thanh toán bằng cách nào? (momo, visa, tiền mặt)"

    elif step == 4:
        data["payment"] = msg
        state["step"] = 5
        BOOKING_FLOW[user_id] = {"step": 0, "data": {}}
        return f"✅ Vé đã được đặt thành công!\nChi tiết: {data}"

    return "Quy trình đặt vé đã hoàn tất hoặc có lỗi."

async def main():
    user_id = "cli" 
    while True:
        user_input = input("User: ")

        if user_input.endswith(".jpg") or user_input.endswith(".png"):
            info = extract_ticket_info_core(user_input)
            print("Bot OCR:", info)
            continue

        if user_input.endswith(".wav"):
            text = transcribe_audio_core(user_input)
            print("Bot (from voice):", text)
            user_input = text
        
        if USER_STATE.get(user_id) == "BOOK_TICKET":
            resp = await handle_booking_flow(user_id, user_input)
            print("Bot:", resp)
            if "Vé đã được đặt" in resp:
                USER_STATE[user_id] = None
            continue


        intent = await classify_intent(user_input)

        if intent == "FAQ":
            resp = search_faq_core(user_input, k=1)
            top = resp["results"][0]
            print("Bot:", top["answer"], f"(từ: {top['question']})")

        elif intent == "GET_BOOKING":
            print("Bot:", get_booking_core("BK123"))

        elif intent == "CHANGE_BOOKING":
            print("Bot:", change_booking_core("BK123", "2025-09-11 09:00"))

        elif intent == "BOOK_TICKET":
            USER_STATE[user_id] = "BOOK_TICKET"
            resp = await handle_booking_flow(user_id, user_input)
            print("Bot:", resp)

        else:
            print("Bot: Xin lỗi, tôi chưa hiểu.")

if __name__ == "__main__":
    asyncio.run(main())
