# Test permanent NSFW disabling on your phone

To test the independent fixes first, select **Prevent NSFW content flashing** and leave **Permanently disable NSFW content** unselected. Keep **Fix NSFW warning navigation** selected too. All three patches are selected by default in Manager, but each can be unchecked independently. Turn Reddit's ordinary NSFW setting off, then open flagged posts (including comment permalinks) and profiles from search, comments and external links. Check the first frame and a repeated visit. Go Back and the Android gesture should return one page. Repeat in anonymous browsing, and verify that turning the ordinary setting on still works. This build does not activate permanent disabling.

1. Refresh the `https://github.com/abdullahumuth/reddit-sfw-patches` source in Manager. Confirm the source version matches the current test release. The source name is **Reddit SFW Patches (PR testing)**. If it still shows the official identity, remove that source entry and add this repository again.
2. Select your **original Reddit 2026.45.0 APKM** (or the supplied 2026.40.0 APKM), not an installed or already patched APK. Keep all three NSFW patches selected to test them together. Patch and install it.
3. Inside Reddit, check **Settings > Morphe > About** for the installed patches version; Manager's source version alone does not prove the installed app was updated. Preserve app data during an update so existing permanent activation remains in effect.
4. In **Settings > Morphe > Layout**, activate **Permanently disable NSFW content** if it is not already active and complete the restart. Search while signed in and anonymously: the “NSFW search results are hidden” settings prompt and SafeSearch-only dropdown should be absent. Check that ordinary search filters still work.
5. Open a blocked community, profile and post from a comment or search. The shared warning should say **Go Back**; both that button and the Android back gesture should return to the previous screen. No blocked content or thumbnail should appear behind the warning, and blocked communities should stay out of both Recently Visited views.
6. In anonymous mode, press the Profile button and check its drawer as well as Settings: mature-content viewing and blur rows should be gone. Viewing/blur and adult-search controls, the disclaimer-removal bypass, and RedGIFs audio/HD options must be absent or disabled. Safe posts, communities and searches must remain usable. Repeat with ordinary viewing previously enabled before activation when preparing a separate fresh-data test.

Use harmless labelled items where possible. Report any remaining bypass, visible thumbnail/posts, search toggle or broken safe page with the installed patches version and steps. No USB debugging is required. Host validation is not a phone pass.

Also check that a flagged profile never flashes its header or posts before the warning, including on a repeated visit. Check the warning spacing and that the anonymous Profile drawer has no empty Settings section. Test a normal profile as a control.

Clearing app data is only for deliberately resetting between tests; it signs you out and resets permanent activation.
