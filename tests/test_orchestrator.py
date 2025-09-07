import pytest

# Import từ orchestrator/app.py
from orchestrator import app

# Import core services trực tiếp từ tools
from tools.rag_server import search_faq_core
from tools.booking_server import get_booking_core, change_booking_core
from tools.ocr_server import extract_ticket_info_core
from tools.speech_server import transcribe_audio_core


@pytest.mark.asyncio
async def test_faq_flow():
    intent = await app.classify_intent("Hành lý bao nhiêu ký?")
    assert intent == "FAQ"

    resp = search_faq_core("Hành lý bao nhiêu ký?", k=1)
    assert "hành lý" in resp["results"][0]["question"].lower()


@pytest.mark.asyncio
async def test_get_and_change_booking():
    intent = await app.classify_intent("Cho tôi xem vé BK123")
    assert intent == "GET_BOOKING"

    booking = get_booking_core("BK123")
    assert booking["code"] == "BK123"

    intent2 = await app.classify_intent("Tôi muốn đổi giờ vé")
    assert intent2 == "CHANGE_BOOKING"

    resp = change_booking_core("BK123", "2025-09-12 10:00")
    assert resp["msg"] == "changed"


@pytest.mark.asyncio
async def test_book_ticket_flow():
    user_id = "test_user"
    app.USER_STATE[user_id] = "BOOK_TICKET"

    step1 = await app.handle_booking_flow(user_id, "Tôi muốn đặt vé")
    assert "ngày" in step1

    step2 = await app.handle_booking_flow(user_id, "2025-09-15")
    assert "tuyến" in step2

    step3 = await app.handle_booking_flow(user_id, "SG-HN")
    assert "ghế" in step3

    step4 = await app.handle_booking_flow(user_id, "A12")
    assert "thanh toán" in step4

    step5 = await app.handle_booking_flow(user_id, "momo")
    assert "Vé đã được đặt" in step5


def test_ocr_stub():
    resp = extract_ticket_info_core("ticket_BK123.png")
    assert resp["booking_code"] == "BK123"


def test_voice_stub():
    resp = transcribe_audio_core("sample.wav")
    assert isinstance(resp, str)
    assert "đổi" in resp.lower()