# 🍪 PlainPi v2 - Easy, Simple, and Fast

**PlainPi** is a simple, fast, and powerful programming language written in Python. You can easily create games, websites, and desktop applications!

---

## ✨ Features

- 🎮 **Game Engine** - Sprites, movement, sound effects
- 🌐 **Web Export** - HTML/CSS output
- 🖥️ **Desktop GUI** - Buttons, inputs, menus, tabs
- 🔧 **Full Featured** - Variables, loops, functions, error handling
- 🎨 **IDE** - Auto-complete, syntax highlighting, live preview

---

## 🚀 Installation

### 1. Install Python (3.8+)
[python.org](https://www.python.org/downloads/)

### 2. Download PlainPi
```bash
git clone https://github.com/user/PlainPi.git
cd PlainPi
```

### 3. Install Dependencies
```bash
pip install pillow
```

---

## 📁 Files
📁 PlainPi/
├── PlainPi.py # Main engine
├── PlainPiStudio.py # IDE
├── PlainPiW.py # Web export
├── main.pi # Example code
├── player.png # Sprite image
├── click.wav # Sound effect
└── music.mp3 # Music

---

## 🎯 Usage

### Run PlainPi Code
```bash
python PlainPi.py main.pi
```

### Start IDE
```bash
python PlainPiStudio.py
```

### Create .exe
```bash
pip install pyinstaller
python -m PyInstaller --onefile --windowed --name PlainPi PlainPi.py
python -m PyInstaller --onefile --windowed --name PlainPiStudio PlainPiStudio.py
```

---

## 📝 Commands

### Basic Commands

| Command | Description | Example |
|---|---|---|
| `Window` | Create window | `Window:[Game] \| Size:[800,600]` |
| `Background` | Background color | `Background:[#2d5a27]` |
| `Sprite` | Add image/object | `Sprite:[player.png] \| Name:[Player] \| Locate:[100,100]` |
| `Move` | Move sprite | `Move:[Player] \| To:[300,100] \| Speed:[5]` |
| `Sound` | Play sound | `Sound:[click.wav] \| Type:[sfx]` |

### GUI Commands

| Command | Description | Example |
|---|---|---|
| `Text` | Show text | `Text:[Hello] \| Name:[Title] \| Locate:[50,50]` |
| `Button` | Add button | `Button:[Click] \| Name:[Btn1] \| Locate:[50,100]` |
| `Input` | Text input | `Input:[Enter...] \| Name:[Input1] \| Locate:[50,150]` |
| `Link` | Web link | `Link:[https://...] \| Name:[Google] \| Content:[Go] \| Locate:[50,200]` |
| `Image` | Show image | `Image:[pic.png] \| Width:[100] \| Locate:[0,0]` |
| `Canvas` | Drawing area | `Canvas:[Name] \| Width:[400] \| Height:[300]` |
| `List` | List box | `List:[A;B;C] \| Name:[List1]` |
| `Check` | Checkbox | `Check:[Accept] \| Name:[Check1]` |
| `Radio` | Radio button | `Radio:[Option1] \| Group:[grp]` |
| `Slider` | Slider | `Slider:[Name] \| From:[0] \| To:[100]` |
| `Progressbar` | Progress bar | `Progressbar:[Name] \| Length:[200]` |
| `Tab` | Tab menu | `Tab:[Name] \| Width:[400]` |
| `Menu` | Menu bar | `Menu:[File:New;Edit:Copy]` |

### Variables & Math

| Command | Description | Example |
|---|---|---|
| `Set` | Set variable | `Set:[x] \| To:[10]` |
| `Get` | Get variable | `Get:[Input1] \| To:[var]` |
| `Add` | Add | `Add:[x] \| By:[5]` |
| `Subtract` | Subtract | `Subtract:[x] \| By:[3]` |
| `Multiply` | Multiply | `Multiply:[x] \| By:[2]` |
| `Divide` | Divide | `Divide:[x] \| By:[2]` |
| `Mod` | Modulo | `Mod:[x] \| By:[3]` |

### Control Structures

| Command | Description | Example |
|---|---|---|
| `If/Else/EndIf` | Condition | `If:[x>5]` ... `Else:` ... `EndIf:` |
| `For/EndFor` | For loop | `For:[i] \| From:[0] \| To:[10]` ... `EndFor:` |
| `While/EndWhile` | While loop | `While:[x<10]` ... `EndWhile:` |
| `Repeat/EndRepeat` | Repeat | `Repeat:[3]` ... `EndRepeat:` |

### Functions

| Command | Description | Example |
|---|---|---|
| `Function/EndFunction` | Define function | `Function:[MyFunc]` ... `EndFunction:` |
| `Call` | Call function | `Call:[MyFunc] \| Args:[1,2,3]` |

### Error Handling

| Command | Description | Example |
|---|---|---|
| `Try/Except/EndTry` | Error handling | `Try:` ... `Except:` ... `EndTry:` |

### File Operations

| Command | Description | Example |
|---|---|---|
| `ReadFile` | Read file | `ReadFile:[data.txt] \| To:[content]` |
| `WriteFile` | Write file | `WriteFile:[data.txt] \| Content:[Hello]` |
| `AppendFile` | Append file | `AppendFile:[log.txt] \| Content:[New line]` |
| `MakeFolder` | Create folder | `MakeFolder:[test]` |
| `ListFolder` | List folder | `ListFolder:[.] \| To:[files]` |

### Time & Random

| Command | Description | Example |
|---|---|---|
| `Now` | Current date | `Now:[now] \| Format:[%Y-%m-%d]` |
| `FormatDate` | Format date | `FormatDate:[2024-01-01] \| Format:[%Y] \| To:[year]` |
| `Random` | Random number | `Random:[0] \| To:[100] \| To:[rand]` |
| `Delay` | Wait (ms) | `Delay:[1000]` |

### Other Commands

| Command | Description | Example |
|---|---|---|
| `Print` | Print to console | `Print:[Hello World]` |
| `Message` | Message box | `Message:[Hello] \| Type:[info]` |
| `Change` | Change widget | `Change:[Label1] \| To:[New Text]` |
| `Clear` | Clear widget | `Clear:[Canvas1]` |
| `Dict` | Create dict | `Dict:[data] \| Data:[key:value]` |
| `ParseJSON` | Parse JSON | `ParseJSON:[{...}] \| To:[obj]` |
| `Import` | Import module | `Import:[math]` |
| `Exit` | Exit program | `Exit:` |

---

## 🎮 Examples

### 1. Simple Game
```text
Window:[Game] | Size:[800,600]
Background:[#2d5a27]

Sprite:[player.png] | Name:[Player] | Locate:[100,100]
Move:[Player] | To:[300,100] | Speed:
Sound:[click.wav] | Type:[sfx]

Text:[Score: 0] | Name:[Score] | Locate:[10,10]
Button:[Start] | Name:[StartBtn] | Locate:[10,50]
```

### 2. Website
```text
Sprite:[header.png] | Name:[Header] | Locate:[0,0]
Text:[Welcome] | Name:[Title] | Locate:[50,100]
Button:[Click] | Name:[Btn1] | Locate:[50,150]
Input:[Your Name] | Name:[Input1] | Locate:[50,200]
Link:[https://google.com] | Name:[Google] | Content:[Go to Google] | Locate:[50,250]
```

### 3. Calculator
```text
Window:[Calculator] | Size:[300,400]

Input:[Number 1] | Name:[Input1] | Locate:[50,50]
Input:[Number 2] | Name:[Input2] | Locate:[50,100]
Button:[Add] | Name:[AddBtn] | Locate:[50,150]
Button:[Subtract] | Name:[SubBtn] | Locate:[150,150]

Set:[result] | To:
```

### 4. Loop Example
```text
Set:[x] | To:
For:[i] | From: | To:
Add:[x] | By:[i]
Print:[x = ${x}]
EndFor:
```

### 5. If-Else Example
```text
Set:[age] | To:
If:[age >= 18]
Message:[You are an adult!] | Type:[info]
Else:
Message:[You are a child!] | Type:[warning]
EndIf:
```

---

## 🛠️ IDE Features

- ✅ **Auto-Complete** - Type `Spr`, press `Tab`
- ✅ **Syntax Highlighting** - Colorful code
- ✅ **Live Preview** - Instant preview
- ✅ **Web Export** - HTML/CSS output
- ✅ **Keyboard Shortcuts** - `F5` (Run), `Ctrl+E` (Export)

---

## 📊 Version History

### v2 (2024)
- ✅ Game engine
- ✅ Web export
- ✅ IDE
- ✅ 50+ commands
- ✅ 4 critical bug fixes

### v1 (2023)
- ✅ Desktop GUI
- ✅ Variables, loops
- ✅ File operations

---

## 🤝 Contributing

1. Fork it
2. Create your feature branch (`git checkout -b feature/NewFeature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 📬 Contact

- GitHub: [@user](https://github.com/user)
- Email: info@plainpi.com
- Website: [plainpi.com](https://plainpi.com)

---

**Coding is easier with PlainPi! 🍪**
