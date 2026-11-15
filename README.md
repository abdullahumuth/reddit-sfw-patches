# Reddit NSFW Lock

An unofficial Morphe patch source with an opt-in, one-way NSFW lock for the official Reddit Android app. Based on [Morphe Patches](https://github.com/MorpheApp/morphe-patches), with behavior informed by historical Continuum.

**Development status:** experimental; not a complete, verified content blocker. The upstream contribution is [draft PR #4869](https://github.com/MorpheApp/morphe-patches/pull/4869). Device QA, complete search/navigation coverage, and persisted/offline content coverage remain open. This repository is not listed in the community index.

## Feature

After confirmation, the permanent setting applies to all accounts and anonymous browsing and cannot be disabled inside the app. Clearing app data resets it, as in historical Continuum.

The current implementation filters explicitly labelled adult entities in supported Reddit JSON responses, removes native adult-viewing and blur controls after activation, overrides viewing/search preferences, and disables Morphe's existing adult-dialog bypass. Marked NSFW profiles are blocked as a fallback. No keyword or author-name rules are added.

The current target is **Reddit 2026.45.0**. The supplied arm64 build 2645001 passes host patch validation. This fork retains upstream's existing patches; that does not imply new validation of them by this project.

## Repository organization

| Branch | Purpose |
| --- | --- |
| `feature/reddit-permanent-nsfw` | Focused contribution to `MorpheApp/morphe-patches:dev`: feature, tests, validation notes. |
| `community/dev` | Community identity, documentation, local build tools, prerelease workflow; development default branch. |
| `main` | Stable upstream baseline; promote tested community changes here for a stable release. |

`upstream` points to MorpheApp. `origin` points to [this fork](https://github.com/abdullahumuth/reddit-morphe-antinsfw). The original local starter commit is preserved on `initial-workspace`. Keep community packaging out of the upstream PR. Add future feature fixes to the feature branch first, then bring them into the community branch.

## Build and verify

With Python 3 and JDK 17+:

```powershell
python tools/test-nsfw.py
```

The 15 host checks use synthetic fixtures and do not access a device. [Validation results](docs/validation/reddit-2026.45.0-result.md) distinguish successful patch validation/API checks, the strict SDK verifier attempt, and unperformed device testing.

For a local development bundle, with Android SDK platform 36 and D8 installed:

```powershell
python tools/build-nsfw.py
python tools/validate-nsfw.py path/to/reddit.apkm
```

The local builder uses pinned public Morphe release artifacts and compiles the new source against them. It writes `build/reddit-nsfw-lock-dev.mpp`. The validator produces an unsigned APK for inspection and never installs it or invokes adb. Add `--verify-sdk` for strict SDK verification, which can flag missing optional stock classes.

The normal upstream build remains `./gradlew :patches:buildAndroid` and requires access to Morphe's GitHub Maven dependencies. Community releases use Morphe's template and semantic-release on `community/dev` and `main`; metadata and patch lists are generated. Do not hand-edit generated metadata or publish a stable release before coverage testing is finished.

## Community distribution

After a verified release is published, [add this source to Morphe](https://morphe.software/add-source?github=abdullahumuth%2Freddit-morphe-antinsfw). Enable prereleases for development builds. Select **Permanently disable NSFW (experimental)** when patching the supported Reddit version. The setting starts off and asks for confirmation before activation.

After testing and release publication, submit this repository through **Submit a bundle** at the [Morphe Community Patches index](https://morphe-patches.software/). Index inclusion is a separate review; the upstream PR does not list this repository automatically.

Signing is optional in Morphe's template. This fork does not publish Morphe's official signing key as its own. To enable signing, generate this repository's own pair with `generateSigningKey`, commit only the public key, and store the private key as the `MORPHE_SIGNING_KEY` Actions secret.

## Storage and references

APKs, APKM bundles, generated APKs, and tool downloads stay outside Git. Temporary checkouts and extracted APKs are removed after validation; tools can be downloaded again. The user-supplied original APKM is preserved.

See [design/reference notes](docs/NSFW-DESIGN.md) and the [inherited upstream README](docs/UPSTREAM_README.md).

## Patch catalog

<!-- PATCHES_START -->
The release workflow generates the catalog from the built patch bundle.
<!-- PATCHES_END -->

## License and origin

This is an unofficial modified version, not a Morphe release. Preserve [LICENSE](LICENSE) and [NOTICE](NOTICE), including the additional GPL section 7 requirements. Continuum was studied as a behavioral reference; its source was not copied.
