#!/usr/bin/env python3
"""Add a visible per-app restriction button to every app in All/Review/Internet lists.

The per-app controls are also available in details and apply to system apps when
the user opts to display those. Changes happen only in official Settings UI.
"""
from pathlib import Path
path = Path("AstelGuard/app/src/main/java/uz/astel/guard/MainActivity.java")
src=path.read_text(encoding="utf-8")
old='''        LinearLayout item = horizontal();
        item.setBackground(bg(Color.WHITE, 14));
        pad(item, 12, 11, 12, 11);
        LinearLayout.LayoutParams itemLp = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        itemLp.setMargins(0, 0, 0, dp(7));
        appList.addView(item, itemLp);'''
new='''        LinearLayout card = vertical();
        card.setBackground(bg(Color.WHITE, 14));
        LinearLayout.LayoutParams itemLp = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        itemLp.setMargins(0, 0, 0, dp(7));
        appList.addView(card, itemLp);
        LinearLayout item = horizontal();
        pad(item, 12, 11, 12, 8);
        card.addView(item);'''
assert old in src, "Could not find installed-app card layout"
src=src.replace(old,new,1)
old='''        item.setOnClickListener(v -> showDetails(a));
    }

    private String human(long bytes) {'''
new='''        item.setOnClickListener(v -> showDetails(a));
        Button quickRestrict = button("Ruxsatlarni cheklash", () -> showRestrictionTools(a), false);
        LinearLayout.LayoutParams btnLp = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(42));
        btnLp.setMargins(dp(12), 0, dp(12), dp(10));
        card.addView(quickRestrict, btnLp);
    }

    private String human(long bytes) {'''
assert old in src, "Could not find app card tail"
src=src.replace(old,new,1)
assert "showRestrictionTools(a)" in src
path.write_text(src,encoding="utf-8")
print("Added user-controlled permission restrictions to EVERY visible app row.")
