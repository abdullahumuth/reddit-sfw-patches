"""Publish Manager metadata aliases after a successful manual PR-test build.

Preserves each alias branch's existing history. Source lives on pr-testing; these
branches are endpoints for Manager's fixed main/dev channel selection.
"""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def git(*args, input=None, env=None):
    return subprocess.check_output(["git", *args], cwd=ROOT, input=input,
                                   encoding="utf-8", env=env).strip()

def main():
    git("fetch", "origin", "pr-testing", "main", "dev")
    source = git("rev-parse", "origin/pr-testing")
    manifest = json.loads(git("show", source + ":patches-bundle.json"))
    if not manifest["download_url"].startswith("https://github.com/abdullahumuth/reddit-sfw-patches/releases/"):
        raise RuntimeError("Refusing a manifest pointing outside this test repository")
    index = ROOT / "build/test-source.index"
    index.parent.mkdir(exist_ok=True)
    index.unlink(missing_ok=True)
    environment = dict(os.environ, GIT_INDEX_FILE=str(index))
    try:
        for branch in ("main", "dev"):
            parent = git("rev-parse", "origin/" + branch)
            git("read-tree", parent, env=environment)
            for name in ("patches-bundle.json", "patches-list.json", ".github/workflows/release.yml"):
                blob = git("rev-parse", source + ":" + name)
                git("update-index", "--add", "--cacheinfo", "100644," + blob + "," + name, env=environment)
            readme = ("# Reddit SFW Patches (PR testing)\n\n"
                      "This branch is a Manager metadata endpoint for the temporary upstream PR test bundle.\n"
                      "Full source, instructions and status: [pr-testing](https://github.com/abdullahumuth/reddit-sfw-patches/tree/pr-testing).\n\n"
                      "Experimental; not an official release or a community-index submission.\n"
                      "The upstream contribution is [PR #4869](https://github.com/MorpheApp/morphe-patches/pull/4869).\n")
            blob = git("hash-object", "-w", "--stdin", input=readme)
            git("update-index", "--add", "--cacheinfo", "100644," + blob + ",README.md", env=environment)
            git("update-index", "--force-remove", "morphe-signing.pub", env=environment)
            tree = git("write-tree", env=environment)
            if tree == git("rev-parse", parent + "^{tree}"):
                print(branch, "already current")
                continue
            commit = git("commit-tree", tree, "-p", parent,
                         input="chore: Point Manager channel at PR test bundle " + manifest["version"] + "\n")
            git("push", "origin", commit + ":refs/heads/" + branch)
            print(branch, manifest["version"], commit)
    finally:
        index.unlink(missing_ok=True)

if __name__ == "__main__":
    main()
