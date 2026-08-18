[app]

# اسم التطبيق
title = Rym Shop

# اسم الحزمة
package.name = rymshop
package.domain = org.rymshop

# ملف التطبيق الرئيسي
source.dir = .
source.include_exts = py,json,ttf,png,jpg

# نقطة تشغيل التطبيق
entrypoint = main.py

# إصدار التطبيق
version = 1.0

# المكتبات المطلوبة
requirements = python3,kivy,arabic-reshaper,python-bidi

# اتجاه الشاشة
orientation = portrait

# اسم الأيقونة، إذا أضفناها لاحقًا
# icon.filename = %(source.dir)s/icon.png


[buildozer]

# مستوى السجل
log_level = 2

# تحذير من تشغيل Buildozer بصلاحيات root
warn_on_root = 1
