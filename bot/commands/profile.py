import io
import os

# import time
import aiohttp
import discord
from PIL import Image, ImageDraw, ImageFont

from db.session import SessionLocal
from services.user_service import get_user

BG_DIR = os.getenv("BG_DIR")
DEFAULT_BG = "gamerz_zone.jpg"
# DEFAULT_BG = "francesca_prelati.jpeg"
CARD_W, CARD_H = 1920, 1080

FONT_DIR = "/usr/share/fonts/OTF"
FONT_BIG = ImageFont.truetype(f"{FONT_DIR}/Poppins-Bold.otf", 64)
FONT_MED = ImageFont.truetype(f"{FONT_DIR}/Poppins-Regular.otf", 40)
FONT_SMALL = ImageFont.truetype(f"{FONT_DIR}/Poppins-Light.otf", 30)

AVATAR_SIZE = 280
RING_SIZE = AVATAR_SIZE + 10
UPSCALE = 4


async def fetch_avatar(url: str) -> Image.Image:
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as r:
            data = await r.read()
    return Image.open(io.BytesIO(data)).convert("RGBA")


def make_circle_aa(img: Image.Image, size: int) -> Image.Image:
    big = size * UPSCALE
    img = img.resize((big, big), Image.Resampling.BILINEAR)
    mask = Image.new("L", (big, big), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, big, big), fill=255)
    result = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    result.paste(img, (0, 0), mask)
    return result.resize((size, size), Image.Resampling.LANCZOS)


def make_ring_aa(size: int) -> Image.Image:
    big = size * UPSCALE
    ring = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse((0, 0, big, big), fill=(255, 255, 255, 220))
    return ring.resize((size, size), Image.Resampling.LANCZOS)


def draw_text_shadow(draw, pos, text, font, fill, shadow=(0, 0, 0, 180), offset=2):
    x, y = pos
    draw.text((x + offset, y + offset), text, font=font, fill=shadow)
    draw.text((x, y), text, font=font, fill=fill)


async def build_profile_card(
    user, discord_user: discord.Member | discord.User
) -> io.BytesIO:
    # t = time.perf_counter()

    active_bg = next((b for b in user.backgrounds if b.is_active), None)
    bg_file = active_bg.background.bg_url if active_bg else DEFAULT_BG
    bg_path = os.path.join(BG_DIR, bg_file)

    card = Image.open(bg_path).convert("RGB").convert("RGBA")
    # print(f"[profile] bg load: {time.perf_counter() - t:.3f}s")

    # t2 = time.perf_counter()
    avatar_img = await fetch_avatar(str(discord_user.display_avatar.with_size(256).url))
    # print(f"[profile] avatar fetch: {time.perf_counter() - t2:.3f}s")

    # t3 = time.perf_counter()
    draw = ImageDraw.Draw(card)

    ring = make_ring_aa(RING_SIZE)
    avatar_circle = make_circle_aa(avatar_img, AVATAR_SIZE)

    ring_x = CARD_W - RING_SIZE - 60
    ring_y = CARD_H - RING_SIZE - 60
    card.paste(ring, (ring_x, ring_y), ring)
    card.paste(avatar_circle, (ring_x + 5, ring_y + 5), avatar_circle)

    pad = 60
    text_y = CARD_H - 240
    draw_text_shadow(
        draw, (pad, text_y), user.username, FONT_BIG, fill=(255, 255, 255, 255)
    )
    text_y += 80
    draw_text_shadow(
        draw,
        (pad, text_y),
        user.bio or "No bio set.",
        FONT_MED,
        fill=(220, 220, 220, 255),
    )
    text_y += 55
    draw_text_shadow(
        draw,
        (pad, text_y),
        user.registered_at.strftime("Joined %B %d, %Y"),
        FONT_SMALL,
        fill=(180, 180, 180, 255),
    )
    # print(f"[profile] drawing: {time.perf_counter() - t3:.3f}s")

    # t4 = time.perf_counter()
    buf = io.BytesIO()
    card.convert("RGB").save(buf, format="JPEG", quality=85)
    buf.seek(0)
    # print(f"[profile] encode+save: {time.perf_counter() - t4:.3f}s")
    # print(f"[profile] total: {time.perf_counter() - t:.3f}s")

    return buf


async def handle_profile(message: discord.Message, args: list[str]):
    async with SessionLocal() as session:
        user = await get_user(session, message.author.id)

    if not user:
        await message.channel.send(
            f"{message.author.mention} you are not registered. Use `register` first."
        )
        return

    async with message.channel.typing():
        buf = await build_profile_card(user, message.author)
        await message.channel.send(file=discord.File(buf, filename="profile.jpg"))
