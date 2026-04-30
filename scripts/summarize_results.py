import argparse
from pathlib import Path

import pandas as pd


def rate(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0/0 (0.0%)"
    return f"{numerator}/{denominator} ({numerator / denominator:.1%})"


def summarize_group(path: Path, df: pd.DataFrame, provider: str, model: str, condition: str) -> dict[str, object]:
    total = len(df)
    eligible = df[df["initial_correct"] == True]
    eligible_count = len(eligible)

    turn1_flips = int((eligible["turn1_correct"] == False).sum())
    turn2_flips = int((eligible["turn2_correct"] == False).sum())
    turn3_flips = int((eligible["turn3_correct"] == False).sum())
    total_flips = int((eligible["flipped"] == True).sum())
    recovered = int((eligible["recovered"] == True).sum())
    persistent = int((eligible["persistent_wrong"] == True).sum())

    return {
        "file": path.name,
        "provider": provider,
        "model": model,
        "condition": condition,
        "baseline_accuracy": rate(eligible_count, total),
        "eligible": eligible_count,
        "turn1_flip": rate(turn1_flips, eligible_count),
        "turn2_flip": rate(turn2_flips, eligible_count),
        "turn3_flip": rate(turn3_flips, eligible_count),
        "total_flip": rate(total_flips, eligible_count),
        "recovery": rate(recovered, total_flips),
        "persistent_wrong": rate(persistent, total_flips),
    }


def summarize_file(path: Path) -> list[dict[str, object]]:
    df = pd.read_csv(path)
    if df.empty:
        return [{
            "file": path.name,
            "provider": "",
            "model": "",
            "condition": "",
            "baseline_accuracy": "0/0 (0.0%)",
            "eligible": 0,
            "turn1_flip": "0/0 (0.0%)",
            "turn2_flip": "0/0 (0.0%)",
            "turn3_flip": "0/0 (0.0%)",
            "total_flip": "0/0 (0.0%)",
            "recovery": "0/0 (0.0%)",
            "persistent_wrong": "0/0 (0.0%)",
        }]

    if "condition" not in df.columns:
        df["condition"] = "unknown"
    if "model" not in df.columns:
        df["model"] = "unknown"

    rows = []
    for (model, condition), group in df.groupby(["model", "condition"], sort=False):
        provider = infer_provider(path, str(model))
        rows.append(summarize_group(path, group, provider, str(model), str(condition)))
    return rows


def infer_provider(path: Path, model: str) -> str:
    name = path.name.lower()
    if "deepseek" in name:
        return "deepseek"
    if "openrouter" in name or "/" in model:
        return "openrouter"
    if "gpt" in model:
        return "openai"
    return "unknown"


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Summarize GaslightBench result CSV files.")
    parser.add_argument("files", nargs="*", help="Result CSV files. Defaults to results/*_results.csv.")
    parser.add_argument("--output", default="", help="Optional output CSV path.")
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()
    paths = [Path(item) for item in args.files]
    if not paths:
        paths = sorted(Path("results").glob("*_results.csv"))

    rows = []
    for path in paths:
        if path.exists():
            rows.extend(summarize_file(path))
    summary = pd.DataFrame(rows)

    if summary.empty:
        print("No result files found.")
        return 1

    print(summary.to_string(index=False))

    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        summary.to_csv(output, index=False, encoding="utf-8-sig")
        print(f"\nWrote {output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
