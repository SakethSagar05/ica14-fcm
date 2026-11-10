#!/usr/bin/env bash
# ICA 14 test helper for an Android emulator/device (uses adb). Run from anywhere:
#   bash tools/fcm_helper.sh info       device/OS + notification permission -> docs/device.txt
#   bash tools/fcm_helper.sh token      copy the current FCM token to the clipboard (never printed in full)
#   bash tools/fcm_helper.sh shot NAME  screenshot -> docs/screenshots/NAME.png  (e.g. T1a, T1b ... T4b)
#   bash tools/fcm_helper.sh home       press Home (puts the app in the background for T2)
#   bash tools/fcm_helper.sh shade      pull down the notification shade
#   bash tools/fcm_helper.sh recents    open recent apps (swipe the app away for T3; NOT force-stop)
set -uo pipefail

PKG="com.saketh.ica14_fcm"
cd "$(dirname "$0")/.."
SDK="${ANDROID_HOME:-${ANDROID_SDK_ROOT:-$HOME/Library/Android/sdk}}"
export PATH="$PATH:$SDK/platform-tools"
command -v adb >/dev/null || { echo "adb not found (expected in $SDK/platform-tools)"; exit 1; }
adb get-state >/dev/null 2>&1 || { echo "No emulator/device connected. Start one, then retry."; exit 1; }
mkdir -p docs/screenshots

case "${1:-}" in
  info)
    model="$(adb shell getprop ro.product.model | tr -d '\r')"
    rel="$(adb shell getprop ro.build.version.release | tr -d '\r')"
    api="$(adb shell getprop ro.build.version.sdk | tr -d '\r')"
    perm="$(adb shell dumpsys package "$PKG" | tr -d '\r' | grep -o 'android.permission.POST_NOTIFICATIONS: granted=[a-z]*' | head -1)"
    gms="$(adb shell pm list packages com.google.android.gms | tr -d '\r' | head -1)"
    { echo "Device: $model, Android $rel (API $api)"
      echo "Notification permission: ${perm:-not found (is the app installed?)}"
      echo "Google Play services: ${gms:-NOT installed (use a Google Play emulator image)}"
    } | tee docs/device.txt ;;
  token)
    tok="$(adb logcat -d -s flutter | tr -d '\r' | grep -o 'FCM token[^:]*: [A-Za-z0-9_:-]*' | tail -1 | sed 's/.*: //')"
    if [ -z "$tok" ]; then
      echo "No token in the log yet. Wait for the app to finish starting (or press R in flutter run), then retry."
      exit 1
    fi
    printf '%s' "$tok" | pbcopy
    echo "Token copied to clipboard (${tok:0:8}...${tok: -6}, ${#tok} chars). Paste it into Firebase Console > Send test message." ;;
  shot)
    name="${2:?usage: fcm_helper.sh shot NAME}"
    adb exec-out screencap -p > "docs/screenshots/$name.png" && echo "Saved docs/screenshots/$name.png" ;;
  home)    adb shell input keyevent KEYCODE_HOME ;;
  shade)   adb shell cmd statusbar expand-notifications ;;
  recents) adb shell input keyevent KEYCODE_APP_SWITCH ;;
  *) sed -n '2,8p' "$0" | sed 's/^# \{0,1\}//' ;;
esac
