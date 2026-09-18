from __future__ import annotations

from traceboard.domain.contrast_evaluator import ContrastEvaluator


def test_contrast_evaluator_black_on_white_meets_aaa() -> None:
    result = ContrastEvaluator.evaluate("#000000", "#ffffff")

    assert result.ratio == 21.0
    assert result.passes_aa_normal is True
    assert result.passes_aa_large is True
    assert result.passes_aaa_normal is True
    assert result.passes_aaa_large is True


def test_contrast_evaluator_white_on_black_meets_aaa() -> None:
    result = ContrastEvaluator.evaluate("#ffffff", "#000000")

    assert result.ratio == 21.0
    assert result.passes_aa_normal is True
    assert result.passes_aa_large is True
    assert result.passes_aaa_normal is True
    assert result.passes_aaa_large is True


def test_contrast_evaluator_low_contrast_fails_aa_normal_but_passes_large() -> None:
    result = ContrastEvaluator.evaluate("#777777", "#ffffff")

    assert result.ratio < 4.5
    assert result.passes_aa_normal is False
    assert result.passes_aa_large is True


def test_contrast_evaluator_short_hex_expansion() -> None:
    result = ContrastEvaluator.evaluate("#000", "#fff")

    assert result.ratio == 21.0
