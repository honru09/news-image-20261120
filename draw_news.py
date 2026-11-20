#!/usr/bin/env python3
"""
draw_news.py - Generate 1024x1024 front-page newspaper infographic
for make.fun competition news-image-20261120.
Date: Friday, 20 November 2026
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions
WIDTH = 1024
HEIGHT = 1024
SCALE = 2  # 2x supersampling for crisp anti-aliasing
W = WIDTH * SCALE
H = HEIGHT * SCALE

FONTS_DIR = "/usr/share/fonts/truetype/dejavu"
FONT_BOLD_PATH = os.path.join(FONTS_DIR, "DejaVuSans-Bold.ttf")
FONT_REG_PATH = os.path.join(FONTS_DIR, "DejaVuSans.ttf")

def get_font(path, size):
    return ImageFont.truetype(path, int(size * SCALE))

def wrap_text(text, font, max_width, draw):
    """Wrap text to fit within max_width (in scaled coords)."""
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def draw_rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def draw_lead_motif(draw, cx, cy, radius):
    """
    Diplomatic motif: Stylized globe with coordinates, golden laurel wreath,
    and 3 national shields (USA, China, Russia) centered below.
    """
    r = radius
    # Soft background circular halo
    draw.ellipse([cx - r - 12*SCALE, cy - r - 12*SCALE, cx + r + 12*SCALE, cy + r + 12*SCALE],
                 fill=(241, 245, 249))

    # Globe ocean circle (Deep slate navy)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                 fill=(15, 23, 42), outline=(30, 58, 138), width=int(2.5 * SCALE))

    # Latitudes
    for r_lat in [0.38, 0.72]:
        ry = int(r * r_lat)
        draw.ellipse([cx - r, cy - ry, cx + r, cy + ry],
                     outline=(59, 130, 246), width=int(1.5 * SCALE))
    # Equator & Prime Meridian
    draw.line([cx - r, cy, cx + r, cy], fill=(96, 165, 250), width=int(2 * SCALE))
    draw.line([cx, cy - r, cx, cy + r], fill=(96, 165, 250), width=int(2 * SCALE))

    # Longitude arcs
    for r_lon in [0.42, 0.78]:
        rx = int(r * r_lon)
        draw.ellipse([cx - rx, cy - r, cx + rx, cy + r],
                     outline=(59, 130, 246), width=int(1.5 * SCALE))

    # Laurel wreath leaves around globe
    for angle_deg in range(-125, 130, 22):
        rad = math.radians(angle_deg)
        lx = cx + int((r + 14 * SCALE) * math.sin(rad))
        ly = cy + int((r + 14 * SCALE) * math.cos(rad))
        draw.ellipse([lx - 5 * SCALE, ly - 3 * SCALE, lx + 5 * SCALE, ly + 3 * SCALE],
                     fill=(217, 119, 6))

    # 3 Diplomatic Shields (USA, China, Russia)
    shield_w = int(22 * SCALE)
    shield_h = int(26 * SCALE)
    shield_y = cy + int(r * 0.44)

    # 1. USA Shield (Left)
    sx = cx - int(38 * SCALE)
    draw.rounded_rectangle([sx - shield_w//2, shield_y, sx + shield_w//2, shield_y + shield_h],
                           radius=int(3 * SCALE), fill=(220, 38, 38), outline=(255, 255, 255), width=int(1.5 * SCALE))
    draw.line([sx - shield_w//2 + 2, shield_y + shield_h//2, sx + shield_w//2 - 2, shield_y + shield_h//2],
              fill=(255, 255, 255), width=int(2.5 * SCALE))
    draw.rounded_rectangle([sx - shield_w//2, shield_y, sx, shield_y + shield_h//2],
                           radius=int(2 * SCALE), fill=(30, 58, 138))
    draw.ellipse([sx - shield_w//4 - 2*SCALE, shield_y + shield_h//4 - 2*SCALE,
                  sx - shield_w//4 + 2*SCALE, shield_y + shield_h//4 + 2*SCALE], fill=(255, 255, 255))

    # 2. China Shield (Center - slightly taller)
    sx = cx
    cw = int(24 * SCALE)
    ch = int(28 * SCALE)
    cy_shield = shield_y - int(3 * SCALE)
    draw.rounded_rectangle([sx - cw//2, cy_shield, sx + cw//2, cy_shield + ch],
                           radius=int(4 * SCALE), fill=(220, 38, 38), outline=(255, 255, 255), width=int(1.5 * SCALE))
    # Center gold star
    draw.ellipse([sx - 4*SCALE, cy_shield + ch//3 - 4*SCALE,
                  sx + 4*SCALE, cy_shield + ch//3 + 4*SCALE], fill=(250, 204, 21))

    # 3. Russia Shield (Right)
    sx = cx + int(38 * SCALE)
    draw.rounded_rectangle([sx - shield_w//2, shield_y, sx + shield_w//2, shield_y + shield_h],
                           radius=int(3 * SCALE), fill=(255, 255, 255), outline=(203, 213, 225), width=int(1.5 * SCALE))
    draw.rectangle([sx - shield_w//2, shield_y + shield_h//3, sx + shield_w//2, shield_y + 2*shield_h//3],
                   fill=(37, 99, 235))
    draw.rectangle([sx - shield_w//2, shield_y + 2*shield_h//3, sx + shield_w//2, shield_y + shield_h],
                   fill=(220, 38, 38))

    # Label underneath motif
    font_motif = get_font(FONT_BOLD_PATH, 9.5)
    motif_lbl = "SHENZHEN APEC 2026"
    bbox_m = draw.textbbox((0, 0), motif_lbl, font=font_motif)
    mw = bbox_m[2] - bbox_m[0]
    draw.text((cx - mw//2, cy + r + int(18 * SCALE)), motif_lbl, font=font_motif, fill=(100, 116, 139))

def draw_scales_icon(draw, bx, by, bw, bh):
    """Scales of Justice Icon."""
    cx = bx + bw // 2
    cy = by + bh // 2
    # Base
    draw.line([cx - 15 * SCALE, cy + 15 * SCALE, cx + 15 * SCALE, cy + 15 * SCALE], fill=(15, 23, 42), width=int(2.5 * SCALE))
    # Post
    draw.line([cx, cy - 16 * SCALE, cx, cy + 15 * SCALE], fill=(15, 23, 42), width=int(2.5 * SCALE))
    draw.ellipse([cx - 3 * SCALE, cy - 19 * SCALE, cx + 3 * SCALE, cy - 13 * SCALE], fill=(15, 23, 42))
    # Crossbeam
    draw.line([cx - 18 * SCALE, cy - 9 * SCALE, cx + 18 * SCALE, cy - 9 * SCALE], fill=(15, 23, 42), width=int(2.5 * SCALE))
    # Left Pan
    draw.line([cx - 18 * SCALE, cy - 9 * SCALE, cx - 24 * SCALE, cy + 3 * SCALE], fill=(100, 116, 139), width=int(1.5 * SCALE))
    draw.line([cx - 18 * SCALE, cy - 9 * SCALE, cx - 12 * SCALE, cy + 3 * SCALE], fill=(100, 116, 139), width=int(1.5 * SCALE))
    draw.arc([cx - 25 * SCALE, cy, cx - 11 * SCALE, cy + 8 * SCALE], 0, 180, fill=(185, 28, 28), width=int(2 * SCALE))
    draw.line([cx - 25 * SCALE, cy + 4 * SCALE, cx - 11 * SCALE, cy + 4 * SCALE], fill=(185, 28, 28), width=int(1.5 * SCALE))
    # Right Pan
    draw.line([cx + 18 * SCALE, cy - 9 * SCALE, cx + 12 * SCALE, cy + 3 * SCALE], fill=(100, 116, 139), width=int(1.5 * SCALE))
    draw.line([cx + 18 * SCALE, cy - 9 * SCALE, cx + 24 * SCALE, cy + 3 * SCALE], fill=(100, 116, 139), width=int(1.5 * SCALE))
    draw.arc([cx + 11 * SCALE, cy, cx + 25 * SCALE, cy + 8 * SCALE], 0, 180, fill=(185, 28, 28), width=int(2 * SCALE))
    draw.line([cx + 11 * SCALE, cy + 4 * SCALE, cx + 25 * SCALE, cy + 4 * SCALE], fill=(185, 28, 28), width=int(1.5 * SCALE))

def draw_bridge_icon(draw, bx, by, bw, bh):
    """Crimea Bridge & Rail Icon."""
    cx = bx + bw // 2
    cy = by + bh // 2
    # Water lines
    draw.line([bx + 4 * SCALE, cy + 15 * SCALE, bx + bw - 4 * SCALE, cy + 15 * SCALE], fill=(59, 130, 246), width=int(2 * SCALE))
    draw.line([bx + 8 * SCALE, cy + 18 * SCALE, bx + bw - 8 * SCALE, cy + 18 * SCALE], fill=(147, 197, 253), width=int(1.5 * SCALE))
    # Bridge deck / roadbed
    draw.line([bx + 4 * SCALE, cy + 5 * SCALE, bx + bw - 4 * SCALE, cy + 5 * SCALE], fill=(15, 23, 42), width=int(2.5 * SCALE))
    # Rail track ties
    for rx in range(bx + 8 * SCALE, bx + bw - 8 * SCALE, 5 * SCALE):
        draw.line([rx, cy + 3 * SCALE, rx, cy + 7 * SCALE], fill=(245, 158, 11), width=int(1.5 * SCALE))
    # Arch
    draw.arc([cx - 20 * SCALE, cy - 16 * SCALE, cx + 20 * SCALE, cy + 12 * SCALE], 180, 360, fill=(185, 28, 28), width=int(2.5 * SCALE))
    # Suspension cables
    for ox in [-12, -6, 0, 6, 12]:
        draw.line([cx + ox * SCALE, cy - 8 * SCALE, cx + ox * SCALE, cy + 5 * SCALE], fill=(148, 163, 184), width=int(1 * SCALE))
    # Piers
    draw.line([cx - 16 * SCALE, cy + 5 * SCALE, cx - 16 * SCALE, cy + 15 * SCALE], fill=(15, 23, 42), width=int(2 * SCALE))
    draw.line([cx + 16 * SCALE, cy + 5 * SCALE, cx + 16 * SCALE, cy + 15 * SCALE], fill=(15, 23, 42), width=int(2 * SCALE))

def draw_tanker_icon(draw, bx, by, bw, bh):
    """Oil Tanker Ship Icon."""
    cx = bx + bw // 2
    cy = by + bh // 2
    # Water
    draw.line([bx + 4 * SCALE, cy + 14 * SCALE, bx + bw - 4 * SCALE, cy + 14 * SCALE], fill=(59, 130, 246), width=int(2 * SCALE))
    # Tanker Hull
    hull = [
        (bx + 6 * SCALE, cy + 3 * SCALE),
        (bx + bw - 8 * SCALE, cy + 3 * SCALE),
        (bx + bw - 14 * SCALE, cy + 13 * SCALE),
        (bx + 11 * SCALE, cy + 13 * SCALE)
    ]
    draw.polygon(hull, fill=(30, 41, 59), outline=(15, 23, 42))
    # Stern superstructure
    draw.rectangle([bx + 8 * SCALE, cy - 8 * SCALE, bx + 18 * SCALE, cy + 3 * SCALE], fill=(225, 29, 72), outline=(15, 23, 42), width=int(1.5 * SCALE))
    draw.rectangle([bx + 11 * SCALE, cy - 14 * SCALE, bx + 15 * SCALE, cy - 8 * SCALE], fill=(15, 23, 42))
    # Oil cargo tanks
    for tx in [bx + 23 * SCALE, bx + 31 * SCALE, bx + 39 * SCALE]:
        draw.rectangle([tx, cy - 2 * SCALE, tx + 5 * SCALE, cy + 3 * SCALE], fill=(100, 116, 139))
    # Warning flame
    draw.polygon([
        (bx + bw - 12 * SCALE, cy - 4 * SCALE),
        (bx + bw - 7 * SCALE, cy - 12 * SCALE),
        (bx + bw - 9 * SCALE, cy - 3 * SCALE),
        (bx + bw - 3 * SCALE, cy - 9 * SCALE),
        (bx + bw - 7 * SCALE, cy + 2 * SCALE)
    ], fill=(234, 88, 12))

def draw_stock_icon(draw, bx, by, bw, bh):
    """Stock Chart Icon for Anthropic IPO."""
    cx = bx + bw // 2
    cy = by + bh // 2
    # Shaded area under the curve
    poly_pts = [
        (bx + 6 * SCALE, cy + 14 * SCALE),
        (bx + 6 * SCALE, cy + 10 * SCALE),
        (bx + 16 * SCALE, cy + 6 * SCALE),
        (bx + 26 * SCALE, cy - 6 * SCALE),
        (bx + 34 * SCALE, cy - 16 * SCALE),
        (bx + bw - 6 * SCALE, cy - 10 * SCALE),
        (bx + bw - 6 * SCALE, cy + 14 * SCALE)
    ]
    draw.polygon(poly_pts, fill=(236, 253, 245))
    # Coordinate grid lines
    draw.line([bx + 5 * SCALE, cy - 15 * SCALE, bx + 5 * SCALE, cy + 15 * SCALE], fill=(203, 213, 225), width=int(1.5 * SCALE))
    draw.line([bx + 5 * SCALE, cy + 15 * SCALE, bx + bw - 5 * SCALE, cy + 15 * SCALE], fill=(203, 213, 225), width=int(1.5 * SCALE))
    # Trend line
    line_pts = [
        (bx + 6 * SCALE, cy + 10 * SCALE),
        (bx + 16 * SCALE, cy + 6 * SCALE),
        (bx + 26 * SCALE, cy - 6 * SCALE),
        (bx + 34 * SCALE, cy - 16 * SCALE),
        (bx + bw - 6 * SCALE, cy - 10 * SCALE)
    ]
    for i in range(len(line_pts) - 1):
        draw.line([line_pts[i], line_pts[i+1]], fill=(16, 185, 129), width=int(2.5 * SCALE))
    # Peak dot
    end_pt = line_pts[-1]
    draw.ellipse([end_pt[0] - 3*SCALE, end_pt[1] - 3*SCALE, end_pt[0] + 3*SCALE, end_pt[1] + 3*SCALE], fill=(5, 150, 105))

def draw_skyscraper_icon(draw, bx, by, bw, bh):
    """PIF Tower Skyscraper Icon."""
    cx = bx + bw // 2
    cy = by + bh // 2
    # Ground
    draw.line([bx + 6 * SCALE, cy + 16 * SCALE, bx + bw - 6 * SCALE, cy + 16 * SCALE], fill=(15, 23, 42), width=int(2 * SCALE))
    # Crystalline faceted tower outline
    tower_pts = [
        (cx - 10 * SCALE, cy + 16 * SCALE),
        (cx - 9 * SCALE, cy - 5 * SCALE),
        (cx - 3 * SCALE, cy - 20 * SCALE),
        (cx, cy - 24 * SCALE),
        (cx + 3 * SCALE, cy - 20 * SCALE),
        (cx + 9 * SCALE, cy - 5 * SCALE),
        (cx + 10 * SCALE, cy + 16 * SCALE)
    ]
    draw.polygon(tower_pts, fill=(15, 23, 42), outline=(30, 41, 59))
    # Facet lines
    draw.line([cx, cy - 24 * SCALE, cx, cy + 16 * SCALE], fill=(51, 65, 85), width=int(1.5 * SCALE))
    draw.line([cx - 3 * SCALE, cy - 20 * SCALE, cx - 10 * SCALE, cy + 16 * SCALE], fill=(71, 85, 105), width=int(1 * SCALE))
    draw.line([cx + 3 * SCALE, cy - 20 * SCALE, cx + 10 * SCALE, cy + 16 * SCALE], fill=(71, 85, 105), width=int(1 * SCALE))
    # Damaged floors marker (red/orange highlighted band across 7-8 floors)
    dam_y = cy - 3 * SCALE
    draw.rectangle([cx - 8 * SCALE, dam_y, cx + 8 * SCALE, dam_y + 6 * SCALE], fill=(239, 68, 68))
    # Antenna
    draw.line([cx, cy - 24 * SCALE, cx, cy - 30 * SCALE], fill=(15, 23, 42), width=int(1.5 * SCALE))

def generate_newspaper():
    img = Image.new("RGB", (W, H), color=(248, 250, 252))
    draw = ImageDraw.Draw(img)

    # Fonts
    font_masthead = get_font(FONT_BOLD_PATH, 42)
    font_edition = get_font(FONT_BOLD_PATH, 11)
    font_date = get_font(FONT_BOLD_PATH, 14)
    
    font_tag = get_font(FONT_BOLD_PATH, 10)
    font_lead_title = get_font(FONT_BOLD_PATH, 24)
    font_lead_body = get_font(FONT_REG_PATH, 14)
    font_lead_callout = get_font(FONT_BOLD_PATH, 11)

    font_sec_title = get_font(FONT_BOLD_PATH, 16.5)
    font_sec_body = get_font(FONT_REG_PATH, 12.5)
    font_sec_stat = get_font(FONT_BOLD_PATH, 10)

    font_footer = get_font(FONT_BOLD_PATH, 12)

    # -------------------------------------------------------------
    # 1. MASTHEAD BANNER (Top y: 0 to 82)
    # -------------------------------------------------------------
    masthead_h = int(82 * SCALE)
    draw.rectangle([0, 0, W, masthead_h], fill=(15, 23, 42))  # Slate-900

    # Crimson accent line (4px)
    draw.rectangle([0, masthead_h, W, masthead_h + int(4 * SCALE)], fill=(185, 28, 28))

    pad_x = int(28 * SCALE)
    draw.text((pad_x, int(16 * SCALE)), "WORLD NEWS", font=font_masthead, fill=(255, 255, 255))
    
    edition_text = "INTERNATIONAL EDITION"
    date_text = "FRIDAY, 20 NOVEMBER 2026"
    
    bbox_ed = draw.textbbox((0, 0), edition_text, font=font_edition)
    ed_w = bbox_ed[2] - bbox_ed[0]
    draw.text((W - pad_x - ed_w, int(18 * SCALE)), edition_text, font=font_edition, fill=(148, 163, 184))

    bbox_date = draw.textbbox((0, 0), date_text, font=font_date)
    date_w = bbox_date[2] - bbox_date[0]
    draw.text((W - pad_x - date_w, int(38 * SCALE)), date_text, font=font_date, fill=(248, 250, 252))

    # -------------------------------------------------------------
    # 2. LEAD STORY BLOCK
    # y: 98 to 354 (height 256px)
    # -------------------------------------------------------------
    lead_y = int(98 * SCALE)
    lead_h = int(256 * SCALE)
    lead_w = W - 2 * pad_x
    card_r = int(8 * SCALE)

    # Lead Card Background & Border
    draw_rounded_rect(draw, [pad_x, lead_y, pad_x + lead_w, lead_y + lead_h], radius=card_r,
                      fill=(255, 255, 255), outline=(203, 213, 225), width=int(2 * SCALE))

    # Crimson left border accent
    draw.rounded_rectangle([pad_x, lead_y, pad_x + int(6 * SCALE), lead_y + lead_h],
                           radius=int(3 * SCALE), fill=(185, 28, 28))

    content_x = pad_x + int(24 * SCALE)
    text_max_w = lead_w - int(240 * SCALE)

    # Lead Tag Badge
    tag_bg = [content_x, lead_y + int(14 * SCALE), content_x + int(235 * SCALE), lead_y + int(35 * SCALE)]
    draw.rounded_rectangle(tag_bg, radius=int(4 * SCALE), fill=(254, 242, 242), outline=(252, 165, 165), width=int(1 * SCALE))
    draw.text((content_x + int(8 * SCALE), lead_y + int(16 * SCALE)),
              "★ HISTORIC SUMMIT • SHENZHEN", font=font_tag, fill=(153, 27, 27))

    # Lead Headline
    lead_hl = "Trump, Xi and Putin Issue Joint 'Declaration Toward Peace'"
    hl_lines = wrap_text(lead_hl, font_lead_title, text_max_w, draw)
    cur_y = lead_y + int(44 * SCALE)
    for line in hl_lines:
        draw.text((content_x, cur_y), line, font=font_lead_title, fill=(15, 23, 42))
        cur_y += int(30 * SCALE)

    # Lead Summary
    summary_text = (
        "In their first-ever trilateral summit on the APEC sidelines, the leaders signed a landmark "
        "accord affirming 'a nuclear war cannot be won and must never be fought.' The declaration "
        "establishes a dialogue on reducing nuclear risks, while omitting the wars in Ukraine and Iran."
    )
    sum_lines = wrap_text(summary_text, font_lead_body, text_max_w, draw)
    cur_y += int(4 * SCALE)
    for line in sum_lines:
        draw.text((content_x, cur_y), line, font=font_lead_body, fill=(51, 65, 85))
        cur_y += int(20 * SCALE)

    # Key takeaway callout bar
    callout_y = lead_y + lead_h - int(38 * SCALE)
    callout_rect = [content_x, callout_y, content_x + text_max_w, callout_y + int(26 * SCALE)]
    draw.rounded_rectangle(callout_rect, radius=int(4 * SCALE), fill=(241, 245, 249), outline=(226, 232, 240), width=int(1 * SCALE))
    callout_str = "KEY PLEDGE: Nuclear risk dialogue established • UN reform & energy supplies pledged • APEC concludes"
    draw.text((content_x + int(10 * SCALE), callout_y + int(5 * SCALE)), callout_str, font=font_lead_callout, fill=(30, 41, 59))

    # Drawn Motif (Globe + Laurel + 3 Shields)
    motif_cx = pad_x + lead_w - int(108 * SCALE)
    motif_cy = lead_y + lead_h // 2 - int(6 * SCALE)
    draw_lead_motif(draw, motif_cx, motif_cy, radius=int(54 * SCALE))

    # -------------------------------------------------------------
    # 3. SECONDARY STORIES - ROW 1 (3 Cards)
    # y: 368 to 660 (height 292px)
    # -------------------------------------------------------------
    row1_y = int(368 * SCALE)
    row1_h = int(292 * SCALE)
    gap1 = int(14 * SCALE)
    card1_w = (lead_w - 2 * gap1) // 3

    cards_r1 = [
        {
            "tag": "THE HAGUE • ICJ RULING",
            "tag_color": (153, 27, 27),
            "tag_bg": (254, 242, 242),
            "tag_border": (252, 165, 165),
            "headline_lines": [
                "World Court Rules Myanmar",
                "Committed Rohingya Genocide"
            ],
            "summary": "In an unprecedented 9-6 verdict, the ICJ held Myanmar responsible for the 2017 genocide killing ~10,000, ordering legal reforms and reparations.",
            "stat": "ICJ VERDICT: 9-6 VOTE • REPARATIONS ORDERED",
            "icon_func": draw_scales_icon
        },
        {
            "tag": "CRIMEA • BLACK SEA",
            "tag_color": (30, 58, 138),
            "tag_bg": (239, 246, 255),
            "tag_border": (191, 219, 254),
            "headline_lines": [
                "Ukraine Strikes Crimea Rail",
                "Bridge; Putin Vows Retaliation"
            ],
            "summary": "A third strike this week damaged the rail section. In Shenzhen, Putin ruled out any Black Sea or energy truce, warning of a 'far more painful' response.",
            "stat": "KERCH CROSSING: RAIL HIT • TRUCE REJECTED",
            "icon_func": draw_bridge_icon
        },
        {
            "tag": "GULF CONFLICT • HORMUZ",
            "tag_color": (194, 65, 12),
            "tag_bg": (255, 247, 237),
            "tag_border": (254, 215, 170),
            "headline_lines": [
                "Tankers Hit Off Hormuz as",
                "Iran Strikes Kuwait Base"
            ],
            "summary": "Iran said 3 tankers struck naval mines; UKMTO reported a projectile hit. Tehran fired drones at a US base in Kuwait after US strikes on Qeshm Island.",
            "stat": "HORMUZ: 3 TANKERS HIT • RETALIATION REPORTED",
            "icon_func": draw_tanker_icon
        }
    ]

    for i, cdata in enumerate(cards_r1):
        cx0 = pad_x + i * (card1_w + gap1)
        cx1 = cx0 + card1_w
        draw_rounded_rect(draw, [cx0, row1_y, cx1, row1_y + row1_h], radius=card_r,
                          fill=(255, 255, 255), outline=(203, 213, 225), width=int(2 * SCALE))
        
        c_pad = int(14 * SCALE)
        inner_w = card1_w - 2 * c_pad
        
        # Header Row: Tag pill (Left) + Icon box (Right)
        icon_box_size = int(42 * SCALE)
        icon_bx = cx1 - c_pad - icon_box_size
        icon_by = row1_y + c_pad
        draw.rounded_rectangle([icon_bx, icon_by, icon_bx + icon_box_size, icon_by + icon_box_size],
                               radius=int(6 * SCALE), fill=(248, 250, 252), outline=(226, 232, 240), width=int(1.5 * SCALE))
        cdata["icon_func"](draw, icon_bx, icon_by, icon_box_size, icon_box_size)

        # Tag badge pill
        tag_w = inner_w - icon_box_size - int(10 * SCALE)
        draw.rounded_rectangle([cx0 + c_pad, row1_y + c_pad + int(8 * SCALE),
                                cx0 + c_pad + tag_w, row1_y + c_pad + int(32 * SCALE)],
                               radius=int(4 * SCALE), fill=cdata["tag_bg"], outline=cdata["tag_border"], width=int(1 * SCALE))
        draw.text((cx0 + c_pad + int(8 * SCALE), row1_y + c_pad + int(13 * SCALE)),
                  cdata["tag"], font=font_tag, fill=cdata["tag_color"])

        # Headline (Guaranteed balanced 2 lines)
        cur_cy = row1_y + c_pad + icon_box_size + int(10 * SCALE)
        for line in cdata["headline_lines"]:
            draw.text((cx0 + c_pad, cur_cy), line, font=font_sec_title, fill=(15, 23, 42))
            cur_cy += int(22 * SCALE)

        # Separator line
        cur_cy += int(4 * SCALE)
        draw.line([cx0 + c_pad, cur_cy, cx1 - c_pad, cur_cy], fill=(241, 245, 249), width=int(1.5 * SCALE))
        cur_cy += int(6 * SCALE)

        # Summary
        sum_lines = wrap_text(cdata["summary"], font_sec_body, inner_w, draw)
        for line in sum_lines:
            draw.text((cx0 + c_pad, cur_cy), line, font=font_sec_body, fill=(51, 65, 85))
            cur_cy += int(17 * SCALE)

        # Bottom stat chip (guaranteed to fit without clipping)
        stat_y = row1_y + row1_h - int(34 * SCALE)
        chip_rect = [cx0 + c_pad, stat_y, cx1 - c_pad, stat_y + int(24 * SCALE)]
        draw.rounded_rectangle(chip_rect, radius=int(4 * SCALE), fill=(241, 245, 249), outline=(226, 232, 240), width=int(1 * SCALE))
        
        # Center stat text horizontally inside chip
        bbox_st = draw.textbbox((0, 0), cdata["stat"], font=font_sec_stat)
        st_w = bbox_st[2] - bbox_st[0]
        st_x = cx0 + c_pad + (inner_w - st_w) // 2
        draw.text((st_x, stat_y + int(5 * SCALE)), cdata["stat"], font=font_sec_stat, fill=(71, 85, 105))

    # -------------------------------------------------------------
    # 4. SECONDARY STORIES - ROW 2 (2 Wider Cards)
    # y: 674 to 966 (height 292px)
    # -------------------------------------------------------------
    row2_y = int(674 * SCALE)
    row2_h = int(292 * SCALE)
    gap2 = int(16 * SCALE)
    card2_w = (lead_w - gap2) // 2

    cards_r2 = [
        {
            "tag": "MARKETS • RECORD TECH IPO",
            "tag_color": (5, 150, 105),
            "tag_bg": (236, 253, 245),
            "tag_border": (167, 243, 208),
            "headline_lines": [
                "Anthropic Raises Record $81.3B",
                "in Historic Nasdaq Debut"
            ],
            "summary": "In the largest IPO on record, Anthropic priced 980M shares at $83, opened at $111.50, and closed at $97.17 (+17%), achieving a ~$1.5T fully diluted valuation while broader US stocks slipped 2%.",
            "badges": [
                ("NASDAQ: ANT", "$97.17 (+17%)"),
                ("RECORD IPO", "$81.3B RAISED")
            ],
            "icon_func": draw_stock_icon
        },
        {
            "tag": "MIDDLE EAST • SECURITY",
            "tag_color": (185, 28, 28),
            "tag_bg": (254, 242, 242),
            "tag_border": (252, 165, 165),
            "headline_lines": [
                "Houthi Strike Hits PIF Tower,",
                "Riyadh's Tallest Skyscraper"
            ],
            "summary": "A missile and drone attack shattered windows across 7-8 floors of the 385-meter PIF Tower, the sovereign wealth fund HQ and Riyadh's tallest building. Saudi officials confirmed zero casualties.",
            "badges": [
                ("PIF TOWER", "7-8 FLOORS HIT"),
                ("CASUALTIES", "ZERO REPORTED")
            ],
            "icon_func": draw_skyscraper_icon
        }
    ]

    for i, cdata in enumerate(cards_r2):
        cx0 = pad_x + i * (card2_w + gap2)
        cx1 = cx0 + card2_w
        draw_rounded_rect(draw, [cx0, row2_y, cx1, row2_y + row2_h], radius=card_r,
                          fill=(255, 255, 255), outline=(203, 213, 225), width=int(2 * SCALE))
        
        c_pad = int(16 * SCALE)
        inner_w = card2_w - 2 * c_pad

        # Header: Tag badge + Icon box
        icon_box_size = int(46 * SCALE)
        icon_bx = cx1 - c_pad - icon_box_size
        icon_by = row2_y + c_pad
        draw.rounded_rectangle([icon_bx, icon_by, icon_bx + icon_box_size, icon_by + icon_box_size],
                               radius=int(6 * SCALE), fill=(248, 250, 252), outline=(226, 232, 240), width=int(1.5 * SCALE))
        cdata["icon_func"](draw, icon_bx, icon_by, icon_box_size, icon_box_size)

        # Tag badge pill
        tag_w = inner_w - icon_box_size - int(12 * SCALE)
        draw.rounded_rectangle([cx0 + c_pad, row2_y + c_pad + int(8 * SCALE),
                                cx0 + c_pad + tag_w, row2_y + c_pad + int(34 * SCALE)],
                               radius=int(4 * SCALE), fill=cdata["tag_bg"], outline=cdata["tag_border"], width=int(1 * SCALE))
        draw.text((cx0 + c_pad + int(8 * SCALE), row2_y + c_pad + int(14 * SCALE)),
                  cdata["tag"], font=font_tag, fill=cdata["tag_color"])

        # Headline (Guaranteed balanced 2 lines)
        cur_cy = row2_y + c_pad + icon_box_size + int(10 * SCALE)
        for line in cdata["headline_lines"]:
            draw.text((cx0 + c_pad, cur_cy), line, font=font_sec_title, fill=(15, 23, 42))
            cur_cy += int(22 * SCALE)

        # Divider
        cur_cy += int(4 * SCALE)
        draw.line([cx0 + c_pad, cur_cy, cx1 - c_pad, cur_cy], fill=(241, 245, 249), width=int(1.5 * SCALE))
        cur_cy += int(6 * SCALE)

        # Summary
        sum_lines = wrap_text(cdata["summary"], font_sec_body, inner_w, draw)
        for line in sum_lines:
            draw.text((cx0 + c_pad, cur_cy), line, font=font_sec_body, fill=(51, 65, 85))
            cur_cy += int(17 * SCALE)

        # Bottom stat boxes (two pills side by side, centered and guaranteed to fit)
        stat_y = row2_y + row2_h - int(34 * SCALE)
        pill_w = (inner_w - int(10 * SCALE)) // 2
        for p_idx, (b_label, b_val) in enumerate(cdata["badges"]):
            px0 = cx0 + c_pad + p_idx * (pill_w + int(10 * SCALE))
            draw.rounded_rectangle([px0, stat_y, px0 + pill_w, stat_y + int(24 * SCALE)],
                                   radius=int(4 * SCALE), fill=(241, 245, 249), outline=(226, 232, 240), width=int(1 * SCALE))
            badge_str = f"{b_label} • {b_val}"
            bbox_b = draw.textbbox((0, 0), badge_str, font=font_sec_stat)
            bw_txt = bbox_b[2] - bbox_b[0]
            bx_pos = px0 + (pill_w - bw_txt) // 2
            draw.text((bx_pos, stat_y + int(5 * SCALE)), badge_str, font=font_sec_stat, fill=(71, 85, 105))

    # -------------------------------------------------------------
    # 5. FOOTER BAR
    # y: 986 to 1024 (height 38px)
    # -------------------------------------------------------------
    foot_y = int(986 * SCALE)
    draw.rectangle([0, foot_y, W, H], fill=(15, 23, 42))
    
    footer_text = "Compiled from public reporting — 20 November 2026"
    bbox_foot = draw.textbbox((0, 0), footer_text, font=font_footer)
    foot_w = bbox_foot[2] - bbox_foot[0]
    draw.text(((W - foot_w) // 2, foot_y + int(10 * SCALE)), footer_text, font=font_footer, fill=(203, 213, 225))

    # -------------------------------------------------------------
    # 6. RESAMPLE & SAVE
    # -------------------------------------------------------------
    out_img = img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    out_path = os.path.join(os.path.dirname(__file__), "entry.png")
    out_img.save(out_path, format="PNG", optimize=True)
    print(f"Saved {out_path} ({WIDTH}x{HEIGHT})")

if __name__ == "__main__":
    generate_newspaper()
