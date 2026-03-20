from __future__ import annotations

from pathlib import Path

from PIL import Image

from .models import RenderConfig
from .renderer import render_coinpile

def generate_image(
    *,
    coins: int,
    width: int = 512,
    height: int = 512,
    random_seed: int = 42,
    pile_spacing: float = 5.0,
    new_pile_probability: float = 0.1,
    position_weight_multiplier: float = 2.0,
    height_weight_multiplier: float = -1.0,
    top_path: str | Path | None = None,
    layer_even_path: str | Path | None = None,
    layer_odd_path: str | Path | None = None,
    bottom_path: str | Path | None = None,
) -> Image.Image:
    config = RenderConfig(
        coins=coins,
        width=width,
        height=height,
        random_seed=random_seed,
        pile_spacing=pile_spacing,
        new_pile_probability=new_pile_probability,
        position_weight_multiplier=position_weight_multiplier,
        height_weight_multiplier=height_weight_multiplier,
        top_path=top_path,
        layer_even_path=layer_even_path,
        layer_odd_path=layer_odd_path,
        bottom_path=bottom_path,
    )
    return render_coinpile(config)


def save_png(
    output_path: str | Path,
    *,
    coins: int,
    width: int = 512,
    height: int = 512,
    random_seed: int = 42,
    pile_spacing: float = 5.0,
    new_pile_probability: float = 0.1,
    position_weight_multiplier: float = 2.0,
    height_weight_multiplier: float = -1.0,
    top_path: str | Path | None = None,
    layer_even_path: str | Path | None = None,
    layer_odd_path: str | Path | None = None,
    bottom_path: str | Path | None = None,
) -> Path:
    image = generate_image(
        coins=coins,
        width=width,
        height=height,
        random_seed=random_seed,
        pile_spacing=pile_spacing,
        new_pile_probability=new_pile_probability,
        position_weight_multiplier=position_weight_multiplier,
        height_weight_multiplier=height_weight_multiplier,
        top_path=top_path,
        layer_even_path=layer_even_path,
        layer_odd_path=layer_odd_path,
        bottom_path=bottom_path,
    )
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    image.save(out)
    return out
