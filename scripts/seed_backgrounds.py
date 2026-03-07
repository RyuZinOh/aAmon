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

RARITIES = ["common", "rare", "epic", "legendary"]


def prompt_details(filename: str) -> dict:
    default_name = os.path.splitext(filename)[0].replace("_", " ").title()
    print(f"\n--- {filename} ---")

    name = input(f"  Name [{default_name}]: ").strip() or default_name
    lore = input(f"  Lore [leave blank to skip]: ").strip() or None

    print(f"  Rarity options: {', '.join(RARITIES)}")
    while True:
        rarity = input(f"  Rarity [common]: ").strip().lower() or "common"
        if rarity in RARITIES:
            break
        print(f"  Invalid rarity. Choose from: {', '.join(RARITIES)}")

    return {"name": name, "lore": lore, "rarity": rarity}


async def seed():
    files = [
        f for f in os.listdir(BG_DIR) if os.path.splitext(f)[1].lower() in SUPPORTED
    ]

    if not files:
        print(f"No images found in {BG_DIR}")
        return

    async with SessionLocal() as session:
        for filename in files:
            existing = await session.execute(
                select(Background).where(Background.bg_url == filename)
            )
            if existing.scalar_one_or_none():
                print(f"  skipping {filename} (already in DB)")
                continue

            details = prompt_details(filename)
            bg = Background(
                bg_url=filename,
                bg_name=details["name"],
                bg_lore=details["lore"],
                bg_rarity=details["rarity"],
                release_date=date.today(),
            )
            session.add(bg)
            print(f"  added {filename} → {details['name']} ({details['rarity']})")

        await session.commit()
        print("\nDone.")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
