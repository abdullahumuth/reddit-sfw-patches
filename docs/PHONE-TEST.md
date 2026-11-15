# Test permanent NSFW disabling on your phone

1. Refresh the `https://github.com/abdullahumuth/reddit-sfw-patches` source in Manager. Confirm the new candidate version; versions through `2.3.0-nsfw.6` have known failures. The source name is **Reddit SFW Patches (PR testing)**. If it still shows the official identity, remove that source entry and add this repository again.
2. Select your **original Reddit 2026.45.0 APKM** (or the supplied 2026.40.0 APKM), not an installed or already patched APK. Explicitly select **Permanently disable NSFW content (experimental)**. Patch and install it.
3. Inside Reddit, check **Settings > Morphe > About** for the installed patches version; Manager's source version alone does not prove the installed app was updated. Preserve app data during an update so existing permanent activation remains in effect.
4. Activate permanent disabling if it is not already active and complete the restart. Check direct links from comments/history and searches while signed in and in anonymous browsing. Repeat with ordinary viewing previously enabled before activation when preparing a separate fresh-data test.
5. Reddit must behave as it does with its ordinary NSFW setting off: no adult content behind errors, no fake not-found response created by the patch, and no way to re-enable viewing. Viewing/blur and adult-search controls, the disclaimer-removal bypass, and RedGIFs audio/HD options must be absent or disabled. Safe posts, communities and searches must remain usable.

Use harmless labelled items where possible. Report any remaining bypass, visible thumbnail/posts, search toggle or broken safe page with the installed patches version and steps. No USB debugging is required. Host validation is not a phone pass.

Clearing app data is only for deliberately resetting between tests; it signs you out and resets permanent activation.
