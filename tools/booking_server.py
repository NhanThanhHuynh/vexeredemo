from fastmcp import FastMCP
from datetime import datetime

mcp = FastMCP("BookingTool")

BOOKINGS = {
    "BK123": {
        "code": "BK123",
        "route": "SG-HN",
        "start_time": "2025-09-10 08:00",
        "changeable_until": "2025-09-09 08:00",
        "fare": 500000
    }
}

# ✅ Core
def get_booking_core(code: str):
    return BOOKINGS.get(code) or {"error": "not found"}

def change_booking_core(code: str, new_time: str):
    b = BOOKINGS.get(code)
    if not b:
        return {"error": "not found"}
    if datetime.now() > datetime.fromisoformat(b["changeable_until"]):
        return {"error": "window closed"}
    b["start_time"] = new_time
    return {"msg": "changed", "new_time": new_time}

# MCP tool wrapper
@mcp.tool()
def get_booking(code: str) -> dict:
    return get_booking_core(code)

@mcp.tool()
def change_booking(code: str, new_time: str) -> dict:
    return change_booking_core(code, new_time)

if __name__ == "__main__":
    mcp.run()
