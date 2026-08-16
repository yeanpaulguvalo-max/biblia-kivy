[app]
title = Palabra del Día
package.name = palabradeldia
package.domain = org.yean

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

version = 0.1

# Pillow: generación de imágenes | pyjnius: acceso a APIs de Android
requirements = python3,kivy,pillow,pyjnius,requests,urllib3,certifi,idna,charset-normalizer

orientation = portrait
fullscreen = 0

# Permiso necesario para cambiar el fondo de pantalla
android.permissions = SET_WALLPAPER

android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
