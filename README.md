# 📚 Study Buddy v0.1.1-BETA

Study Buddy is a terminal-based study helper with a large question bank (~800+ questions auto-expanded).  
This is the **v0.1.1-BETA release**.

⚠️ **Note:**  
Currently, only a **Linux version** is available.  
A **Windows version** is in the works, and a possible **macOS version** may come later.

---

## 🚀 How to Run (Linux)

1. **Download the latest release** from this repository.
2. Extract the files (you should have two items):
   - `study-buddy-v0.1.1-BETA` (the executable)
   - `StudyBuddyLauncher.desktop` (the launcher file)

---

### 🔧 Important Notes About the `.desktop` File

- The launcher **must be named with the `.desktop` extension**, for example:
  ```
  StudyBuddyLauncher.desktop
  ```
- Do **NOT** save it as `.txt` (e.g. `StudyBuddyLauncher.txt`) — otherwise your desktop environment won’t recognize it as an application.

---

### ⚙️ Editing the `.desktop` File

1. Open `StudyBuddyLauncher.desktop` in a text editor.  
   You’ll see a line like this:

   ```ini
   Exec=/your/path/to/study-buddy-v0.1.1-BETA
   ```

2. Change `/your/path/to/` to the **full path** of where you extracted the program.  
   For example, if you put it in `~/Desktop/StudyBuddy/`, then update it to:

   ```ini
   Exec=/home/yourusername/Desktop/StudyBuddy/study-buddy-v0.1.1-BETA
   ```

---

### 🖥️ Making the `.desktop` File Executable

Run the following command in your terminal:

```bash
chmod +x /path/to/StudyBuddyLauncher.desktop
```

Example (if it’s on your Desktop):

```bash
chmod +x ~/Desktop/StudyBuddyLauncher.desktop
```

---

## 🎮 Running the Program

- Double-click `StudyBuddyLauncher.desktop` in your file manager (e.g. Dolphin, Nautilus).
- Or run directly from the terminal:

```bash
./study-buddy-v0.1.1-BETA
```

---

## 📌 Current Roadmap

- [x] Linux binary (v0.1.1-BETA)
- [ ] Windows build (working on it)
- [ ] macOS build (maybe, if I get access to a mac or vm)

---

## 📝 License

This project is still in **beta**. License to be decided later.
