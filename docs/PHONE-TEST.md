# Test permanently disabling NSFW on your phone

This is an experimental build. These checks determine whether the feature actually covers your usage; passing host tests alone does not prove that.

1. In Morphe Manager, add `https://github.com/abdullahumuth/reddit-morphe-antinsfw` as a patch source and enable **prereleases** for it.
2. Select the same Reddit **2026.45.0 APKM** used for validation (arm64, build **2645001**). Enable **Permanently disable NSFW content (experimental)**, patch, and install using Manager's prompts.
3. Open **Reddit → Settings → Morphe → Permanently disable NSFW content**. Confirm and restart when prompted.
4. Check the following without entering or viewing adult material:
   - Ordinary posts and searches still work.
   - Searches omit posts, communities, and profiles marked NSFW.
   - Known marked NSFW post/community/profile links cannot open their content, including links opened from outside Reddit.
   - Native adult-viewing and blur controls disappear. The permanent setting says **NSFW content is permanently disabled** and cannot be reversed by tapping.
   - The behavior persists after closing/reopening Reddit, switching accounts, and anonymous browsing.
   - Also check saved/history/offline entries that existed before activation; this coverage remains unverified.
5. Report any failure in this repository's issues with the Reddit version, patch release, steps, and expected/actual behavior. Avoid posting explicit content or account credentials.

To reset between tests, clear Reddit's app data in Android settings. This signs you out and deletes its local data. There is deliberately no in-app undo. USB debugging is not needed.
