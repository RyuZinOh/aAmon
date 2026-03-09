import asyncio
import os
import sys
from datetime import date

from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

ASYNC_DB_URL = os.getenv("ASYNC_DB_URL")
BG_DIR = os.getenv("BG_DIR")
SUPPORTED = {".jpg", ".jpeg", ".png", ".webp"}

engine = create_async_engine(ASYNC_DB_URL, echo=False)  # type: ignore
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

from db.models import Background


def cost_to_rarity(cost: int) -> str:
    if cost <= 500:
        return "common"
    elif cost <= 1500:
        return "rare"
    elif cost <= 3000:
        return "epic"
    else:
        return "legendary"


def prompt_details(filename: str) -> dict:
    default_name = os.path.splitext(filename)[0].replace("_", " ").title()
    print(f"\n--- {filename} ---")

    name = input(f"Name [{default_name}]: ").strip() or default_name
    lore = input(f"Lore [leave blank to skip]: ").strip() or None

    while True:
        try:
            cost = int(input(f"Balance: ").strip() or 100)
            if cost >= 0:
                break
            print("Cost must be 0 or more.")
        except ValueError:
            print("Enter a valid number.")

    rarity = cost_to_rarity(cost)
    print(f"  Rarity auto-set to: {rarity}")

    return {"name": name, "lore": lore, "cost": cost, "rarity": rarity}


async def update_prices(session: AsyncSession):
    result = await session.execute(select(Background))
    bgs = result.scalars().all()

    if not bgs:
        print("No backgrounds found.")
        return

    print("\n=== Update existing background prices ===")
    for bg in bgs:
        print(
            f"\n[{bg.bg_id}] {bg.bg_name} — current cost: {bg.bg_cost} ({bg.bg_rarity})"
        )
        raw = input(f"New cost [leave blank to skip]: ").strip()
        if not raw:
            continue
        try:
            cost = int(raw)
            bg.bg_cost = cost
            bg.bg_rarity = cost_to_rarity(cost)
            print(f"Updated → {cost} Chronux ({bg.bg_rarity})")
        except ValueError:
            print("Invalid, skipping.")

    await session.commit()
    print("\nPrices updated.")


async def seed():
    files = [
        f for f in os.listdir(BG_DIR) if os.path.splitext(f)[1].lower() in SUPPORTED
    ]

    async with SessionLocal() as session:
        print("1) Seed new backgrounds")
        print("2) Update existing prices")
        choice = input("\nChoice [1]: ").strip() or "1"

        if choice == "2":
            await update_prices(session)
        else:
            if not files:
                print(f"No images found in {BG_DIR}")
                return

            for filename in files:
                existing = await session.execute(
                    select(Background).where(Background.bg_url == filename)
                )
                if existing.scalar_one_or_none():
                    print(f"skipping {filename} (already in DB)")
                    continue

                details = prompt_details(filename)
                bg = Background(
                    bg_url=filename,
                    bg_name=details["name"],
                    bg_lore=details["lore"],
                    bg_rarity=details["rarity"],
                    bg_cost=details["cost"],
                    release_date=date.today(),
                )
                session.add(bg)
                print(
                    f"added {filename} → {details['name']} ({details['rarity']}, {details['cost']} Chronux)"
                )

            await session.commit()
            print("\nDone.")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
