#!/usr/bin/env python3
"""Render a 1024x1024 editorial world-news front page for Monday 23 November 2026."""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MAP_SRC = "/root/.gemini/antigravity-cli/brain/e8365f43-e797-414e-b87a-4acbad1d4b9c/editorial_world_map_1795408939613.jpg"
OUT_PNG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
PREVIEW_300 = "/tmp/news-20261123-preview-300.png"

# System TrueType fonts (Liberation Serif, Sans, Mono)
F_SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
F_SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
F_SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
F_SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"
F_MONO_B = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# Palette: warm archival editorial paper + crisp ink + distinct regional accents
BG = (246, 243, 235)         # #F6F3EB broadsheet ivory
CARD_BG = (255, 254, 250)    # #FFFEFA card white-ivory
CARD_BORDER = (214, 207, 192)
NAVY = (17, 24, 39)          # #111827 masthead & footer ink
INK = (17, 24, 39)           # #111827 primary text
MUTED = (55, 65, 81)         # #374151 crisp body text (higher contrast!)
SRC_CLR = (100, 110, 124)
GOLD = (217, 148, 36)
GOLD_LIGHT = (254, 243, 199)

# 6 distinct regional accent colors
C_MARKET = (29, 78, 216)     # cobalt blue (Markets / East Asia)
C_EUROPE = (185, 28, 28)     # crimson (Europe & Climate Diplomacy)
C_MENA = (180, 83, 9)        # burnt amber (Middle East & North Africa)
C_AFRICA = (15, 118, 110)    # deep teal (Africa & Public Health)
C_SASIA = (79, 70, 229)      # indigo (South & Southeast Asia)
C_AMERICAS = (4, 120, 87)    # emerald (Americas & Sport)


def wrap_text(draw, text, fnt, max_w):
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        cand = w if not cur else cur + " " + w
        if draw.textlength(cand, font=fnt) <= max_w:
            cur = cand
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_badge(draw, cx, cy, num, color, r=10, font_size=11):
    draw.ellipse((cx - r - 1.8, cy - r - 1.8, cx + r + 1.8, cy + r + 1.8), fill=(255, 255, 255))
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=color)
    f = font(F_SANS_B, font_size)
    s = str(num)
    bbox = draw.textbbox((0, 0), s, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw / 2 - bbox[0], cy - th / 2 - bbox[1]), s, fill=(255, 255, 255), font=f)


def draw_pill(draw, x, y, text, bg, fg=(255, 255, 255), size=11, pad_x=7, pad_y=3):
    f = font(F_SANS_B, size)
    bbox = draw.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    w = int(tw + pad_x * 2)
    h = int(th + pad_y * 2)
    draw.rounded_rectangle((x, y, x + w, y + h), radius=3, fill=bg)
    draw.text((x + pad_x - bbox[0], y + pad_y - bbox[1]), text, fill=fg, font=f)
    return w, h


def build_image():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # ---------------------------------------------------------------- 1. MASTHEAD (y: 0..86)
    draw.rectangle((0, 0, W, 86), fill=NAVY)
    draw.rectangle((0, 82, W, 86), fill=GOLD)

    draw.text((20, 11), "THE WORLD TODAY", fill=(255, 253, 248), font=font(F_SERIF_B, 39))
    draw.text(
        (22, 58),
        "ONE DAY IN 7 REGIONS  ·  MARKETS  ·  DIPLOMACY  ·  CONFLICT  ·  CLIMATE  ·  HEALTH  ·  SPORT",
        fill=(203, 213, 225),
        font=font(F_SANS_R, 12),
    )

    # Prominent high-contrast date plate (legible even at 300px)
    draw.rounded_rectangle((652, 13, W - 18, 72), radius=5, fill=(30, 41, 59), outline=GOLD, width=2)
    draw.text((670, 18), "MONDAY", fill=GOLD, font=font(F_SANS_B, 13))
    draw.text((670, 35), "23 NOVEMBER 2026", fill=(255, 255, 255), font=font(F_SERIF_B, 25))

    # ---------------------------------------------------------------- 2. HERO BAND (y: 94..408)
    hero_y0, hero_y1 = 94, 408
    map_x0, map_x1 = 16, 594
    lead_x0, lead_x1 = 606, W - 16

    # Left: Editorial World Map frame
    draw.rounded_rectangle((map_x0, hero_y0, map_x1, hero_y1), radius=6, fill=CARD_BG, outline=CARD_BORDER, width=1)
    map_raw = Image.open(MAP_SRC).convert("RGB")
    mw, mh = map_raw.size
    crop_box = (int(mw * 0.03), int(mh * 0.05), int(mw * 0.97), int(mh * 0.95))
    map_crop = map_raw.crop(crop_box)
    target_mw = (map_x1 - map_x0) - 8
    target_mh = (hero_y1 - hero_y0) - 32
    map_resized = map_crop.resize((target_mw, target_mh), Image.Resampling.LANCZOS)
    img.paste(map_resized, (map_x0 + 4, hero_y0 + 28))

    # Map title bar
    draw.rectangle((map_x0 + 1, hero_y0 + 1, map_x1 - 1, hero_y0 + 27), fill=(238, 233, 222))
    draw.line((map_x0, hero_y0 + 27, map_x1, hero_y0 + 27), fill=CARD_BORDER, width=1)
    draw.text(
        (map_x0 + 10, hero_y0 + 6),
        "GLOBAL FLASHPOINTS  ·  23 NOVEMBER 2026  (12 STORIES MAPPED)",
        fill=INK,
        font=font(F_SANS_B, 11.5),
    )

    # 12 cleanly separated, geographically calibrated numbered pins (1-to-1 with stories)
    mx, my = map_x0 + 4, hero_y0 + 28
    pins = [
        (1, 0.870, 0.390, C_MARKET),    # 1: Tokyo / Asian AI tech rout
        (2, 0.568, 0.285, C_EUROPE),    # 2: Kyiv / Ukraine strikes & talks
        (3, 0.568, 0.375, C_EUROPE),    # 3: Antalya, Turkey (COP31 collapse fallout)
        (4, 0.515, 0.245, C_EUROPE),    # 4: Poland / Eastern Baltic (Sparta II)
        (5, 0.530, 0.425, C_MENA),      # 5: Benghazi, Libya (corvette Merkury)
        (6, 0.635, 0.450, C_MENA),      # 6: Strait of Hormuz / Riyadh
        (7, 0.565, 0.555, C_AFRICA),    # 7: Khartoum, Sudan & Ituri, DR Congo
        (8, 0.492, 0.535, C_AFRICA),    # 8: Abuja, Nigeria (Africa Space Forum)
        (9, 0.822, 0.375, C_MARKET),    # 9: Seoul, South Korea & Taipei
        (10, 0.715, 0.455, C_SASIA),    # 10: New Delhi / Nepal & Bangladesh
        (11, 0.785, 0.555, C_SASIA),    # 11: Bangkok, Thailand & Banten, Indonesia
        (12, 0.220, 0.390, C_AMERICAS), # 12: US, Sinaloa Mexico & Edmonton Canada
    ]
    for num, fx, fy, clr in pins:
        px = int(mx + fx * target_mw)
        py = int(my + fy * target_mh)
        draw_badge(draw, px, py, num, clr, r=10, font_size=11)

    # Right: Top 2 Lead Story Cards
    leads = [
        {
            "num": 1,
            "tag": "LEAD · GLOBAL MARKETS & AI",
            "color": C_MARKET,
            "headline": "AI Tech Rout Sweeps Asia; Nikkei Drops 5%",
            "body": "Asian chipmakers tumbled Monday after the S&P 500 entered a 10%+ correction and the Nasdaq erased 2026 gains. Tokyo's Nikkei fell to ~56,437 while Seoul and Taipei prepared stabilization measures.",
            "source": "Reuters · Washington Post · Trading Economics",
        },
        {
            "num": 2,
            "tag": "LEAD · EUROPE & UKRAINE WAR",
            "color": C_EUROPE,
            "headline": "Strike Near Kyiv Kills 12; New Talks Set",
            "body": "A Russian airstrike hit housing near Kyiv as grid damage forced Odesa schools online. The Kremlin set fresh US-Russia-Ukraine talks post-Shenzhen; ship Sparta II burned in the Baltic.",
            "source": "The Guardian · Washington Post · RFE/RL",
        },
    ]

    lead_h = (hero_y1 - hero_y0 - 10) // 2
    for idx, ld in enumerate(leads):
        y0 = hero_y0 + idx * (lead_h + 10)
        y1 = y0 + lead_h
        draw.rounded_rectangle((lead_x0, y0, lead_x1, y1), radius=6, fill=CARD_BG, outline=CARD_BORDER, width=1)
        draw.rectangle((lead_x0, y0 + 6, lead_x0 + 5, y1 - 6), fill=ld["color"])

        draw_badge(draw, lead_x0 + 22, y0 + 20, ld["num"], ld["color"], r=10, font_size=11)
        draw_pill(draw, lead_x0 + 38, y0 + 10, ld["tag"], ld["color"], size=10.5, pad_x=7, pad_y=3)

        f_lh = font(F_SERIF_B, 17.5)
        h_lines = wrap_text(draw, ld["headline"], f_lh, (lead_x1 - lead_x0) - 26)
        cy = y0 + 35
        for ln in h_lines:
            draw.text((lead_x0 + 15, cy), ln, fill=INK, font=f_lh)
            cy += 21

        f_lb = font(F_SANS_R, 12.5)
        b_lines = wrap_text(draw, ld["body"], f_lb, (lead_x1 - lead_x0) - 26)
        cy += 3
        for ln in b_lines[:4]:
            draw.text((lead_x0 + 15, cy), ln, fill=MUTED, font=f_lb)
            cy += 16.5

        draw.text((lead_x0 + 15, y1 - 19), ld["source"], fill=SRC_CLR, font=font(F_SANS_I, 10.5))

    # ---------------------------------------------------------------- 3. REGIONAL GRID (3x2 cards, y: 418..968)
    grid_y0 = 418
    grid_gap_x = 12
    grid_gap_y = 12
    card_w = (W - 32 - 2 * grid_gap_x) // 3  # 322 px
    card_h = 269

    cards = [
        {
            "region": "EUROPE & CLIMATE DIPLOMACY",
            "color": C_EUROPE,
            "stories": [
                (3, "Fallout After COP31 Collapses",
                 "Capitals reacted Monday after UN climate talks in Antalya ended without a pact Sunday — the first COP breakdown since 2009 — as EU, African & Latin American blocs rejected weak fossil-fuel terms.",
                 "The Guardian · UN · CBS News"),
                (4, "Baltic Ship Fire & Poland Plots",
                 "Finnish and Estonian crews battled a fire on Russian cargo vessel Sparta II after a reported drone hit; Poland confirmed Russian plots against a rapper on Polish and Danish soil.",
                 "Al Jazeera · CNN · Taipei Times"),
            ],
        },
        {
            "region": "MIDDLE EAST & NORTH AFRICA",
            "color": C_MENA,
            "stories": [
                (5, "Russian Corvette Hit in Benghazi",
                 "Suspected Ukrainian naval drones struck the Russian corvette Merkury docked at Benghazi, Libya, reportedly sinking it with several dead; a Maltese-flagged vessel was also hit offshore.",
                 "Al Jazeera · CNN"),
                (6, "Hormuz Tanker Alerts; Soft Crude",
                 "IRGC claimed actions against tankers near the Strait of Hormuz while Saudi defenses intercepted projectiles near Riyadh; crude oil edged lower on global tech-driven demand fears.",
                 "Al Jazeera · Reuters"),
            ],
        },
        {
            "region": "AFRICA & PUBLIC HEALTH",
            "color": C_AFRICA,
            "stories": [
                (7, "Khartoum UN Hit; WHO DRC Plea",
                 "Heavy drone strikes hit residential areas and a UN site in Khartoum, Sudan. In DR Congo's Ituri province, WHO urged peace as clashes trapped Ebola staff for 24+ hours.",
                 "Al Jazeera · Inquirer"),
                (8, "Abuja Hosts Africa Space Forum",
                 "Delegates convene in Abuja for ASEICC 2026 (Nov 24–27) as Africa's $22B+ space sector expands domestic satellite engineering, Earth observation, and Africa2Moon lunar plans.",
                 "African Leadership · Aerospace"),
            ],
        },
        {
            "region": "EAST ASIA & MARKETS",
            "color": C_MARKET,
            "stories": [
                (9, "S. Korea Minister Quits Over AI",
                 "Education Minister Choi Kyo-jin resigned Monday amid public outrage over AI-assisted cheating scandals surrounding South Korea's national CSAT college entrance exam.",
                 "AP · Regional Wire"),
                (1, "Seoul & Taipei Ready Backstops",
                 "After sharp losses in Samsung, SK Hynix, and Taiwan's Taiex from the global AI valuation unwind, authorities eased share-buyback rules and readied stabilization funds.",
                 "Focus Taiwan · Investing.com"),
            ],
        },
        {
            "region": "SOUTH & SOUTHEAST ASIA",
            "color": C_SASIA,
            "stories": [
                (10, "Modi-Shah Talks; Dhaka Protests",
                 "Indian PM Narendra Modi and visiting Nepal PM Balendra Shah discussed cross-border power grids; garment worker wage clashes along Gazipur highways shut factories in Bangladesh.",
                 "India Today · Al Jazeera"),
                (11, "Thai Verdict & Banten Plant Fire",
                 "Thailand's Appeal Court prepared its lèse-majesté ruling on MP Rukchanok Srinork; Indonesian crews searched for dozens missing after a Banten confectionery plant blaze.",
                 "Thai Enquirer · Al Jazeera"),
            ],
        },
        {
            "region": "AMERICAS & SPORT",
            "color": C_AMERICAS,
            "stories": [
                (12, "US Rate Fears; Cartel Boss Held",
                 "Sticky US inflation lifted Treasury yields and Fed rate anxiety ahead of Thanksgiving. Elite Mexican forces arrested an FBI-wanted Beltrán Leyva cartel leader in Sinaloa.",
                 "The Hill · Washington Post"),
                (None, "Edmonton Elks Win Grey Cup",
                 "The Edmonton Elks defeated the Montreal Alouettes to capture the CFL Grey Cup championship, capping the Canadian football season.",
                 "AP · Sports Wire"),
            ],
        },
    ]

    f_reg = font(F_SANS_B, 12.5)
    f_sh = font(F_SERIF_B, 15.5)
    f_sb = font(F_SANS_R, 12.2)
    f_ss = font(F_SANS_I, 10.5)

    for idx, card in enumerate(cards):
        col = idx % 3
        row = idx // 3
        x0 = 16 + col * (card_w + grid_gap_x)
        y0 = grid_y0 + row * (card_h + grid_gap_y)
        x1 = x0 + card_w
        y1 = y0 + card_h

        draw.rounded_rectangle((x0, y0, x1, y1), radius=6, fill=CARD_BG, outline=CARD_BORDER, width=1)
        draw.rounded_rectangle((x0, y0, x1, y0 + 27), radius=6, fill=card["color"])
        draw.rectangle((x0, y0 + 14, x1, y0 + 27), fill=card["color"])
        draw.text((x0 + 10, y0 + 6), card["region"], fill=(255, 255, 255), font=f_reg)

        cy = y0 + 35
        for s_idx, (num, headline, body, src) in enumerate(card["stories"]):
            if s_idx > 0:
                draw.line((x0 + 10, cy, x1 - 10, cy), fill=(228, 222, 210), width=1)
                cy += 8

            if num is not None:
                draw_badge(draw, x0 + 20, cy + 9, num, card["color"], r=9, font_size=10.5)
                hx = x0 + 34
                hw = card_w - 44
            else:
                draw.ellipse((x0 + 15, cy + 5, x0 + 23, cy + 13), fill=card["color"])
                hx = x0 + 29
                hw = card_w - 39

            h_lines = wrap_text(draw, headline, f_sh, hw)
            for li, ln in enumerate(h_lines[:2]):
                draw.text((hx if li == 0 else x0 + 11, cy), ln, fill=INK, font=f_sh)
                cy += 18.5

            cy += 2
            b_lines = wrap_text(draw, body, f_sb, card_w - 22)
            for ln in b_lines[:5]:
                draw.text((x0 + 11, cy), ln, fill=MUTED, font=f_sb)
                cy += 15.2

            draw.text((x0 + 11, cy + 1), src, fill=SRC_CLR, font=f_ss)
            cy += 18

    # ---------------------------------------------------------------- 4. BOTTOM DATA TICKER (y: 976..1024)
    draw.rectangle((0, 976, W, H), fill=NAVY)
    draw.rectangle((0, 976, W, 979), fill=GOLD)
    draw.text(
        (18, 985),
        "NIKKEI ~56,437 (-5%)  |  S&P 500 CORRECTION (-10%+)  |  EUR/USD 1.096  |  COP31: NO PACT  |  23 NOV 2026",
        fill=GOLD_LIGHT,
        font=font(F_MONO_B, 11),
    )
    draw.text(
        (18, 1004),
        "Monday 23 November 2026 world summary  ·  Sources: Reuters, AP, BBC, The Guardian, Al Jazeera, Washington Post, UN, Focus Taiwan",
        fill=(156, 163, 175),
        font=font(F_SANS_R, 10.5),
    )

    img.save(OUT_PNG, format="PNG", optimize=True)
    size_kb = os.path.getsize(OUT_PNG) / 1024
    print(f"Wrote {OUT_PNG}: {W}x{H}, {size_kb:.1f} KiB")

    img.resize((300, 300), Image.Resampling.LANCZOS).save(PREVIEW_300, format="PNG")
    print(f"Wrote 300px preview: {PREVIEW_300}")


if __name__ == "__main__":
    build_image()
