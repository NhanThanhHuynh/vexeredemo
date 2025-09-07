import re

def extract_ticket_info_core(image_path: str) -> dict:
    match = re.search(r"(BK\d+)", image_path)
    if match:
        return {"booking_code": match.group(1), "status": "mocked"}
    return {"error": "no booking code detected"}