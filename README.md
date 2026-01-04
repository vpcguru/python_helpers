# python_helpers
Python helper scripts

## move-sort-files
Sorts and organizes files by their modification date into subdirectories. Works on both Windows and macOS.

**Requirements:** Python 3

**Usage:**
```
python ./move-sort-files/main.py <OriginalFolder> <DestFolder> <move_or_copy>
```

**Arguments:**
- `<OriginalFolder>` - Path to folder containing files to organize
- `<DestFolder>` - Path where organized files should be placed
- `<move_or_copy>` - `TRUE` to move files, `FALSE` to copy files

**Examples:**

Windows:
```
python ./move-sort-files/main.py g:\DCMI\ \\NAS\photo\2024\ TRUE
```

macOS/Linux:
```
python ./move-sort-files/main.py /Users/username/Pictures/Camera ~/Photos/Sorted TRUE
```