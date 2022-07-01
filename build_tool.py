import argparse
import json
from time import time
import subprocess
import os
import sys


def main():
    with open(
        os.path.join(os.path.dirname(__file__), "./typethon/build_metadata.json"), "r"
    ) as f:
        build_metadata = json.loads(f.read())

    top_ap = argparse.ArgumentParser(
        description="Tool for managing building of typethon."
    )
    sub_aps = top_ap.add_subparsers(required=True, dest="command")

    build_ap = sub_aps.add_parser(
        "build",
        help="Build typethon.",
        description="Build typethon.",
    )
    build_ap.add_argument(
        "--skip-git", help="Skip git commit hash fetching.", action="store_true"
    )

    cont_ap = sub_aps.add_parser(
        "add_contributor",
        help="Add yourself to the contributors list.",
        description="Add yourself to the contributors list.",
    )
    cont_ap.add_argument("author", help="The author's name.")

    args = top_ap.parse_args()

    if args.command == "build":
        print("Fetching timestamp...")
        build_metadata["build_timestamp"] = time()
        if not args.skip_git:
            print("Fetching commit hash...")
            try:
                build_metadata["build_commit"] = (
                    subprocess.check_output(["git", "rev-parse", "HEAD"])
                    .decode("ascii")
                    .strip()
                )
                build_metadata["build_commit_short"] = (
                    subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
                    .decode("ascii")
                    .strip()
                )
            except:
                print(
                    "Could not get commit hash. Is git installed? You can skip this stage with --skip-git (not recommended)."
                )
                exit(1)
        else:
            build_metadata["build_commit"] = "unknown"
            build_metadata["build_commit_short"] = "unknown"
        print("Saving modified metadata...")
        with open(
            os.path.join(os.path.dirname(__file__), "./typethon/build_metadata.json"),
            "w",
        ) as f:
            f.write(json.dumps(build_metadata, indent=4, sort_keys=True))
        print("Triggering build...")
        sys.argv.append("sdist")
        sys.argv.append("bdist_wheel")
        import setup

        print("Done!")
    elif args.command == "add_contributor":
        print("Adding contributor...")
        build_metadata["contributors"].append(args.author)
        print("Saving modified metadata...")
        with open(
            os.path.join(os.path.dirname(__file__), "./typethon/build_metadata.json"),
            "w",
        ) as f:
            f.write(json.dumps(build_metadata, indent=4, sort_keys=True))
        print("Done!")


if __name__ == "__main__":
    main()
