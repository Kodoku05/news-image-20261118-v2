"""Render a fixed newspaper front page using measured Pillow typography."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
PAPER = "#F6F2E9"
NAVY = "#132638"
RED = "#B92E32"
RULE = "#C8C5BD"
FONT_PAIRS = (
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
     "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    ("/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
     "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"),
)
REGULAR, BOLD = next(
    pair for pair in FONT_PAIRS if all(Path(name).is_file() for name in pair)
)
image = Image.new("RGB", (1024, 1024), PAPER)
draw = ImageDraw.Draw(image)


def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else REGULAR, size)


def wrapped(text, face, width):
    lines = []
    for paragraph in text.split("\n"):
        line = ""
        for word in paragraph.split():
            assert draw.textlength(word, font=face) <= width, word
            candidate = f"{line} {word}".strip()
            if draw.textlength(candidate, font=face) > width:
                lines.append(line)
                line = word
            else:
                line = candidate
        lines.append(line)
    return lines


def text_block(text, x, y, width, size, leading, bold=False, color=NAVY):
    face = font(size, bold)
    for line in wrapped(text, face, width):
        left, top, right, bottom = draw.textbbox((x, y), line, font=face, anchor="lt")
        assert 0 <= left <= right < 1024 and 0 <= top <= bottom < 1024
        assert right <= x + width + 1, f"Text extends outside its column: {line}"
        assert bottom <= y + leading, f"Text exceeds line spacing: {line}"
        draw.text((x, y), line, font=face, fill=color, anchor="lt")
        y += leading
    return y


def centered(text, y, size, color, bold=False):
    face = font(size, bold)
    width = draw.textlength(text, font=face)
    assert width <= 960
    draw.text(((1024 - width) / 2, y), text, font=face, fill=color, anchor="lt")


# The date is a second masthead line, large enough to read at thumbnail scale.
draw.rectangle((0, 0, 1023, 145), fill=NAVY)
centered("THE WORLD TODAY", 23, 64, PAPER, True)
centered("WEDNESDAY 18 NOVEMBER 2026", 101, 33, PAPER, True)
draw.rectangle((0, 146, 1023, 152), fill=RED)

text_block("FULL-DAY WORLD NEWS", 32, 169, 960, 18, 22, True, RED)
lead_end = text_block(
    "IRAN STRIKES KUWAIT\nAND BAHRAIN", 30, 201, 964, 59, 65, True
)
deck_end = text_block(
    "Tehran hits US bases at Ali Al Salem after the US struck Qeshm Island "
    "in the Strait of Hormuz.",
    32, lead_end + 7, 960, 22, 28,
)
grid_top = deck_end + 16
draw.line((32, grid_top, 992, grid_top), fill=NAVY, width=3)

stories = [
    ("KERCH BRIDGE SPAN COLLAPSES",
     "Ukraine hits the Crimea bridge a second day running; 227m road arch falls, 2 killed."),
    ("XI AND PUTIN MEET IN SHENZHEN",
     "Ahead of Thursday’s first trilateral summit with Trump."),
    ("DEMOCRATS TAKE SENATE 56-44",
     "Peltola wins Alaska, the last midterm race decided."),
    ("ISRAEL ELECTS NEW SPEAKER",
     "Matan Kahana wins the Knesset vote, a setback for Netanyahu."),
    ("US LOSES MEASLES-FREE STATUS",
     "After 26 years: 5,400 cases, 10 deaths."),
    ("NVIDIA POSTS RECORD 115.8BN QUARTER",
     "Revenue up 103%; board rejects Huang’s return as CEO."),
    ("EBOLA PASSES 11,000 CASES IN DR CONGO",
     "Seven in ten children under five die."),
]

grid_bottom = 931
draw.line((512, grid_top + 14, 512, grid_bottom), fill=RULE, width=1)
for x, indices in ((32, (0, 1, 3, 4)), (535, (2, 5, 6))):
    heights = [
        len(wrapped(stories[i][0], font(30, True), 457)) * 32 + 6
        + len(wrapped(stories[i][1], font(20), 457)) * 24
        for i in indices
    ]
    available = grid_bottom - (grid_top + 14)
    gap = (available - sum(heights)) / (len(indices) - 1)
    assert gap >= 12, f"Insufficient story separation: {gap}"
    y = grid_top + 14
    for position, i in enumerate(indices):
        title, deck = stories[i]
        end = text_block(title, x, y, 457, 30, 32, True)
        end = text_block(deck, x, end + 6, 457, 20, 24)
        assert end <= grid_bottom + 0.01
        if position < len(indices) - 1:
            rule_y = end + gap / 2
            draw.line((x, rule_y, x + 457, rule_y), fill=RULE, width=1)
        y = end + gap

footer_top = 947
draw.rectangle((0, footer_top, 1023, 1023), fill=NAVY)
draw.rectangle((0, footer_top, 8, 1023), fill=RED)
footer_end = text_block(
    'Trump hails “very big” Philippines trade deal — 6.0 quake hits Papua New Guinea — '
    'Russian military plane crashes in Siberia, 19 dead — Cold kills in Gaza tents.',
    32, footer_top + 15, 960, 17, 23, color=PAPER,
)
assert footer_end <= 1018, f"Footer exceeds canvas: {footer_end}"
destination = ROOT / "entry.png"
image.save(destination, optimize=True)
assert destination.stat().st_size <= 1048576
print(f"Saved {destination.name}: 1024 x 1024; {destination.stat().st_size} bytes")
