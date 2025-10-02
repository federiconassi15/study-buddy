# Study Buddy v0.1.1-BETA

**Note:** For now, there is only a Linux version and a Windows version. A macOS version may come in the future, but it's not confirmed yet.

## Current Versions

- Linux: `study-buddy-v0.1.1-BETA-linux`  
- Windows: `study-buddy-v0.1.1-BETA-x86_64bit.exe`

---

## Linux Installation

1. Download `study-buddy-v0.1.1-BETA-linux` and place it in a folder of your choice.  
2. Create a `.desktop` file (plain text) on your Desktop (or wherever you want). Example:

```ini
[Desktop Entry]
Type=Application
Name=Study Buddy
Exec=/your/path/to/study-buddy-v0.1.1-BETA-linux
Icon=study-buddy
Terminal=true
Categories=Education;
```

3. **Important:** Change the `Exec=` line to the **full path** where you placed the Linux executable. For example:

```ini
Exec=/home/yourusername/Downloads/study-buddy-v0.1.1-BETA-linux
```

4. Make the `.desktop` file executable:

```bash
chmod +x /path/to/study-buddy-v0.1.1-BETA.desktop-linux
```

5. You can now double-click the `.desktop` file to run the application.

---

## Windows Installation

1. Download `study-buddy-v0.1.1-BETA-x86_64bit.exe`.  
2. Double-click the `.exe` file to run it.  
3. (Optional) Create a shortcut on your Desktop for easy access.

---

## Notes

- Linux users must have the executable permission set and correct paths in the `.desktop` file.  
- Windows users can run the `.exe` directly; no additional configuration is needed.  
- This is a BETA version; expect possible bugs or missing features.  
- Future releases may include macOS support.

