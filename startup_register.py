#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windowsスタートアップ登録ツール
PC起動時に自動でことわざアプリを起動します。
"""

import sys
import os
import winreg

APP_NAME = "KotowazaApp"
APP_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"


def get_app_path():
    app_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(app_dir, "kotowaza_app.py")


def get_pythonw():
    # pythonw.exe はコンソールウィンドウなしで実行できる
    base = os.path.dirname(sys.executable)
    candidates = [
        os.path.join(base, "pythonw.exe"),
        os.path.join(base, "pythonw"),
        sys.executable,
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    return sys.executable


def register():
    app_path = get_app_path()
    pythonw = get_pythonw()
    cmd = f'"{pythonw}" "{app_path}"'
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, APP_KEY, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, cmd)
        winreg.CloseKey(key)
        print(f"[OK] スタートアップに登録しました。")
        print(f"     コマンド: {cmd}")
    except Exception as e:
        print(f"[エラー] 登録できませんでした: {e}")


def unregister():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, APP_KEY, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, APP_NAME)
        winreg.CloseKey(key)
        print("[OK] スタートアップから削除しました。")
    except FileNotFoundError:
        print("[情報] スタートアップには登録されていません。")
    except Exception as e:
        print(f"[エラー] 削除できませんでした: {e}")


def status():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, APP_KEY, 0, winreg.KEY_READ)
        val, _ = winreg.QueryValueEx(key, APP_NAME)
        winreg.CloseKey(key)
        print(f"[登録済み] {val}")
    except FileNotFoundError:
        print("[未登録] スタートアップには登録されていません。")
    except Exception as e:
        print(f"[エラー] {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方:")
        print("  python startup_register.py register    # スタートアップに登録")
        print("  python startup_register.py unregister  # スタートアップから削除")
        print("  python startup_register.py status      # 登録状況を確認")
        sys.exit(0)

    cmd = sys.argv[1].lower()
    if cmd == "register":
        register()
    elif cmd == "unregister":
        unregister()
    elif cmd == "status":
        status()
    else:
        print(f"不明なコマンド: {cmd}")
        sys.exit(1)
