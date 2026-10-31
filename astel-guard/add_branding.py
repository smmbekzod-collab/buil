#!/usr/bin/env python3
"""Use the custom shield symbol for the Android launcher and app header."""
from pathlib import Path
import base64

asset = Path("astel-guard/assets/launcher_icon.webp.b64")
blob = base64.b64decode(asset.read_text().strip(), validate=True)
assert blob[:4] == b"RIFF" and blob[8:12] == b"WEBP", "Logo source is not a valid WebP file"
res = Path("AstelGuard/app/src/main/res/drawable-nodpi")
res.mkdir(parents=True, exist_ok=True)
(res / "astel_guard_icon.webp").write_bytes(blob)

manifest = Path("AstelGuard/app/src/main/AndroidManifest.xml")
m = manifest.read_text(encoding="utf-8")
old = '        android:label="Astel Guard"'
assert old in m, "App label missing"
m = m.replace(old, '        android:icon="@drawable/astel_guard_icon"\n' + old, 1)
manifest.write_text(m, encoding="utf-8")

activity = Path("AstelGuard/app/src/main/java/uz/astel/guard/MainActivity.java")
s = activity.read_text(encoding="utf-8")
old = '        hero.addView(txt("ASTEL  /  GUARD", 14, Color.rgb(97, 224, 199), true));'
assert old in s, "Hero header anchor missing"
new = '''        LinearLayout brandRow = horizontal();
        ImageView brandIcon = new ImageView(this);
        brandIcon.setImageResource(R.drawable.astel_guard_icon);
        brandIcon.setScaleType(ImageView.ScaleType.FIT_CENTER);
        LinearLayout.LayoutParams brandIconLp = new LinearLayout.LayoutParams(dp(60), dp(60));
        brandIconLp.setMargins(0, 0, dp(12), 0);
        brandRow.addView(brandIcon, brandIconLp);
        brandRow.addView(txt("ASTEL  /  GUARD", 16, Color.rgb(97, 224, 199), true));
        hero.addView(brandRow);'''
s = s.replace(old, new, 1)
activity.write_text(s, encoding="utf-8")
print("Custom Astel Guard shield logo installed in launcher and screen header.")
