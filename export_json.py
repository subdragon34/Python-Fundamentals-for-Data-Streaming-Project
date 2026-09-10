import json

from main import EVENTS


with open("events.json", "w", encoding="utf-8") as file:
    json.dump(EVENTS, file, indent=2, ensure_ascii=False)

print(f"Exported {len(EVENTS)} events to events.json")
