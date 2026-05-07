# /// script
# requires-python = ">=3.11"
# dependencies = ["pillow"]
# ///
"""
Hand-designed 32×32 pixel logo: "MS" initials.

Tones: body (main terracotta), highlight (top-edge shine).
Outputs preview + TS rect array for src/lib/portrait_data.ts.
"""

from pathlib import Path
from PIL import Image, ImageDraw

SIZE = 32

# Layout: M (left), gap, S (right). Centered vertically.
# 'h' = highlight (top edge shine), 'B' = body, '.' = transparent
# Variant A: thicker M (3-pixel walls) for visual balance with S
VARIANT_A = """\
................................
................................
................................
................................
................................
................................
................................
................................
....hhh.....hhh...hhhhhhhhhh....
....BBB.....BBB...BBBBBBBBBB....
....BBBB...BBBB...BB............
....BBBBB.BBBBB...BB............
....BBBBBBBBBBB...BB............
....BBB.BBB.BBB...BB............
....BBB..B..BBB...BBBBBBBBBB....
....BBB.....BBB...BBBBBBBBBB....
....BBB.....BBB...........BB....
....BBB.....BBB...........BB....
....BBB.....BBB...........BB....
....BBB.....BBB...........BB....
....BBB.....BBB...BBBBBBBBBB....
....BBB.....BBB...BBBBBBBBBB....
................................
................................
................................
................................
................................
................................
................................
................................
................................
................................
"""

# Variant B: MS with terminal cursor "_" for identity hook (compact)
VARIANT_B = """\
................................
................................
................................
................................
................................
................................
................................
................................
.hh......hh....hhhhhhhhh........
.BB......BB....BBBBBBBBB........
.BBB....BBB....BB...............
.BBBB..BBBB....BB...............
.BB.BBBB.BB....BB...............
.BB..BB..BB....BBBBBBBBB........
.BB......BB....BBBBBBBBB........
.BB......BB...........BB........
.BB......BB...........BB........
.BB......BB...........BB........
.BB......BB....BBBBBBBBB........
.BB......BB....BBBBBBBBB........
................................
................................
........................hhhh....
........................BBBB....
................................
................................
................................
................................
................................
................................
................................
................................
"""

# Base shape for variant C (no shadow yet — added algorithmically)
VARIANT_C_BASE = """\
................................
................................
................................
................................
................................
................................
................................
................................
....hh......hh....hhhhhhhhhh....
....BB......BB....BBBBBBBBBB....
....BBB....BBB....BB............
....BBBB..BBBB....BB............
....BB.BBBB.BB....BB............
....BB..BB..BB....BB............
....BB......BB....BBBBBBBBBB....
....BB......BB....BBBBBBBBBB....
....BB......BB............BB....
....BB......BB............BB....
....BB......BB............BB....
....BB......BB............BB....
....BB......BB....BBBBBBBBBB....
....BB......BB....BBBBBBBBBB....
................................
................................
................................
................................
................................
................................
................................
................................
................................
................................
"""


def _connected_components(rows: list[list[str]]) -> list[set[tuple[int, int]]]:
    """Find 4-connected components of body/highlight cells."""
    h, w = len(rows), len(rows[0])
    seen: set[tuple[int, int]] = set()
    comps: list[set[tuple[int, int]]] = []
    for y in range(h):
        for x in range(w):
            if rows[y][x] not in ("B", "h") or (x, y) in seen:
                continue
            comp: set[tuple[int, int]] = set()
            stack = [(x, y)]
            while stack:
                cx, cy = stack.pop()
                if (cx, cy) in comp:
                    continue
                if not (0 <= cx < w and 0 <= cy < h):
                    continue
                if rows[cy][cx] not in ("B", "h"):
                    continue
                comp.add((cx, cy))
                stack.extend([(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)])
            comps.append(comp)
            seen |= comp
    return comps


def add_drop_shadow(design: str, dx: int = 1, dy: int = 1, bar_min: int = 4) -> str:
    """Add 'f' (shadow) at (x+dx, y+dy) for each body/highlight pixel.
    Allowed if the target is OUTSIDE every letter's bounding box, OR if the
    source body pixel is part of a horizontal stroke of >= bar_min consecutive
    body pixels (so horizontal bars cast interior shadow into their bowls)."""
    rows = [list(r) for r in design.strip("\n").split("\n") if r]
    h, w = len(rows), len(rows[0])
    comps = _connected_components(rows)
    bboxes = [
        (min(c[0] for c in comp), min(c[1] for c in comp),
         max(c[0] for c in comp), max(c[1] for c in comp))
        for comp in comps
    ]

    def inside_any_bbox(x: int, y: int) -> bool:
        return any(x0 <= x <= x1 and y0 <= y <= y1 for x0, y0, x1, y1 in bboxes)

    # Mark pixels that belong to a horizontal OR vertical run of length >= bar_min
    on_long_bar = [[False] * w for _ in range(h)]

    def is_body(yy: int, xx: int) -> bool:
        return rows[yy][xx] in ("B", "h")

    for y in range(h):
        x = 0
        while x < w:
            if is_body(y, x):
                x0 = x
                while x < w and is_body(y, x):
                    x += 1
                if x - x0 >= bar_min:
                    for xx in range(x0, x):
                        on_long_bar[y][xx] = True
            else:
                x += 1
    for x in range(w):
        y = 0
        while y < h:
            if is_body(y, x):
                y0 = y
                while y < h and is_body(y, x):
                    y += 1
                if y - y0 >= bar_min:
                    for yy in range(y0, y):
                        on_long_bar[yy][x] = True
            else:
                y += 1

    fills = {(x, y) for y in range(h) for x in range(w) if rows[y][x] in ("B", "h")}
    for x, y in fills:
        nx, ny = x + dx, y + dy
        if not (0 <= nx < w and 0 <= ny < h):
            continue
        if rows[ny][nx] != ".":
            continue
        outside = not inside_any_bbox(nx, ny)
        from_bar = on_long_bar[y][x]
        if outside or from_bar:
            rows[ny][nx] = "f"
    return "\n".join("".join(r) for r in rows) + "\n"


VARIANT_C = add_drop_shadow(VARIANT_C_BASE)

DESIGN = VARIANT_A  # default; will iterate via main()

CHAR_TO_ROLE = {"h": "highlight", "B": "body", "f": "face"}

PALETTE = {
    "highlight": "#e0a282",
    "body": "#c47a5a",
    "midtone": "#a86245",
    "face": "#7d4126",
    "dark": "#2a1a12",
}


def parse_design():
    rows = [r for r in DESIGN.strip("\n").split("\n") if r]
    assert len(rows) == SIZE, f"want {SIZE} rows, got {len(rows)}"
    grid = []
    for r in rows:
        assert len(r) == SIZE, f"want {SIZE} cols, got {len(r)}: {r!r}"
        grid.append(list(r))
    return grid


def to_rects(grid):
    rects = []
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch == ".":
                continue
            rects.append({"x": x, "y": y, "role": CHAR_TO_ROLE[ch]})
    return rects


def build_groups(rects):
    """Reveal in 5 vertical bands top-to-bottom."""
    bands = [[] for _ in range(5)]
    for i, r in enumerate(rects):
        gi = min(4, (r["y"] - 6) * 5 // 16) if r["y"] >= 6 else 0
        bands[max(0, gi)].append(i)
    return [b for b in bands if b]


def render_preview(grid, scale=16):
    img = Image.new("RGBA", (SIZE * scale, SIZE * scale), (10, 10, 15, 255))
    draw = ImageDraw.Draw(img)
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch == ".":
                continue
            color = PALETTE[CHAR_TO_ROLE[ch]]
            draw.rectangle(
                (x * scale, y * scale, x * scale + scale - 1, y * scale + scale - 1),
                fill=color,
            )
    return img


def emit_ts(rects, eyes, groups):
    rect_lines = ",\n  ".join(
        f'{{ x: {r["x"]}, y: {r["y"]}, w: 1, h: 1, role: "{r["role"]}" }}' for r in rects
    )
    eyes_str = ", ".join(str(i) for i in eyes)
    groups_str = ",\n  ".join("[" + ", ".join(str(i) for i in g) + "]" for g in groups)
    return (
        '// Hand-designed initials "MS" (32×32)\n'
        'import type { LogoRect } from "./logos";\n\n'
        f"export const PORTRAIT_VIEWBOX = {SIZE};\n\n"
        f"export const portraitShape: LogoRect[] = [\n  {rect_lines}\n];\n\n"
        f"export const portraitEyeIndices: number[] = [{eyes_str}];\n\n"
        f"export const portraitBuildGroups: number[][] = [\n  {groups_str}\n];\n"
    )


def render_variant(name: str, design: str):
    rows = [r for r in design.strip("\n").split("\n") if r]
    assert len(rows) == SIZE, f"[{name}] want {SIZE} rows, got {len(rows)}"
    grid = []
    for i, r in enumerate(rows):
        assert len(r) == SIZE, f"[{name}] row {i} has {len(r)} cols (need {SIZE}): {r!r}"
        grid.append(list(r))
    rects = to_rects(grid)
    preview = render_preview(grid, scale=16)
    preview.save(f"/tmp/ms_{name}_preview.png")
    preview.resize((128, 128), Image.NEAREST).save(f"/tmp/ms_{name}_actual.png")
    return rects


def main():
    rects_a = render_variant("a", VARIANT_A)
    rects_b = render_variant("b", VARIANT_B)
    rects_c = render_variant("c", VARIANT_C)

    # Build comparison: 3 variants side by side at 16x and at 128px
    from PIL import ImageDraw as _ID
    W, H = 1700, 800
    canvas = Image.new("RGBA", (W, H), (10, 10, 15, 255))
    for idx, name in enumerate(["a", "b", "c"]):
        big = Image.open(f"/tmp/ms_{name}_preview.png").resize((480, 480))
        small = Image.open(f"/tmp/ms_{name}_actual.png")
        x_big = 40 + idx * 560
        canvas.paste(big, (x_big, 200))
        canvas.paste(small, (x_big + 176, 60))
    draw = _ID.Draw(canvas)
    labels = ["A — M più spessa", "B — MS_ con cursore", "C — con drop shadow"]
    for i, lab in enumerate(labels):
        draw.text((40 + i * 560 + 100, 30), lab, fill="#c47a5a")
    canvas.save("/tmp/ms_variants.png")

    # Default winner: variant C. Emit TS for it.
    eyes: list[int] = []
    Path("/tmp/ms.ts").write_text(emit_ts(rects_c, eyes, build_groups(rects_c)))
    print({"a": len(rects_a), "b": len(rects_b), "c": len(rects_c)})


if __name__ == "__main__":
    main()
