#!/usr/bin/env python3
"""Keep a public browsing invitation in Ming's generated GitHub READMEs."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parent.parent
START = "<!-- sidecourt-referral:start -->"
END = "<!-- sidecourt-referral:end -->"


def existing_referral(readme: str, repo: str) -> bool:
    config = json.loads((ROOT / "ops/github-referrals.json").read_text(encoding="utf-8"))
    entry = config.get("existing_referrals", {}).get(repo)
    return bool(entry and entry["link"] in readme and entry["context"] in readme)


def referral_block(repo: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", repo):
        raise ValueError("Expected a repository name, without an owner or URL")
    config = json.loads((ROOT / "ops/github-referrals.json").read_text(encoding="utf-8"))
    if config["browse_url"] != "https://sidecourt.space/drops/":
        raise ValueError("The referral must use the verified public browsing destination")
    query = urlencode(dict(utm_source="github", utm_medium="readme",
                          utm_campaign="tools", utm_content=repo))
    url = config["browse_url"] + "?" + query
    copy = config["repositories"].get(repo, config["default"])
    if copy.count("{url}") != 1 or "]({url})" not in copy:
        raise ValueError("Referral copy must contain one Markdown browsing link")
    return f"{START}\n## Explore SideCourt\n\n{copy.format(url=url)}\n{END}"


def ensure_referral(readme: str, repo: str) -> str:
    if START not in readme and END not in readme and existing_referral(readme, repo):
        return readme
    block = referral_block(repo)
    if START in readme or END in readme:
        if readme.count(START) != 1 or readme.count(END) != 1 or readme.index(START) > readme.index(END):
            raise ValueError("Ambiguous referral markers; preserve the README for manual repair")
        start, end = readme.index(START), readme.index(END) + len(END)
        return readme[:start] + block + readme[end:]
    # Preserve every existing byte, including retirement notices and install instructions.
    separator = "" if readme.endswith("\n\n") else "\n" if readme.endswith("\n") else "\n\n"
    return readme + separator + block + "\n"


def has_referral(readme: str, repo: str) -> bool:
    if START not in readme and END not in readme:
        return existing_referral(readme, repo)
    return readme.count(START) == 1 and readme.count(END) == 1 and referral_block(repo) in readme


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo")
    parser.add_argument("readme", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    content = args.readme.read_text(encoding="utf-8")
    if args.check:
        return 0 if has_referral(content, args.repo) else 1
    result = ensure_referral(content, args.repo)
    if result != content:
        args.readme.write_text(result, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
