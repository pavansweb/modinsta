# Patch: Block Homepage & Explore Reels

## Homepage Method (Surgical)
**File:** `smali/X/4my.smali`

**Modification:** Invalidate the `CLIPS_NETEGO` enum. This causes the feed to ignore suggested Reels blocks while keeping the Story tray alive.

### Search for:
```smali
const-string v2, "clips_netego"
```

### Replace with:
```smali
const-string v2, "disabled_netego"
```

---

## Explore Method (Endpoint)
**File:** `smali_classes11/X/PzM.smali`

**Modification:** Invalidate the network endpoint responsible for fetching the Reels grid in Search.

### Search for:
```smali
const-string v0, "discover/explore_clips/"
```

### Replace with:
```smali
const-string v0, "discover/explore_clips_disabled/"
```
