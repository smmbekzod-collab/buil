#!/usr/bin/env python3
"""Add user-confirmed, per-app Android permission restriction shortcuts.

This deliberately does not use Accessibility automation or change permissions
without the user entering the OS settings. Android's Device Owner API is not
available to a normal installed application.
"""
from pathlib import Path

src_path = Path("AstelGuard/app/src/main/java/uz/astel/guard/MainActivity.java")
src = src_path.read_text(encoding="utf-8")

old = '''        frame.addView(protect, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(44)));
        space(frame, 6);
        Button allFiles = button("Barcha fayllarga kirish ruxsatlari",'''
new = '''        frame.addView(protect, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(44)));
        space(frame, 6);
        Button restrictTarget = button("APK Qo‘riqchi — ruxsatlarni cheklash", () -> {
            for (AppRecord app : apps) {
                if ("com.baxtiyorov.security".equals(app.packageName)) {
                    showRestrictionTools(app);
                    return;
                }
            }
            new AlertDialog.Builder(this)
                    .setMessage("APK Qo‘riqchi topilmadi. Ilovalar ro‘yxatidan boshqa ilovani tanlashingiz mumkin.")
                    .setPositiveButton("Tushunarli", null).show();
        }, true);
        frame.addView(restrictTarget, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(44)));
        space(frame, 6);
        Button allFiles = button("Barcha fayllarga kirish ruxsatlari",'''
assert old in src, "Target shortcut anchor missing"
src = src.replace(old, new, 1)

old = '''        space(column, 14);
        Button open = button("Ilova ruxsatlari va sozlamalari",'''
new = '''        space(column, 14);
        Button restrict = button("Ruxsatlarni cheklash / boshqarish", () -> showRestrictionTools(a), true);
        column.addView(restrict, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(46)));
        space(column, 8);
        Button open = button("Ilova ruxsatlari va sozlamalari",'''
assert old in src, "Details dialog anchor missing"
src = src.replace(old, new, 1)

old = '''            String state = p.special ? "Maxsus ruxsat: holatini sozlamada tekshiring" : (p.granted ? "Berilgan" : "Berilmagan");'''
new = '''            String state = p.special ? "Maxsus ruxsat: holatini sozlamada tekshiring"
                    : isAutomaticPermission(p.permission) ? "Tizim ruxsati (alohida o‘chirib bo‘lmaydi)"
                    : (p.granted ? "Berilgan" : "Berilmagan");'''
assert old in src, "Permission state anchor missing"
src = src.replace(old, new, 1)

mark = '    private void shareReport() {'
assert mark in src, "Method insertion anchor missing"
insert = '''    private boolean isAutomaticPermission(String permission) {
        try {
            android.content.pm.PermissionInfo pi;
            if (Build.VERSION.SDK_INT >= 33) {
                pi = getPackageManager().getPermissionInfo(permission,
                        PackageManager.PermissionInfoFlags.of(0));
            } else {
                pi = getPackageManager().getPermissionInfo(permission, 0);
            }
            return (pi.getProtection() & android.content.pm.PermissionInfo.PROTECTION_MASK_BASE)
                    == android.content.pm.PermissionInfo.PROTECTION_NORMAL;
        } catch (Exception ignored) {
            return false;
        }
    }

    private void addRestrictionAction(LinearLayout container, String title, String explanation, Runnable onClick) {
        space(container, 9);
        container.addView(txt(title, 13, TEXT, true));
        container.addView(txt(explanation, 11, MUTED, false));
        space(container, 3);
        Button b = button("Sozlamani ochish", onClick, false);
        container.addView(b, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(43)));
    }

    private void showRestrictionTools(AppRecord a) {
        ScrollView scroll = new ScrollView(this);
        LinearLayout column = vertical();
        pad(column, 18, 12, 18, 16);
        scroll.addView(column);
        column.addView(txt(a.name + " (" + a.packageName + ")", 13, TEXT, true));
        space(column, 7);
        column.addView(txt("Bu oynadagi tugmalar Android sozlamasini ochadi. Ruxsatni siz bekor qilasiz; Astel Guard yashirin ravishda o‘zgartirmaydi.", 12, AMBER, false));

        addRestrictionAction(column, "1. Kamera, mikrofon, rasmlar, kontaktlar, SMS va joylashuv",
                "Ilova haqida → Ruxsatlar (Разрешения) → kerakli huquq → Запретить.",
                () -> openAppSettings(a.packageName));

        addRestrictionAction(column, "2. Barcha fayllarga kirish",
                "Barcha fayllarga kirish (Доступ ко всем файлам) ro‘yxatida ushbu ilovaning tugmasini o‘chiring.",
                () -> openAllFiles(a.packageName));

        addRestrictionAction(column, "3. Boshqa ilovalar ustida oynalar",
                "Поверх других окон ruxsatini o‘chiring. Ayrim Android versiyalarida umumiy ro‘yxat ochiladi.",
                () -> openPackageAction(Settings.ACTION_MANAGE_OVERLAY_PERMISSION, a.packageName));

        addRestrictionAction(column, "4. Noma’lum manbadan APK o‘rnatish",
                "Установка неизвестных приложений → Запретить / Не разрешать.",
                () -> openPackageAction(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES, a.packageName));

        addRestrictionAction(column, "5. Foydalanish tarixini kuzatish",
                "Доступ к данным об использовании → ilovani tanlang va o‘chiring.",
                () -> safeStart(new Intent(Settings.ACTION_USAGE_ACCESS_SETTINGS)));

        addRestrictionAction(column, "6. Accessibility xizmatlari",
                "Специальные возможности → yuklangan xizmatlar. Faqat ushbu ilovaga tegishlisini o‘chiring.",
                () -> safeStart(new Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS)));

        addRestrictionAction(column, "7. Telefon administratorligi",
                "Администраторы устройства → faqat ushbu ilova faol bo‘lsa, administratorlikni bekor qiling.",
                () -> safeStart(new Intent(Settings.ACTION_SECURITY_SETTINGS)));

        addRestrictionAction(column, "8. Bildirishnomalar",
                "Уведомления → Разрешить уведомления tugmasini o‘chiring.",
                () -> openNotificationSettings(a.packageName));

        addRestrictionAction(column, "9. Internet / fon ma’lumotlari",
                "Mobil internet yoki Wi-Fi cheklovlarini telefonning tarmoq sozlamasida tekshiring. INTERNET — oddiy tizim ruxsati, bu tugma uni bekor qilmaydi.",
                () -> safeStart(new Intent(Settings.ACTION_DATA_USAGE_SETTINGS)));

        addRestrictionAction(column, "10. Ilovani majburan to‘xtatish yoki o‘chirish",
                "О приложении → Остановить / Удалить. To‘xtatish doimiy bloklash emas.",
                () -> openAppSettings(a.packageName));

        space(column, 13);
        column.addView(txt("Eslatma: barcha ilovalarning ruxsatlarini bir bosishda bekor qilish Android tomonidan oddiy ilovalarga berilmaydi. Avtomatik beriladigan tizim ruxsatlari, masalan INTERNET, oddiy ruxsatlar ro‘yxatidan o‘chirilmaydi.", 11, MUTED, false));
        new AlertDialog.Builder(this).setTitle("Ruxsatlarni cheklash")
                .setView(scroll).setPositiveButton("Yopish", null).show();
    }

    private void openPackageAction(String action, String pkg) {
        try {
            Intent i = new Intent(action);
            i.setData(Uri.parse("package:" + pkg));
            startActivity(i);
        } catch (Exception ignored) {
            openAppSettings(pkg);
        }
    }

    private void openNotificationSettings(String pkg) {
        try {
            Intent i = new Intent(Settings.ACTION_APP_NOTIFICATION_SETTINGS);
            i.putExtra(Settings.EXTRA_APP_PACKAGE, pkg);
            startActivity(i);
        } catch (Exception ignored) {
            openAppSettings(pkg);
        }
    }

'''
src = src.replace(mark, insert + mark, 1)
src_path.write_text(src, encoding="utf-8")
assert "showRestrictionTools(AppRecord a)" in src
print("Updated per-app permission management screens for Astel Guard.")
