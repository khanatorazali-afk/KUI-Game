[app]
title = KUI
package.name = kui
package.domain = kz.demo
source.dir = .
source.include_exts = py,wav,json,png,kv
source.exclude_patterns = server.py,tests/*
version = 0.1.0
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
