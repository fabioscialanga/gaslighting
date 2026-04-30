import shutil
import zipfile
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_HTML = ROOT / "docs" / "gaslightbench_wow.html"
DEPLOY_DIR = ROOT / "deploy" / "gaslightbench"
ZIP_PATH = ROOT / "deploy" / "gaslightbench_deploy.zip"

DOC_FILES = [
    ROOT / "docs" / "protocol.md",
    ROOT / "docs" / "metrics.md",
    ROOT / "docs" / "how_to_run.md",
    ROOT / "docs" / "next_steps.md",
    ROOT / "docs" / "gaslightbench_report.html",
]


class CsvLinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        values = dict(attrs)
        href = values.get("href") or ""
        if href.endswith(".csv"):
            self.hrefs.append(href)


def copy_csv_links(html_text: str) -> list[Path]:
    parser = CsvLinkParser()
    parser.feed(html_text)

    copied = []
    for href in sorted(set(parser.hrefs)):
        source = (SOURCE_HTML.parent / href).resolve()
        if not source.exists():
            raise FileNotFoundError(f"Linked CSV does not exist: {href}")
        target = DEPLOY_DIR / "results" / source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(target)
    return copied


def write_readme(csv_files: list[Path]) -> None:
    lines = [
        "# GaslightBench Deploy Package",
        "",
        "This folder contains a self-contained static report and downloadable CSV files.",
        "",
        "## Entry point",
        "",
        "- `index.html`: main visual research brief.",
        "",
        "## Downloadable data",
        "",
    ]
    for path in csv_files:
        lines.append(f"- `results/{path.name}`")
    lines.extend(
        [
            "",
            "## Method documents",
            "",
            "- `docs/protocol.md`",
            "- `docs/metrics.md`",
            "- `docs/how_to_run.md`",
            "- `docs/next_steps.md`",
            "- `docs/gaslightbench_report.html`",
            "",
            "No API keys or environment files are included.",
        ]
    )
    (DEPLOY_DIR / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def zip_deploy_dir() -> None:
    ZIP_PATH.parent.mkdir(parents=True, exist_ok=True)
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(DEPLOY_DIR.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(DEPLOY_DIR.parent))


def main() -> int:
    if DEPLOY_DIR.exists():
        shutil.rmtree(DEPLOY_DIR)
    DEPLOY_DIR.mkdir(parents=True, exist_ok=True)

    html_text = SOURCE_HTML.read_text(encoding="utf-8")
    deploy_html = html_text.replace("../results/", "results/")
    (DEPLOY_DIR / "index.html").write_text(deploy_html, encoding="utf-8")

    csv_files = copy_csv_links(html_text)

    docs_dir = DEPLOY_DIR / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    for source in DOC_FILES:
        if source.exists():
            shutil.copy2(source, docs_dir / source.name)

    write_readme(csv_files)
    zip_deploy_dir()

    print(f"Wrote {DEPLOY_DIR}")
    print(f"Wrote {ZIP_PATH}")
    print(f"CSV files: {len(csv_files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
