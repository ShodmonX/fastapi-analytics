# generate_fake_events_single.py
import asyncio
import random
import httpx
import time
from datetime import datetime

API_URL = "http://localhost:8080/analytics/"
TOTAL_EVENTS = 100_000
CONCURRENCY = 50
TIMEOUT = 1000

EVENT_TYPES = [
    "login", "logout", "signup",
    "post_create", "post_view", "post_like", "post_share",
    "comment_create", "comment_like",
    "app_open", "app_background", "session_start",
    "page_view_home", "page_view_profile",
    "screen_view_dashboard", "profile_update",
    "search", "notification_click",
    "onboarding_step_1_completed", "subscription_start"
]

USER_IDS = list(range(1, 5001))

def create_event():
    user_id = random.choices(
        USER_IDS,
        weights=[100 if i < 50 else 10 if i < 500 else 1 for i in range(len(USER_IDS))],
        k=1
    )[0]
    event_type = random.choice(EVENT_TYPES)
    return {"user_id": user_id, "event_type": event_type}

async def send_one_event(client: httpx.AsyncClient, semaphore: asyncio.Semaphore):
    async with semaphore:
        event = create_event()
        try:
            r = await client.post(
                API_URL,
                json=event,
                headers={"Content-Type": "application/json"},
                timeout=20
            )
            if r.status_code == 201:
                return True
            else:
                print(f"Xato {r.status_code}: {r.text}")
                return False
        except Exception as e:
            print(f"Request xatosi: {e} → {event}")

async def main():
    print(f"{TOTAL_EVENTS} ta event yuborilmoqda... (parallel: {CONCURRENCY})")
    start_time = time.time()

    semaphore = asyncio.Semaphore(CONCURRENCY)
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        tasks = [
            send_one_event(client, semaphore)
            for _ in range(TOTAL_EVENTS)
        ]
        await asyncio.gather(*tasks)

    duration = time.time() - start_time
    print(f"\nTUGADI!")
    print(f"→ {TOTAL_EVENTS} ta event yuborildi")
    print(f"→ Vaqt: {duration:.1f} sekund")
    print(f"→ Oʻrtacha: {TOTAL_EVENTS/duration:,.0f} event/sekund")

if __name__ == "__main__":
    asyncio.run(main())