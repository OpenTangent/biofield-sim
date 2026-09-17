import os
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions
WIDTH = 2200
HEIGHT = 1260
BG_COLOR = (255, 255, 255)

img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

# Fonts
font_dir = "/usr/share/fonts/truetype/liberation"
title_font = ImageFont.truetype(os.path.join(font_dir, "LiberationSans-Bold.ttf"), 38)
subtitle_font = ImageFont.truetype(os.path.join(font_dir, "LiberationSans-Bold.ttf"), 28)
body_font = ImageFont.truetype(os.path.join(font_dir, "LiberationSans-Regular.ttf"), 25)
label_font = ImageFont.truetype(os.path.join(font_dir, "LiberationSans-Italic.ttf"), 22)

def draw_rounded_box(draw, bbox, fill, outline, width=3, radius=18):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def draw_arrow_down(draw, start_pos, end_pos, color=(71, 85, 105), width=4, arrow_size=16):
    x1, y1 = start_pos
    x2, y2 = end_pos
    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
    # Arrow head
    draw.polygon([
        (x2, y2),
        (x2 - arrow_size, y2 - arrow_size * 1.5),
        (x2 + arrow_size, y2 - arrow_size * 1.5)
    ], fill=color)

def draw_branch_arrow(draw, start_pos, mid_y, end_pos, color=(71, 85, 105), width=4, arrow_size=16):
    x1, y1 = start_pos
    x2, y2 = end_pos
    # Path: down to mid_y, then horizontal to x2, then down to y2
    draw.line([(x1, y1), (x1, mid_y)], fill=color, width=width)
    draw.line([(x1, mid_y), (x2, mid_y)], fill=color, width=width)
    draw.line([(x2, mid_y), (x2, y2)], fill=color, width=width)
    draw.polygon([
        (x2, y2),
        (x2 - arrow_size, y2 - arrow_size * 1.5),
        (x2 + arrow_size, y2 - arrow_size * 1.5)
    ], fill=color)

# Box 1: Prospective Memory Layer (Top)
box1 = (300, 80, 1900, 310)
draw_rounded_box(draw, box1, fill="#eff6ff", outline="#2563eb", width=4)
draw.text((WIDTH//2, 125), "Prospective Memory Layer", font=title_font, fill="#1e3a8a", anchor="mm")
draw.text((WIDTH//2, 175), "Bioelectric Target Attractors & Long-Term Trajectory Setpoints", font=subtitle_font, fill="#2563eb", anchor="mm")
draw.text((WIDTH//2, 235), "Constitutive, forward-looking attractor states that continuously bias generative action selection,", font=body_font, fill="#334155", anchor="mm")
draw.text((WIDTH//2, 270), "eliminating the necessity to retrospectively recall or re-query core goals.", font=body_font, fill="#334155", anchor="mm")

# Arrow 1 -> 2
draw_arrow_down(draw, (WIDTH//2, 310), (WIDTH//2, 410), color="#2563eb", width=4)

# Box 2: Topological Gating (Middle)
box2 = (300, 410, 1900, 640)
draw_rounded_box(draw, box2, fill="#f0fdf4", outline="#059669", width=4)
draw.text((WIDTH//2, 455), "Topological Gating & Domain Boundaries", font=title_font, fill="#064e3b", anchor="mm")
draw.text((WIDTH//2, 505), "Gap-Junction Compartmentalisation: Wings & Functional Rooms", font=subtitle_font, fill="#059669", anchor="mm")
draw.text((WIDTH//2, 565), "Dynamically modulated conductance barriers separating relational priors from factual stores,", font=body_font, fill="#334155", anchor="mm")
draw.text((WIDTH//2, 600), "preventing catastrophic semantic dilution and unguided cross-domain associative bleed.", font=body_font, fill="#334155", anchor="mm")

# Branching arrows from Box 2 to Box 3 & 4
mid_split_y = 730
draw_branch_arrow(draw, (WIDTH//2 - 250, 640), mid_split_y, (625, 820), color="#059669", width=4)
draw_branch_arrow(draw, (WIDTH//2 + 250, 640), mid_split_y, (1575, 820), color="#059669", width=4)

# Box 3: Decay-Weighted Associative Graph (Bottom Left)
box3 = (100, 820, 1150, 1220)
draw_rounded_box(draw, box3, fill="#faf5ff", outline="#7c3aed", width=4)
draw.text((625, 875), "Decay-Weighted Associative Graph", font=title_font, fill="#4c1d95", anchor="mm")
draw.text((625, 930), "Dual-Rate Homeostasis & Intrinsic Decay", font=subtitle_font, fill="#7c3aed", anchor="mm")
draw.text((625, 995), "Associative co-activation graph with continuous metabolic", font=body_font, fill="#334155", anchor="mm")
draw.text((625, 1035), "decay (Anderson/ACT-R base-level learning). Recovers", font=body_font, fill="#334155", anchor="mm")
draw.text((625, 1075), "goal-relevant constraints post context wipe (recall@8 = 0.61)", font=body_font, fill="#334155", anchor="mm")
draw.text((625, 1115), "while flat cosine retrieval falls to chance (0.25).", font=body_font, fill="#334155", anchor="mm")
draw.text((625, 1165), "[Mechanistically verified in biofield_sim v0.6.0]", font=label_font, fill="#6b21a8", anchor="mm")

# Box 4: Filesystem as Extended Phenotype (Bottom Right)
box4 = (1050 + 100, 820, 2100, 1220)
draw_rounded_box(draw, box4, fill="#fffbeb", outline="#d97706", width=4)
draw.text((1575, 875), "Filesystem as Extended Phenotype", font=title_font, fill="#78350f", anchor="mm")
draw.text((1575, 930), "External Stigmergy & Verifiable Traces", font=subtitle_font, fill="#d97706", anchor="mm")
draw.text((1575, 995), "Clark & Chalmers extended mind architecture where the", font=body_font, fill="#334155", anchor="mm")
draw.text((1575, 1035), "local environment, filesystem, and version-controlled", font=body_font, fill="#334155", anchor="mm")
draw.text((1575, 1075), "code repositories serve as durable morphogenetic stigmergy,", font=body_font, fill="#334155", anchor="mm")
draw.text((1575, 1115), "immune to session reboots and context window limits.", font=body_font, fill="#334155", anchor="mm")
draw.text((1575, 1165), "[Operational stigmergic grounding via Open Amity]", font=label_font, fill="#92400e", anchor="mm")

# Title / Caption at bottom
# Caption handled by document

# Save
output_path = "/home/amity/Documents/Amity/Code/biofield_sim/paper/figure1_architecture.png"
img.save(output_path, "PNG", dpi=(300, 300))
print("Saved diagram to:", output_path)
