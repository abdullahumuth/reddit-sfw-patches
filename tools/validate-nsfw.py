"""Read-only input inspection and host APK patching. Never installs or uses adb."""
import argparse
import os
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Reddit APK or APKM")
    parser.add_argument("--sdk", type=Path, default=os.environ.get("ANDROID_SDK_ROOT"))
    parser.add_argument("--verify-sdk", action="store_true", help="Also run strict SDK verification, including stock third-party code")
    parser.add_argument("--force", action="store_true", help="Force execution on unadvertised versions for compatibility discovery")
    parser.add_argument("--with-defaults", action="store_true", help="Include default patches to check integration")
    args = parser.parse_args()
    if not args.sdk:
        parser.error("--sdk or ANDROID_SDK_ROOT is required")
    work = ROOT / "build/reddit-apk"
    work.mkdir(exist_ok=True, parents=True)
    apk = args.input.resolve()
    if apk.suffix.lower() == ".apkm":
        with zipfile.ZipFile(apk) as bundle:
            apk = work / "base.apk"
            apk.write_bytes(bundle.read("base.apk"))
    command = ["java", "-Xmx4g", "-jar", str(ROOT / "build/tools/morphe-desktop.jar"),
               "patch", str(apk), "-p", str(ROOT / "build/reddit-permanently-disable-nsfw-dev.mpp"),
               "--exclusive", "-e", "Permanently disable NSFW content (experimental)",
               "--validate", "--unsigned",
               "-o", str(work / "nsfw-unsigned.apk"),
               "--result-file", str(work / "validation.json")]
    if args.force:
        command.append("-f")
    if args.with_defaults:
        command.remove("--exclusive")
    if args.verify_sdk:
        command.append("--verify-with-sdk=" + str(args.sdk))
    (work / "validation.json").unlink(missing_ok=True)
    log = ROOT / "build/nsfw-validation.log"
    with log.open("w", encoding="utf-8") as output:
        result = subprocess.run(command, cwd=ROOT, stdout=output, stderr=subprocess.STDOUT)
    print(log.read_text(encoding="utf-8")[-6000:])
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
