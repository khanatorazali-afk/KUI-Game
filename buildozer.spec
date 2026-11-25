[app]
title = KUI
icon.filename = %(source.dir)s/assets/kui_icon.png
package.name = kui
package.domain = kz.demo
source.dir = .
source.include_exts = py,wav,mp3,ogg,json,png,kv,ttf
source.exclude_patterns = server.py,tests/*
version = 0.2.1
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.archs = arm64-v8a, armeabi-v7a
android.release_artifact = aab
android.debug_artifact = apk
[buildozer]
log_level = 2
warn_on_root = 1
