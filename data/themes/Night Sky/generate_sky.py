"""Rebuild the static vector sky; no runtime drawing or animation is needed."""

# This standalone asset generator is not an importable package.
# ruff: noqa: INP001

from pathlib import Path
from random import Random

WIDTH, HEIGHT = 1500, 320
SEED = 71024


def generate() -> str:
    rng = Random(SEED)  # noqa: S311 - reproducible star positions, not security
    parts = [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
            f'viewBox="0 0 {WIDTH} {HEIGHT}" preserveAspectRatio="none">'
        ),
        (
            '<defs><linearGradient id="sky" x2="0" y2="1">'
            '<stop stop-color="#141a45"/><stop offset=".5" stop-color="#1e1b5c"/>'
            '<stop offset="1" stop-color="#05050d"/></linearGradient>'
        ),
        (
            '<radialGradient id="nebula"><stop stop-color="#6b3fa0" stop-opacity=".55"/>'
            '<stop offset=".45" stop-color="#4b2a7a" stop-opacity=".35"/>'
            '<stop offset="1" stop-color="#4b2a7a" stop-opacity="0"/></radialGradient>'
        ),
        (
            '<linearGradient id="fade" x2="0" y2="1">'
            '<stop stop-color="#fff"/>'
            '<stop offset=".38" stop-color="#fff" stop-opacity=".92"/>'
            '<stop offset=".77" stop-color="#fff" stop-opacity=".2"/>'
            '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        ),
        (
            '<filter id="soft" x="-.3" y="-.5" width="1.6" height="2">'
            '<feGaussianBlur stdDeviation="12"/></filter></defs>'
        ),
        f'<mask id="header"><path fill="url(#fade)" d="M0 0h{WIDTH}v{HEIGHT}H0z"/></mask>',
        '<g mask="url(#header)">',
        f'<path fill="url(#sky)" d="M0 0h{WIDTH}v{HEIGHT}H0z"/>',
        '<ellipse cx="1150" cy="65" rx="480" ry="195" fill="url(#nebula)"/>',
        '<ellipse cx="980" cy="100" rx="290" ry="95" fill="url(#nebula)" opacity=".45"/>',
        '<g fill="#1c2a5a" opacity=".55" filter="url(#soft)">',
        ('<path d="M-50 220Q-20 120 65 159Q110 105 160 157Q240 130 275 195Q320 147 380 205Q430 170 490 250H-50Z"/>'),
        '<path d="M-40 270Q40 190 105 231Q170 181 215 219Q300 185 365 260H-40Z"/></g>',
    ]
    for _ in range(95):
        x, y = rng.uniform(20, WIDTH - 20), rng.uniform(12, 245)
        radius = rng.choices([0.8, 1.2, 1.8, 2.5], weights=[45, 35, 17, 3])[0]
        opacity = rng.uniform(0.25, 0.85)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius}" fill="white" opacity="{opacity:.2f}"/>')
    for x, y, size in [(190, 71, 7), (835, 119, 6), (1290, 93, 8)]:
        parts.append(
            f'<path transform="translate({x} {y})" fill="#fff" opacity=".85" '
            f'd="M0 -{size} 1.4 -1.4 {size} 0 1.4 1.4 0 {size} -1.4 1.4 -{size} 0 -1.4 -1.4Z"/>'
        )
    parts.append("</g></svg>")
    return "\n".join(parts) + "\n"


if __name__ == "__main__":
    Path(__file__).with_name("sky.svg").write_text(generate())
