# Patch: Disable Reels Scrolling (DM Viewer)

## File: `smali_classes3/X/1fG.smali` (Scroll Controller)

**Modification:** In the `onViewCreated` (A0P) method, check if the `ClipsViewerSource` is `DIRECT`. If so, disable user input on the `ViewPager2`.

### Search for:
```smali
    iput-object p1, p0, LX/1fG;->A00:Landroidx/viewpager2/widget/ViewPager2;

    iput-object p1, v1, LX/1fX;->A02:Landroid/view/View;
```

### Replace with:
```smali
    iput-object p1, p0, LX/1fG;->A00:Landroidx/viewpager2/widget/ViewPager2;

    iget-object v8, p0, LX/1fG;->A06:Lcom/instagram/clips/intf/ClipsViewerConfig;

    iget-object v8, v8, Lcom/instagram/clips/intf/ClipsViewerConfig;->A00:Lcom/instagram/clips/intf/ClipsViewerSource;

    sget-object v9, Lcom/instagram/clips/intf/ClipsViewerSource;->A1D:Lcom/instagram/clips/intf/ClipsViewerSource;

    if-ne v8, v9, :cond_mod_scroll

    const/4 v8, 0x0

    invoke-virtual {p1, v8}, Landroidx/viewpager2/widget/ViewPager2;->setUserInputEnabled(Z)V

    :cond_mod_scroll
    iput-object p1, v1, LX/1fX;->A02:Landroid/view/View;
```
