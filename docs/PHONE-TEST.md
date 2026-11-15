# Test permanently disabling NSFW on your phone

This is an experimental build. These checks determine whether the feature actually covers your usage; passing host tests alone does not prove that.

1. In Morphe Manager, add `https://github.com/abdullahumuth/reddit-sfw-patches` as a patch source. Remove the old source entry first to discard its cached official bundle. Refresh sources and check that this one is called **Reddit SFW Patches (PR testing)**. Both channel settings point to the same experimental test build; neither makes it a stable release.
2. Select the same Reddit **2026.45.0 APKM** used for validation (arm64, build **2645001**). For the first test, select only **Permanently disable NSFW content (experimental)**; its required dependencies are automatic. Patch and install using Manager's prompts.
3. Open **Reddit → Settings → Morphe → Permanently disable NSFW content**. Confirm and restart when prompted.
4. Use harmless items that are marked NSFW where possible. Check the following:
   - Ordinary posts and searches still work.
   - Searches omit posts, communities, and profiles marked NSFW.
   - Known marked NSFW post/community/profile links cannot open their content, including links opened from outside Reddit.
   - Native adult-viewing and blur controls disappear. With the RedGIFs audio patch also selected, its audio/HD controls and the adult-dialog bypass control disappear; RedGIFs posts and playback requests must be blocked. The permanent setting says **NSFW content is permanently disabled** and cannot be reversed by tapping.
   - The behavior persists after closing/reopening Reddit, switching accounts, and anonymous browsing.
   - Also check saved/history/offline entries that existed before activation; this coverage remains unverified.
5. Report any failure in this repository's issues with the Reddit version, patch release, steps, and expected/actual behavior. Avoid posting explicit content or account credentials.

To reset between tests, clear Reddit's app data in Android settings. This signs you out and deletes its local data. There is deliberately no in-app undo. USB debugging is not needed.

## Regression checks for the reported failures

Current published builds through `v2.3.0-nsfw.5` have confirmed bypasses. Use only a newer candidate after host APK validation has completed; build success is not device verification.

Repeat these checks while signed in and in anonymous browsing, first with ordinary NSFW viewing previously off, then with it previously on before permanent activation. Reuse the same harmless, labelled community and preloaded links from the original failure.

- Open a marked community from a comment, history, and an external link. Its root must stay hidden while the label is checked; no icon, thumbnail, banner or posts may show behind a message. The message must explain that the community is marked NSFW and permanently disabled, with a working back action. It must not claim that the community does not exist.
- Return to an ordinary community. It must become visible and remain usable; a stale block must not cover it.
- Anonymous search must omit the native Show NSFW control. Native search filter state must remain safe even if it was previously set to show adult results.
- After activation, the saved adult-warning bypass and RedGIFs audio/HD settings are cleared as well as hidden. The confirmation restart must complete before retesting.
- Repeat after reopening Reddit and entering anonymous browsing again. Report blank safe screens, stuck navigation, transient image flashes, or any content exposure as failures.

Do not clear app data merely to install an update: the existing permanent setting must survive upgrading. Clearing data is only needed when deliberately preparing a fresh prior-setting test and signs you out.
