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
    )
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    image.save(out)
    return out
