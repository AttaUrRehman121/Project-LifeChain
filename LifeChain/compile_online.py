#!/usr/bin/env python
"""
Online Translation Compiler Helper
This script helps you compile .po files to .mo files using online tools
since gettext is not installed locally.
"""

import os
import requests
import base64
import zipfile
import tempfile
import shutil

def create_online_compilation_guide():
    """Create a guide for online compilation"""
    
    print("🌐 Online Translation Compilation Guide")
    print("=" * 50)
    print()
    
    print("Since gettext is not installed locally, you can compile your translations online:")
    print()
    
    print("📋 Step 1: Prepare your .po files")
    print("   - English: locale/en/LC_MESSAGES/django.po")
    print("   - Urdu: locale/ur/LC_MESSAGES/django.po")
    print()
    
    print("🌐 Step 2: Use online compilation tools")
    print("   Option A: Poedit Online")
    print("   - Visit: https://poedit.net/online")
    print("   - Upload your .po file")
    print("   - Download the compiled .mo file")
    print()
    
    print("   Option B: Online .po to .mo converter")
    print("   - Visit: https://www.poedit.net/online")
    print("   - Or search for 'online po to mo converter'")
    print()
    
    print("📁 Step 3: Place compiled files")
    print("   - Put django.mo in locale/en/LC_MESSAGES/")
    print("   - Put django.mo in locale/ur/LC_MESSAGES/")
    print()
    
    print("🧪 Step 4: Test the system")
    print("   - Run: python manage.py runserver")
    print("   - Visit: http://localhost:8000/")
    print("   - Click language switcher to test")
    print()

def check_current_files():
    """Check what translation files currently exist"""
    
    print("📁 Current Translation Files Status")
    print("=" * 40)
    print()
    
    # Check English files
    en_po = "locale/en/LC_MESSAGES/django.po"
    en_mo = "locale/en/LC_MESSAGES/django.mo"
    
    if os.path.exists(en_po):
        print(f"✅ English .po file: {en_po}")
        po_size = os.path.getsize(en_po)
        print(f"   Size: {po_size} bytes")
    else:
        print(f"❌ English .po file missing: {en_po}")
    
    if os.path.exists(en_mo):
        print(f"✅ English .mo file: {en_mo}")
        mo_size = os.path.getsize(en_mo)
        print(f"   Size: {mo_size} bytes")
    else:
        print(f"❌ English .mo file missing: {en_mo}")
    
    print()
    
    # Check Urdu files
    ur_po = "locale/ur/LC_MESSAGES/django.po"
    ur_mo = "locale/ur/LC_MESSAGES/django.mo"
    
    if os.path.exists(ur_po):
        print(f"✅ Urdu .po file: {ur_po}")
        po_size = os.path.getsize(ur_po)
        print(f"   Size: {po_size} bytes")
    else:
        print(f"❌ Urdu .po file missing: {ur_po}")
    
    if os.path.exists(ur_mo):
        print(f"✅ Urdu .mo file: {ur_mo}")
        mo_size = os.path.getsize(ur_mo)
        print(f"   Size: {mo_size} bytes")
    else:
        print(f"❌ Urdu .mo file missing: {ur_mo}")
    
    print()

def create_compilation_script():
    """Create a batch script for easy compilation once gettext is installed"""
    
    script_content = """@echo off
REM Translation Compilation Script
REM Run this after installing gettext

echo Compiling English translations...
python manage.py compilemessages --locale en

echo.
echo Compiling Urdu translations...
python manage.py compilemessages --locale ur

echo.
echo Compilation complete!
echo Check the locale/*/LC_MESSAGES/ directories for .mo files
pause
"""
    
    with open("compile_translations.bat", "w") as f:
        f.write(script_content)
    
    print("📝 Created compile_translations.bat script")
    print("   Run this after installing gettext")

def main():
    """Main function"""
    
    print("🚀 LifeChain Translation Compilation Helper")
    print("=" * 50)
    print()
    
    # Check current files
    check_current_files()
    
    # Create online compilation guide
    create_online_compilation_guide()
    
    # Create compilation script
    create_compilation_script()
    
    print("🎯 Next Steps:")
    print("1. Install gettext using one of the methods above")
    print("2. Or use online compilation tools")
    print("3. Once .mo files are created, test the language system")
    print()
    
    print("💡 Quick Test (without full translation):")
    print("   - The language switcher will work for session-based switching")
    print("   - Full content translation requires compiled .mo files")
    print()
    
    print("🔗 Useful Links:")
    print("   - Chocolatey: https://chocolatey.org/install")
    print("   - gettext for Windows: https://mlocati.github.io/articles/gettext-iconv-windows.html")
    print("   - Poedit Online: https://poedit.net/online")

if __name__ == "__main__":
    main()
