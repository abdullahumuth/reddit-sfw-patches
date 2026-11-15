"""Build the NSFW development bundle against pinned public Morphe release artifacts.

This avoids GitHub Maven authentication. The regular upstream Gradle build remains
the intended upstream release path. Only the new patch and runtime are compiled;
the upstream bundle's existing classes and extension are retained.
"""
import argparse
import hashlib
import os
from pathlib import Path
import subprocess
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
TOOLS = BUILD / "tools"
WORK = BUILD / "nsfw-build"


def fetch(name, url, digest=None):
    destination = TOOLS / name
    if not destination.exists():
        print("Downloading", name, flush=True)
        with urllib.request.urlopen(url, timeout=120) as response:
            destination.write_bytes(response.read())
    if digest and hashlib.sha256(destination.read_bytes()).hexdigest() != digest:
        raise RuntimeError("SHA-256 mismatch: " + name)
    return destination


def run(*command):
    subprocess.run(list(map(str, command)), cwd=ROOT, check=True)


def jar_directory(directory, destination):
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as output:
        for path in sorted(directory.rglob("*.class")):
            output.write(path, path.relative_to(directory).as_posix())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sdk", type=Path, default=os.environ.get("ANDROID_SDK_ROOT"))
    parser.add_argument("--compiler", type=Path, help="Kotlin compiler embeddable 2.4.21 jar")
    args = parser.parse_args()
    if not args.sdk:
        parser.error("--sdk or ANDROID_SDK_ROOT is required")
    sdk = Path(args.sdk)
    android = sdk / "platforms/android-36/android.jar"
    d8 = sorted(sdk.glob("build-tools/*/lib/d8.jar"))[-1]
    TOOLS.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    upstream = fetch("patches-2.2.0.mpp",
        "https://github.com/MorpheApp/morphe-patches/releases/download/v2.2.0/patches-2.2.0.mpp",
        "6ca368de24d475404257611cf03c2a82062a00ab9d60ddd220badaa332a68f2e")
    desktop = fetch("morphe-desktop.jar",
        "https://github.com/MorpheApp/morphe-desktop/releases/download/v2.1.1/morphe-desktop-2.1.1-all.jar",
        "3a2efefd567b44dde15971a58d5aa649a32aba30781d3400dc08d688c720168f")
    compiler = args.compiler
    if compiler is None:
        cached = list((Path.home() / ".gradle/caches/modules-2/files-2.1/org.jetbrains.kotlin/kotlin-compiler-embeddable/2.4.21").glob("*/*.jar"))
        compiler = cached[0] if cached else fetch("kotlin-compiler-embeddable-2.4.21.jar",
            "https://repo.maven.apache.org/maven2/org/jetbrains/kotlin/kotlin-compiler-embeddable/2.4.21/kotlin-compiler-embeddable-2.4.21.jar")
    # Host-test dependencies are pinned and verified by the same script used in CI.
    run("python", ROOT / "tools/test-nsfw.py")
    libraries = list((BUILD / "host-tests").glob("*.jar"))
    annotations = BUILD / "host-tests/annotations-13.0.jar"
    patch_classes = WORK / "patch-classes"
    patch_classes.mkdir(exist_ok=True)
    runtime_classes = WORK / "runtime-classes"
    runtime_classes.mkdir(exist_ok=True)
    stub_classes = WORK / "stub-classes"
    stub_classes.mkdir(exist_ok=True)
    stub_sources = WORK / "stubs"
    stub_sources.mkdir(exist_ok=True)
    # Compile-only declarations of existing extension APIs. Never packaged.
    (stub_sources / "Utils.java").write_text("""
        package app.morphe.extension.shared;
        public final class Utils {
            public static android.content.Context getContext() { throw new UnsupportedOperationException(); }
        }
        """)
    (stub_sources / "StringRef.java").write_text("""
        package app.morphe.extension.shared;
        public final class StringRef {
            public static String str(String key) { throw new UnsupportedOperationException(); }
        }
        """)
    (stub_sources / "AbstractPreferenceFragment.java").write_text("""
        package app.morphe.extension.shared.settings.preference;
        public abstract class AbstractPreferenceFragment extends android.preference.PreferenceFragment {
            public static void showRestartDialog(android.content.Context context) { throw new UnsupportedOperationException(); }
        }
        """)
    run("javac", "--release", "17", "-cp", android, "-d", stub_classes,
        *stub_sources.glob("*.java"))
    runtime = ROOT / "extensions/reddit/src/main/java/app/morphe/extension/reddit"
    sources = list((runtime / "patches/nsfw").glob("*.java"))
    sources += [runtime / "patches/PermanentNsfwPatch.java",
                runtime / "settings/preference/PermanentNsfwPreference.java"]
    run("javac", "--release", "17", "-cp", os.pathsep.join(map(str, [android, stub_classes, *libraries])),
        "-d", runtime_classes, *sources)
    run("java", "-cp", os.pathsep.join(map(str, [compiler, desktop, annotations])),
        "org.jetbrains.kotlin.cli.jvm.K2JVMCompiler", "-no-stdlib", "-no-reflect", "-jvm-target", "17",
        "-Xfriend-paths=" + str(upstream), "-cp", os.pathsep.join(map(str, [desktop, upstream])),
        "-d", patch_classes, ROOT / "patches/src/main/kotlin/app/morphe/patches/reddit/nsfw/PermanentNsfwPatch.kt")
    runtime_jar = WORK / "runtime.jar"
    patch_jar = WORK / "patch.jar"
    stub_jar = WORK / "stubs.jar"
    jar_directory(runtime_classes, runtime_jar)
    jar_directory(patch_classes, patch_jar)
    jar_directory(stub_classes, stub_jar)
    with zipfile.ZipFile(upstream) as original:
        (WORK / "reddit-original.dex").write_bytes(original.read("extensions/reddit.mpe"))
        (WORK / "patches-original.dex").write_bytes(original.read("classes.dex"))
    runtime_dex = WORK / "runtime-dex"
    patch_dex = WORK / "patch-dex"
    runtime_dex.mkdir(exist_ok=True)
    patch_dex.mkdir(exist_ok=True)
    run("java", "-cp", d8, "com.android.tools.r8.D8", "--release", "--min-api", "29",
        "--lib", android, "--classpath", stub_jar, *sum((["--classpath", path] for path in libraries), []),
        "--output", runtime_dex, WORK / "reddit-original.dex", runtime_jar)
    run("java", "-cp", d8, "com.android.tools.r8.D8", "--release", "--min-api", "26",
        "--lib", android, "--classpath", desktop, "--output", patch_dex,
        WORK / "patches-original.dex", patch_jar)
    if (patch_dex / "classes2.dex").exists() or (runtime_dex / "classes2.dex").exists():
        raise RuntimeError("Unexpected multidex extension/bundle output")
    destination = BUILD / "reddit-permanently-disable-nsfw-dev.mpp"
    with zipfile.ZipFile(upstream) as original, zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as output:
        for entry in original.infolist():
            data = original.read(entry.filename)
            if entry.filename == "extensions/reddit.mpe":
                data = (runtime_dex / "classes.dex").read_bytes()
            elif entry.filename == "classes.dex":
                data = (patch_dex / "classes.dex").read_bytes()
            elif entry.filename == "addresources/values/reddit/strings.xml":
                data = (ROOT / "patches/src/main/resources/addresources/values/reddit/strings.xml").read_bytes()
            elif entry.filename == "META-INF/MANIFEST.MF":
                manifest = data.decode().replace("\r", "")
                manifest = manifest.replace("Name: Morphe Patches", "Name: Permanently disable NSFW for Reddit (unofficial development)")
                manifest = manifest.replace("Description: Patches for Morphe", "Description: Experimental option to permanently disable NSFW content in Reddit based on Morphe Patches")
                manifest = manifest.replace("Author: MorpheApp", "Author: Permanently disable NSFW for Reddit contributors; upstream MorpheApp")
                manifest = manifest.replace("Source: git@github.com:MorpheApp/morphe-patches.git",
                    "Source: https://github.com/abdullahumuth/reddit-morphe-antinsfw")
                manifest = manifest.replace("Website: https://morphe.software",
                    "Website: https://github.com/abdullahumuth/reddit-morphe-antinsfw")
                data = manifest.encode()
            output.writestr(entry, data)
        for path in sorted(patch_classes.rglob("*.class")):
            output.write(path, path.relative_to(patch_classes).as_posix())
        for name in ("LICENSE", "NOTICE"):
            output.write(ROOT / name, name)
    print("Built", destination, flush=True)


if __name__ == "__main__":
    main()
