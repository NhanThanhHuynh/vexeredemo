1. Quy ước code style

Ngôn ngữ: Python 3.10+

Style: tuân theo PEP8

Tên biến/hàm: snake_case (vd: get_booking_core).

Tên class: PascalCase.

Hằng số: UPPER_CASE.

Comment & Docstring:

Sử dụng docstring cho tất cả public function.

Comment ngắn gọn, tập trung vào “tại sao” thay vì “làm gì”.

Imports:

Nhóm theo chuẩn: built-in → third-party → local.

Tránh import *.

Line length: ≤ 100 ký tự.

Logging/Debug: dùng print() cho POC, có thể thay bằng logging khi production.

2. Kiểm thử & CI
2.1. Tầng kiểm thử

Unit test:

search_faq_core() (FAQ).

get_booking_core() và change_booking_core() (Booking).

handle_booking_flow() (multi-turn).

Integration test:

Orchestrator gọi các service core function.

E2E test:

Manual CLI (user nhập text → bot trả lời).

Mock test:

OCR/Voice stub trả về giá trị giả lập.

2.2. Continuous Integration

Công cụ: pytest + coverage.

Pipeline:

Khi push lên GitHub → GitHub Actions chạy pytest -v.

Có thể bổ sung check code style (flake8 hoặc black).

Báo cáo:

Coverage report để track độ bao phủ test.

Fail-fast nếu có test không pass.

3. Điểm còn hạn chế & hướng mở rộng
3.1. Hạn chế

Intent classification: phụ thuộc LLM (OpenAI) → nếu mất mạng/timeout thì fallback chưa mạnh.

Booking DB: chỉ mock data, chưa kết nối với hệ thống thực.

OCR/Voice: mới ở mức stub, chưa dùng dịch vụ thật.

State machine: lưu state trong RAM → không hỗ trợ multi-user, không scale ngang.

3.2. Hướng mở rộng

Scalability: lưu state vào Redis hoặc DB → hỗ trợ nhiều người dùng đồng thời.

Model:

Dùng hybrid search (BM25 + FAISS) để cải thiện chất lượng FAQ.

Train intent classifier riêng để giảm phụ thuộc API.

Service integration:

OCR thực (Tesseract/Google Vision API).

STT/TTS thực (Google Speech, Whisper).

Tích hợp Payment Gateway cho booking flow.

Multi-language: hỗ trợ song ngữ (VN/EN).

Deployment: Dockerize, deploy lên cloud (AWS/GCP).