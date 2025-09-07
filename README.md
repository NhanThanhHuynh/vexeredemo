Hệ thống chatbot hỗ trợ:

FAQ (tra cứu câu hỏi thường gặp từ CSV).

Booking (xem vé, đổi vé, đặt vé theo từng bước).

OCR (ảnh vé → mã vé).

Voice (âm thanh → text → intent).

2. Yêu cầu môi trường

Python 3.10+ (đã test với Python 3.12.10).

Tạo virtual env:

python -m venv vexeredemo
source vexeredemo/bin/activate   # Linux/Mac
vexeredemo\Scripts\activate      # Windows

Hoặc sử dụng môi trường đã tạo sẵn : 
.\Scripts\activate #Windows

Cài dependencies:

pip install -r requirements.txt

3. Chuẩn bị dữ liệu

FAQ CSV: data/faq_data.csv

4. Cấu trúc thư mục
vexeredemo/
│── orchestrator/
│   └── app.py             # Orchestrator CLI
│── tools/
│   ├── rag_server.py      # FAQ search (FAISS)
│   ├── booking_server.py  # Mock booking API
│   ├── ocr_server.py      # OCR stub
│   └── speech_server.py   # Voice stub
│── tests/
│   └── test_orchestrator.py       # Unit & flow tests
│── data/
│   └── faq_data.csv       # FAQ sample data
│── README.md
│── requirements.txt

5. Cấu hình OpenAI API

Chatbot cần LLM để phân loại intent.

Cấu hình API key trong file app.py:
openai.api_key ="sk-xxxxx"

6. Chạy demo CLI

Khởi động MCP server:

python ../tools/rag_server.py
python ../tools/booking_server.py

Khởi động chatbot:

python ../orchestrator/app.py

Ví dụ
User: Hành lý bao nhiêu ký?
Bot: Quý khách có thể mang theo ... (từ: Hành lý xách tay bao nhiêu kg?)

User: Cho tôi xem vé BK123
Bot: {'code': 'BK123', 'route': 'SG-HN', 'start_time': '2025-09-10 08:00', 'fare': 500000}

User: Tôi muốn đặt vé
Bot: Bạn muốn đi ngày nào?

User: 2025-09-15
Bot: Bạn muốn đi tuyến nào? (VD: SG-HN, SG-DN)

User: SG-HN
Bot: Bạn muốn chọn ghế nào?

User: A12
Bot: Bạn muốn thanh toán bằng cách nào? (momo, visa, tiền mặt)

User: momo
Bot: ✅ Vé đã được đặt thành công!
Chi tiết: {'date': '2025-09-15', 'route': 'SG-HN', 'seat': 'A12', 'payment': 'momo'}

7. Chạy test

Chạy toàn bộ test với pytest:

pytest -v ../tests/test_orchestrator.py

8. Mở rộng

Có thể thay stub OCR/Voice bằng dịch vụ thực tế (Tesseract OCR, Google Speech).

Triển khai Flask/FastAPI để expose REST API thay cho CLI.

Thay FAISS bằng ElasticSearch khi dữ liệu lớn.
