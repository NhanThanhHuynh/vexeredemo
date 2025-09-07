# VexereDemo Chatbot

Hệ thống chatbot hỗ trợ các chức năng:

* **FAQ**: Tra cứu câu hỏi thường gặp từ CSV.
* **Booking**: Xem vé, đổi vé, đặt vé theo từng bước.
* **OCR**: Ảnh vé → mã vé.
* **Voice**: Âm thanh → text → intent.

---

## 1. Yêu cầu môi trường

* Python 3.10+ (đã test với Python 3.12.10)

### Tạo virtual environment

```bash
python -m venv vexeredemo

# Linux / Mac
source vexeredemo/bin/activate

# Windows
vexeredemo\Scripts\activate
```

### Cài dependencies

```bash
pip install -r requirements.txt
```

---

## 2. Chuẩn bị dữ liệu

* FAQ CSV: `data/faq_data.csv`

---

## 3. Cấu trúc thư mục

```
vexeredemo/
│── orchestrator/
│   └── app.py             # Orchestrator CLI
│── tools/
│   ├── rag_server.py      # FAQ search (FAISS)
│   ├── booking_server.py  # Mock booking API
│   ├── ocr_server.py      # OCR stub
│   └── speech_server.py   # Voice stub
│── tests/
│   └── test_orchestrator.py  # Unit & flow tests
│── data/
│   └── faq_data.csv       # FAQ sample data
│── README.md
│── requirements.txt
```

---

## 4. Cấu hình OpenAI API

Chatbot cần LLM để phân loại intent.
Cấu hình API key trong `app.py`:

```python
openai.api_key = "sk-xxxxx"
```

---

## 5. Chạy demo CLI

### Khởi động MCP server:

```bash
python ../tools/rag_server.py
python ../tools/booking_server.py
```

### Khởi động chatbot:

```bash
python ../orchestrator/app.py
```

### Ví dụ tương tác

```
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
```

---

## 6. Chạy test

Chạy toàn bộ test với pytest:

```bash
pytest -v ../tests/test_orchestrator.py
```

---

## 7. Mở rộng

* Thay stub OCR/Voice bằng dịch vụ thực tế (Tesseract OCR, Google Speech).
* Triển khai Flask/FastAPI để expose REST API thay cho CLI.
* Thay FAISS bằng ElasticSearch khi dữ liệu lớn.