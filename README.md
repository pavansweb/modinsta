# ModInsta: Distraction-Free Instagram

A project to surgically modify the Instagram Android APK to remove infinite-scroll "traps" while keeping essential communication features (DMs, Stories, Search).

## 🚀 Final Features (v4)
- **Reels Tab Removed:** The bottom navigation Reels button is replaced/merged with the Profile tab.
- **Homepage Reels Blocked:** Sugggested Reels ("Clips Netego") are invalidated. Your feed stays clean.
- **Stories Restored:** Essential story tray at the top remains fully functional.
- **Explore (Search) Page Reels Blocked:** Search for people and tags without the video grid distraction.
- **DM Reels Scroll-Lock:** Open a Reel from a message, but swiping up/down to see more is disabled.
- **DM Posts Scroll-Lock:** Viewing a post shared in DMs is locked to that single item.

## 🛠 Technical Implementation Progress

### Phase 1: Environment & Decompilation
- **Tools:** Setup portable Java 17 and Apktool 2.9.3.
- **Initial Target:** Bottom navigation bar.
- **Method:** Resource ID redirection. Merged `clips_tab` (0x7f0b0c81) with `profile_tab` ID to trigger Instagram's internal UI deduplication.

### Phase 2: The "Reels Rabbit Hole" Lock
- **Class:** `LX/1fG` (Scroll Controller).
- **Component:** `androidx.viewpager2.widget.ViewPager2`.
- **Logic:** Injected a conditional check on `ClipsViewerSource`. If source is `DIRECT` (0x1D), `setUserInputEnabled(false)` is called on the ViewPager.
- **Result:** Viewing shared Reels works, but infinite scrolling is dead.

### Phase 3: Network-Level Blocking (Home & Search)
- **Target 1:** `feed/reels_tray/` endpoint in `LX/4du.smali`. (Note: Later discovered this also blocked Stories).
- **Target 2:** `discover/explore_clips/` endpoint in `smali_classes11/X/PzM.smali`.
- **Method:** `sed` string invalidation of API endpoints to return 404/Empty responses.

### Phase 4: Story Restoration & Post Locking
- **Fix:** Switched from blocking the `reels_tray` endpoint (which contains Stories) to surgically invalidating the `CLIPS_NETEGO` enum in `LX/4my.smali`.
- **New Feature:** Locked DM posts.
- **Class:** `LX/Tvs` (List Adapter for Contextual Feed).
- **Method:** Overrode `getCount()` to return a constant `1`. This forces the app to render only the shared post, even if a feed is available.

## 📦 How to Build
1. Decompile: `apktool d -r instagram.apk`
2. Apply patches (see `/patches` folder).
3. Rebuild: `apktool b ig_mod -o modded.apk`
4. Sign: `java -jar uber-apk-signer.jar --apks modded.apk`

## ⚠️ Disclaimer
This project is for educational purposes only. Modifying APKs violates Meta's Terms of Service. Use at your own risk.
