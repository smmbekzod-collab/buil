#!/usr/bin/env python3
"""Prepare a privacy-preserving Android APK without a sensitive Accessibility service.
The app can still inspect the enabled accessibility services of other installed apps.
This is intended to avoid requesting a potentially abused capability on sideload installs.
"""
from pathlib import Path
import re

base = Path("AstelGuard/app/src/main")
manifest_path = base / "AndroidManifest.xml"
manifest = manifest_path.read_text(encoding="utf-8")
manifest, n = re.subn(
    r'\s*<service\s+android:name="\.GuardWindowMonitor"[\s\S]*?</service>',
    "", manifest, count=1,
)
if n != 1:
    raise SystemExit("Expected Accessibility service declaration not found")
if "BIND_ACCESSIBILITY_SERVICE" in manifest or "android.permission.INTERNET" in manifest:
    raise SystemExit("Unexpected sensitive permission in the manifest")
manifest_path.write_text(manifest, encoding="utf-8")

src_path = base / "java/uz/astel/guard/MainActivity.java"
src = src_path.read_text(encoding="utf-8")
start = src.index('        LinearLayout monitor = vertical();')
end = src.index('        TextView heading = txt("Tekshiruv boshqaruvi",', start)
src = src[:start] + src[end:]
line_start = src.index('        device.addView(txt("Astel Guard faol kuzatuvi:')
line_end = src.index('\n', line_start) + 1
src = src[:line_start] + src[line_end:]
start = src.index('        LinearLayout history = vertical();')
end = src.index('\n    }\n\n    private void addMetric', start)
src = src[:start] + src[end:]
src_path.write_text(src, encoding="utf-8")

monitor_class = base / "java/uz/astel/guard/GuardWindowMonitor.java"
if monitor_class.exists():
    monitor_class.unlink()
config_xml = base / "res/xml/guard_accessibility.xml"
if config_xml.exists():
    config_xml.unlink()

print("Verified: No Accessibility service, no INTERNET permission.")
print("Preserved: app permissions audit, Usage Stats, traffic stats, admin and accessibility detection.")
