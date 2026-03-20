from __future__ import annotations

import argparse

from .api import save_png


def main() -> None:
    parser = argparse.ArgumentParser(prog="coinpiles", description="Generate coin pile images from numeric values.")
    sub = parser.add_subparsers(dest="command", required=True)

    generate = sub.add_parser("generate", help="Generate a PNG from coins")
    generate.add_argument("--coins", type=int, required=True, help="Coin count")
    generate.add_argument("--width", type=int, default=512, help="Canvas width before crop")
    generate.add_argument("--height", type=int, default=512, help="Canvas height before crop")
    generate.add_argument("--random-seed", type=int, default=42, help="Random seed for deterministic layout")
    generate.add_argument("--pile-spacing", type=float, default=5.0, help="Spiral spacing between pile anchors")
    generate.add_argument("--new-pile-probability", type=float, default=0.1, help="Chance to start a new pile")
    generate.add_argument(
        "--position-weight-multiplier", type=float, default=2.0, help="Bias multiplier for higher piles"
    )
    generate.add_argument(
        "--height-weight-multiplier", type=float, default=-1.0, help="Bias multiplier for current pile height"
    )
    generate.add_argument(
        "--top-path", default=None, help="Path to top sprite"
    )
    generate.add_argument("--layer-even-path", default=None, help="Path to even layer sprite")
    generate.add_argument("--layer-odd-path", default=None, help="Path to odd layer sprite")
    generate.add_argument("--bottom-path", default=None, help="Path to bottom sprite")
    generate.add_argument("--output", required=True, help="Output PNG path")

    args = parser.parse_args()
    if args.command == "generate":
        out = save_png(
            args.output,
            coins=args.coins,
            width=args.width,
            height=args.height,
            random_seed=args.random_seed,
            pile_spacing=args.pile_spacing,
            new_pile_probability=args.new_pile_probability,
            position_weight_multiplier=args.position_weight_multiplier,
            height_weight_multiplier=args.height_weight_multiplier,
            top_path=args.top_path,
            layer_even_path=args.layer_even_path,
            layer_odd_path=args.layer_odd_path,
            bottom_path=args.bottom_path,
        )
        print(f"Generated: {out}")


if __name__ == "__main__":
    main()
