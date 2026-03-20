from __future__ import annotations

import math
import random
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

from .models import RenderConfig


@dataclass(frozen=True)
class Pile:
    bottom_center_x: float
    bottom_center_y: float
    count: int

    @property
    def coin_width(self) -> int:
        return 8


def _spiral_positions(num_points: int, spacing: float = 5.0) -> list[tuple[float, float]]:
    points: list[tuple[float, float]] = []
    for i in range(num_points):
        theta = i * 137.5
        radius = spacing * math.sqrt(i)
        x = radius * math.cos(math.radians(theta))
        y = radius * math.sin(math.radians(theta))
        points.append((x, y))
    return points


def _load_sprites(config: RenderConfig) -> tuple[Image.Image, Image.Image, Image.Image, Image.Image]:
    assets = Path(__file__).resolve().parent / "assets"
    top_src = Path(config.top_path) if config.top_path else (assets / "top.png")
    layer_even_src = Path(config.layer_even_path) if config.layer_even_path else (assets / "layer_even.png")
    layer_odd_src = Path(config.layer_odd_path) if config.layer_odd_path else (assets / "layer_odd.png")
    bottom_src = Path(config.bottom_path) if config.bottom_path else (assets / "bottom.png")
    top = Image.open(top_src).convert("RGBA")
    layer_even = Image.open(layer_even_src).convert("RGBA")
    layer_odd = Image.open(layer_odd_src).convert("RGBA")
    bottom = Image.open(bottom_src).convert("RGBA")
    return top, layer_even, layer_odd, bottom


def _distribute_coins(
    total_coins: int,
    rng: random.Random,
    previous_pile_counts: list[int] | None,
    positions: list[tuple[float, float]],
    new_pile_probability: float,
    position_weight_multiplier: float,
    height_weight_multiplier: float,
) -> list[int]:
    if previous_pile_counts is None:
        pile_counts = [1]
        remaining_coins = total_coins - 1
    else:
        pile_counts = previous_pile_counts.copy()
        remaining_coins = total_coins - sum(pile_counts)

    while remaining_coins > 0:
        if rng.random() < new_pile_probability:
            pile_counts.append(1)
            remaining_coins -= 1
        else:
            break

    while remaining_coins > 0:
        weights: list[tuple[int, float]] = []
        pile_positions = [(i, y) for i, (_, y) in enumerate(positions[: len(pile_counts)])]
        pile_positions.sort(key=lambda x: x[1])

        for rank, (pile_idx, _) in enumerate(pile_positions):
            position_weight = 1.0 - (rank / len(pile_counts))
            height_weight = pile_counts[pile_idx] / max(pile_counts) if pile_counts else 1.0
            weight = (position_weight * position_weight_multiplier) + (height_weight * height_weight_multiplier)
            weights.append((pile_idx, weight))

        weights.sort(key=lambda x: x[0])
        normalized = [w for _, w in weights]
        total_weight = sum(normalized)
        if total_weight > 0:
            normalized = [w / total_weight for w in normalized]
            r = rng.random()
            cumsum = 0.0
            chosen_pile = len(normalized) - 1
            for i, w in enumerate(normalized):
                cumsum += w
                if r <= cumsum:
                    chosen_pile = i
                    break
        else:
            chosen_pile = rng.randint(0, len(pile_counts) - 1)

        pile_counts[chosen_pile] += 1
        remaining_coins -= 1

    return pile_counts


def _draw_coin_pile(
    count: int, top: Image.Image, layer_even: Image.Image, layer_odd: Image.Image, bottom: Image.Image
) -> Image.Image:
    count = max(1, int(count))
    total_height = (top.height - 1) + max(0, count - 1) + bottom.height
    pile = Image.new("RGBA", (top.width, total_height), (0, 0, 0, 0))

    for i in range(count - 1):
        if count % 2 == 0:
            layer = layer_even if i % 2 == 0 else layer_odd
        else:
            layer = layer_odd if i % 2 == 0 else layer_even
        pile.paste(layer, (0, top.height - 1 + i), layer)

    pile.paste(bottom, (0, top.height - 1 + max(0, count - 1)), bottom)
    pile.paste(top, (0, 0), top)
    return pile


def render_coinpile(config: RenderConfig) -> Image.Image:
    coin_count = config.resolved_coin_count()
    rng = random.Random(config.random_seed)
    top, layer_even, layer_odd, bottom = _load_sprites(config)

    canvas = Image.new("RGBA", (config.width, config.height), (0, 0, 0, 0))

    num_piles = coin_count + 1
    raw_positions = _spiral_positions(num_piles, spacing=config.pile_spacing)
    cx = config.width / 2
    cy = config.height / 2
    positions = [(x + cx, y + cy) for x, y in raw_positions]

    previous_pile_counts: list[int] | None = None
    for current_coins in range(1, coin_count + 1):
        pile_counts = _distribute_coins(
            current_coins,
            rng,
            previous_pile_counts,
            positions,
            config.new_pile_probability,
            config.position_weight_multiplier,
            config.height_weight_multiplier,
        )
        previous_pile_counts = pile_counts

    piles: list[Pile] = []
    for i, count in enumerate(pile_counts):
        if count > 0:
            x, y = positions[i]
            piles.append(Pile(bottom_center_x=x, bottom_center_y=y, count=count))

    piles.sort(key=lambda p: p.bottom_center_y)

    for pile in piles:
        pile_img = _draw_coin_pile(pile.count, top, layer_even, layer_odd, bottom)
        draw_x = int(round(pile.bottom_center_x - (pile.coin_width / 2)))
        draw_y = int(round(pile.bottom_center_y - pile_img.height))
        canvas.paste(pile_img, (draw_x, draw_y), pile_img)

    bbox = canvas.getbbox()
    if bbox is None:
        return canvas
    return canvas.crop(bbox)
