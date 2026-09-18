from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ContrastResult:
    """WCAG contrast evaluation result."""

    foreground: str
    background: str
    ratio: float
    passes_aa_normal: bool
    passes_aa_large: bool
    passes_aaa_normal: bool
    passes_aaa_large: bool


class ContrastEvaluator:
    """Pure-domain WCAG contrast checker for color token pairs."""

    @staticmethod
    def _parse_hex_color(hex_color: str) -> tuple[int, int, int]:
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 3:
            hex_color = "".join(c * 2 for c in hex_color)
        if len(hex_color) != 6:
            raise ValueError(f"Invalid hex color: #{hex_color}")

        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return r, g, b

    @staticmethod
    def _relative_luminance(r: int, g: int, b: int) -> float:
        def channel_luminance(c: int) -> float:
            cs = c / 255.0
            return cs / 12.92 if cs <= 0.03928 else ((cs + 0.055) / 1.055) ** 2.4

        return (
            0.2126 * channel_luminance(r)
            + 0.7152 * channel_luminance(g)
            + 0.0722 * channel_luminance(b)
        )

    @classmethod
    def evaluate(cls, foreground_hex: str, background_hex: str) -> ContrastResult:
        fg_rgb = cls._parse_hex_color(foreground_hex)
        bg_rgb = cls._parse_hex_color(background_hex)

        fg_lum = cls._relative_luminance(*fg_rgb)
        bg_lum = cls._relative_luminance(*bg_rgb)

        lighter = max(fg_lum, bg_lum)
        darker = min(fg_lum, bg_lum)
        ratio = (lighter + 0.05) / (darker + 0.05)

        return ContrastResult(
            foreground=foreground_hex,
            background=background_hex,
            ratio=ratio,
            passes_aa_normal=ratio >= 4.5,
            passes_aa_large=ratio >= 3.0,
            passes_aaa_normal=ratio >= 7.0,
            passes_aaa_large=ratio >= 4.5,
        )
