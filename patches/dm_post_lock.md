# Patch: Disable Post Scrolling (DM Viewer)

## Layer 1: Layout Controller
**File:** `smali_classes3/instagram/features/feed/contextualfeed/ContextualFeedFragment.smali`

**Modification:** In the `A18` method (Layout Configuration), check the module name. If it's a "direct" or "single" feed, call `suppressLayout(true)` on the RecyclerView.

### Search for:
```smali
.method public final A18(Landroidx/recyclerview/widget/RecyclerView;)V
    .locals 2

    invoke-static {p1}, LX/AuD;->A0o(Ljava/lang/Object;)V

    invoke-virtual {p0}, Landroidx/fragment/app/Fragment;->getContext()Landroid/content/Context;
```

### Replace with:
```smali
.method public final A18(Landroidx/recyclerview/widget/RecyclerView;)V
    .locals 2

    invoke-static {p1}, LX/AuD;->A0o(Ljava/lang/Object;)V

    invoke-virtual {p0}, Linstagram/features/feed/contextualfeed/ContextualFeedFragment;->getModuleName()Ljava/lang/String;

    move-result-object v0

    if-eqz v0, :cond_mod_lock

    const-string v1, "direct"

    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    move-result v1

    if-nez v1, :cond_lock_triggered

    const-string v1, "single"

    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    move-result v0

    if-eqz v0, :cond_mod_lock

    :cond_lock_triggered
    const/4 v0, 0x1

    invoke-virtual {p1, v0}, Landroidx/recyclerview/widget/RecyclerView;->suppressLayout(Z)V

    :cond_mod_lock
    invoke-virtual {p0}, Landroidx/fragment/app/Fragment;->getContext()Landroid/content/Context;
```

---

## Layer 2: Adapter Enforcement
**File:** `smali_classes16/X/Tvs.smali` (List Adapter)

**Modification:** Append an override for `getCount()` that always returns `1`. Even if the app tries to load more posts, the UI will only render the first one.

### Append to file:
```smali
.method public final getCount()I
    .locals 1

    const/4 v0, 0x1

    return v0
.end method
```
