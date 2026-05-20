# Patch: Remove Reels Tab (Bottom Navigation)

## File: `smali/X/2zo.smali`

**Modification:** Redirect the `CLIPS` tab resource ID to match the `PROFILE` tab ID. This triggers Instagram's deduplication logic, removing the Reels icon entirely.

### Search for:
```smali
    .line 209
    .line 210
    const v6, 0x7f0b0c81
```

### Replace with:
```smali
    .line 209
    .line 210
    const v6, 0x7f0b306a
```

## File: `smali/X/8mm.smali`

**Modification:** Update the tab array to duplicate the Profile tab object into the slot previously held by the Clips tab object.

### Search for:
```smali
    sget-object v6, LX/2zo;->A09:LX/2zo;

    .line 13
    .line 14
    sget-object v7, LX/2zo;->A0B:LX/2zo;
```

### Replace with:
```smali
    sget-object v6, LX/2zo;->A0G:LX/2zo;

    .line 13
    .line 14
    sget-object v7, LX/2zo;->A0B:LX/2zo;
```
