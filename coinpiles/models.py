from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RenderConfig:
    coins: int
    width: int = 512
    height: int = 512
    random_seed: int = 42
    pile_spacing: float = 5.0
    new_pile_probability: float = 0.1
    position_weight_multiplier: float = 2.0
    height_weight_multiplier: float = -1.0

    def resolved_coin_count(self) -> int:
        return max(1, int(self.coins))
