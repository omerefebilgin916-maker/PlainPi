# PlainPiStudio.py - Modern IDE for PlainPi
# DUZELTME #3: Syntax + Auto-Complete tek fonksiyonda birlestirildi

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import re

class PlainPiStudio:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PlainPi Studio")
        self.root.geometry("1400x900")
        self.root.configure(bg="#1e1e1e")

        self.current_file = None
        self.autocomplete_window = None
        self.current_template = None
        self.create_ui()

    def create_ui(self):
        # Menu Bar
        self.create_menu()

        # Main Container
        main_frame = tk.Frame(self.root, bg="#1e1e1e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left Panel (Editor + Console)
        left_frame = tk.Frame(main_frame, bg="#1e1e1e")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.create_editor(left_frame)
        self.create_console(left_frame)

        # Right Panel (Preview + PlainPiW)
        right_frame = tk.Frame(main_frame, bg="#1e1e1e")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        self.create_preview(right_frame)
        self.create_plainpiw_panel(right_frame)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Run Menu
        run_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Run", menu=run_menu)
        run_menu.add_command(label="Run PlainPi", command=self.run_plainpi, accelerator="F5")
        run_menu.add_command(label="Export Web", command=self.export_web, accelerator="Ctrl+E")

        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

        # Shortcuts
        self.root.bind("<F5>", lambda e: self.run_plainpi())
        self.root.bind("<Control-e>", lambda e: self.export_web())

    def create_editor(self, parent):
        # Editor Header
        header = tk.Label(parent, text="📝 Code Editor", bg="#2d2d2d", fg="white", 
                         font=("Arial", 12, "bold"), pady=5)
        header.pack(fill=tk.X, pady=(0, 5))

        # Editor Frame
        editor_frame = tk.Frame(parent, bg="#2d2d2d")
        editor_frame.pack(fill=tk.BOTH, expand=True)

        # Line Numbers
        self.line_numbers = tk.Text(editor_frame, width=4, bg="#1e1e1e", fg="#666", 
                                   font=("Consolas", 12), state=tk.DISABLED, wrap=tk.NONE)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Code Editor
        self.editor = tk.Text(editor_frame, bg="#2d2d2d", fg="white", font=("Consolas", 12),
                             insertbackground="white", selectbackground="#4CAF50", wrap=tk.NONE)
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(editor_frame, command=self.editor.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.editor.config(yscrollcommand=scrollbar.set)

        # DUZELTME #3: Tek fonksiyon (Syntax + Auto-Complete)
        self.editor.bind("<KeyRelease>", self.on_key_release)
        self.editor.bind("<Tab>", self.insert_autocomplete)

    def create_console(self, parent):
        # Console Header
        header = tk.Label(parent, text="💻 Console", bg="#2d2d2d", fg="white", 
                         font=("Arial", 12, "bold"), pady=5)
        header.pack(fill=tk.X, pady=(10, 5))

        # Console
        self.console = tk.Text(parent, bg="#1e1e1e", fg="#4CAF50", font=("Consolas", 10),
                              state=tk.DISABLED, height=8)
        self.console.pack(fill=tk.X)

    def create_preview(self, parent):
        # Preview Header
        header = tk.Label(parent, text="👁️ Live Preview", bg="#2d2d2d", fg="white", 
                         font=("Arial", 12, "bold"), pady=5)
        header.pack(fill=tk.X, pady=(0, 5))

        # Preview Canvas
        self.preview = tk.Canvas(parent, bg="#1e1e1e", highlightthickness=2, 
                                highlightbackground="#4CAF50")
        self.preview.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Preview Info
        info = tk.Label(parent, text="Click F5 to run PlainPi", bg="#2d2d2d", fg="#888", 
                       font=("Arial", 9))
        info.pack(fill=tk.X, pady=(5, 0))

    def create_plainpiw_panel(self, parent):
        # PlainPiW Header
        header = tk.Label(parent, text="🌐 PlainPiW (Web Export)", bg="#2d2d2d", fg="white", 
                         font=("Arial", 12, "bold"), pady=5)
        header.pack(fill=tk.X, pady=(10, 5))

        # Buttons
        btn_frame = tk.Frame(parent, bg="#2d2d2d")
        btn_frame.pack(fill=tk.X)

        export_btn = tk.Button(btn_frame, text="Export to HTML", bg="#4CAF50", fg="white",
                              font=("Arial", 10), command=self.export_web)
        export_btn.pack(fill=tk.X, pady=2)

        open_btn = tk.Button(btn_frame, text="Open in Browser", bg="#2196F3", fg="white",
                            font=("Arial", 10), command=self.open_in_browser)
        open_btn.pack(fill=tk.X, pady=2)

        # Info
        info = tk.Label(parent, text="PlainPiW converts .pi to HTML/CSS", bg="#2d2d2d", 
                       fg="#888", font=("Arial", 9))
        info.pack(fill=tk.X, pady=(10, 0))

    # DUZELTME #3: Tek fonksiyon (Syntax + Auto-Complete)
    def on_key_release(self, event=None):
        if event.keysym in ["Tab", "Escape"]:
            return

        # Syntax Highlighting
        self.update_syntax()

        # Auto-Complete
        self.check_autocomplete(event)

    def update_syntax(self):
        code = self.editor.get("1.0", tk.END)

        keywords = ["Sprite:", "Move:", "Sound:", "Window:", "Text:", "Button:", "Input:", "Link:",
                   "Set:", "Add:", "Subtract:", "Multiply:", "Divide:", "Mod:",
                   "If:", "Else:", "EndIf:", "For:", "EndFor:", "While:", "EndWhile:",
                   "Repeat:", "EndRepeat:", "Function:", "EndFunction:", "Call:",
                   "Try:", "Except:", "EndTry:", "Print:", "Message:", "Background:"]

        # Clear old tags
        self.editor.tag_remove("keyword", "1.0", tk.END)

        for keyword in keywords:
            start = "1.0"
            while True:
                pos = self.editor.search(keyword, start, tk.END)
                if not pos:
                    break
                end = f"{pos}+{len(keyword)}c"
                self.editor.tag_add("keyword", pos, end)
                self.editor.tag_config("keyword", foreground="#4CAF50")
                start = end

    def check_autocomplete(self, event=None):
        if event.keysym in ["Return", "Tab", "Escape"]:
            return

        # Get current line
        pos = self.editor.index(tk.INSERT)
        line_num = int(pos.split(".")[0])
        line_start = f"{line_num}.0"
        line_end = f"{line_num}.end"
        current_line = self.editor.get(line_start, line_end)

        # Get last word
        words = current_line.split()
        if not words:
            return
        last_word = words[-1]

        # Auto-complete templates
        templates = {
            "Spr": "Sprite:[player.png] | Name:[Player] | In:[Main] | Locate:[100,100]",
            "Mov": "Move:[Player] | To:[300,100] | Speed:[5]",
            "Sou": "Sound:[click.wav] | Type:[sfx]",
            "Win": "Window:[My Game] | Size:[800,600]",
            "Tex": "Text:[Hello World] | Name:[Title] | In:[Main] | Locate:[50,50]",
            "But": "Button:[Click Me] | Name:[Btn1] | In:[Main] | Locate:[50,100]",
            "Inp": "Input:[Enter text...] | Name:[Input1] | In:[Main] | Locate:[50,150]",
            "Lin": "Link:[https://google.com] | Name:[Google] | In:[Main] | Locate:[50,200]",
            "Set": "Set:[x] | To:[10]",
            "Add": "Add:[x] | By:[5]",
            "If:": "If:[x>5]",
            "For": "For:[i] | From:[0] | To:[10]",
            "Rep": "Repeat:[3]",
            "Fun": "Function:[MyFunc]",
            "Pri": "Print:[Hello World]",
            "Mes": "Message:[Hello] | Type:[info]",
            "Back": "Background:[#2d5a27]"
        }

        # Show autocomplete popup
        if len(last_word) >= 2:
            for prefix, template in templates.items():
                if last_word.startswith(prefix):
                    self.show_autocomplete_popup(template, line_num, len(current_line))
                    break

    def show_autocomplete_popup(self, template, line_num, x_pos):
        # Close existing popup
        if self.autocomplete_window:
            self.autocomplete_window.destroy()

        # Create popup
        self.autocomplete_window = tk.Toplevel(self.root)
        self.autocomplete_window.overrideredirect(True)

        # Position
        x = self.root.winfo_x() + 100
        y = self.root.winfo_y() + 200
        self.autocomplete_window.geometry(f"+{x}+{y}")

        # Frame
        frame = tk.Frame(self.autocomplete_window, bg="#4CAF50", bd=2)
        frame.pack()

        # Label
        label = tk.Label(frame, text=f"Press Tab: {template[:50]}...", 
                        bg="#4CAF50", fg="white", font=("Consolas", 10))
        label.pack(padx=10, pady=5)

        # Store template
        self.current_template = template

        # Close on click
        self.autocomplete_window.bind("<Button-1>", lambda e: self.close_autocomplete())
        self.root.after(3000, self.close_autocomplete)

    def close_autocomplete(self):
        if self.autocomplete_window:
            self.autocomplete_window.destroy()
            self.autocomplete_window = None

    def insert_autocomplete(self, event=None):
        if self.current_template:
            # Get current line
            pos = self.editor.index(tk.INSERT)
            line_num = int(pos.split(".")[0])
            line_start = f"{line_num}.0"
            line_end = f"{line_num}.end"
            current_line = self.editor.get(line_start, line_end)

            # Replace last word with template
            words = current_line.split()
            if words:
                last_word = words[-1]
                start_pos = current_line.rfind(last_word)
                self.editor.delete(f"{line_num}.{start_pos}", line_end)
                self.editor.insert(tk.INSERT, self.current_template)

            self.close_autocomplete()
            return "break"

        return None

    def log(self, message):
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END, message + "\n")
        self.console.config(state=tk.DISABLED)
        self.console.see(tk.END)

    def new_file(self):
        self.editor.delete("1.0", tk.END)
        self.current_file = None
        self.log("✅ New file created")

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PlainPi Files", "*.pi"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
            self.editor.delete("1.0", tk.END)
            self.editor.insert("1.0", code)
            self.current_file = file_path
            self.log(f"✅ Opened: {file_path}")

    def save_file(self):
        if self.current_file:
            code = self.editor.get("1.0", tk.END)
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(code)
            self.log(f"✅ Saved: {self.current_file}")
        else:
            file_path = filedialog.asksaveasfilename(defaultextension=".pi", 
                                                    filetypes=[("PlainPi Files", "*.pi")])
            if file_path:
                code = self.editor.get("1.0", tk.END)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(code)
                self.current_file = file_path
                self.log(f"✅ Saved: {file_path}")

    def run_plainpi(self):
        code = self.editor.get("1.0", tk.END)
        self.log("▶️ Running PlainPi...")

        try:
            import PlainPi
            PlainPi.run_plainpi(code)
            self.log("✅ PlainPi executed successfully")
        except Exception as e:
            self.log(f"❌ Error: {e}")

    def export_web(self):
        code = self.editor.get("1.0", tk.END)
        self.log("🌐 Exporting to HTML...")

        try:
            import PlainPiW
            piw = PlainPiW.PlainPiW()
            piw.parse(code)
            output_file = piw.export_html("exported_website.html")
            self.log(f"✅ Web exported: {output_file}")
        except Exception as e:
            self.log(f"❌ Error: {e}")

    def open_in_browser(self):
        import webbrowser
        if os.path.exists("exported_website.html"):
            webbrowser.open("exported_website.html")
            self.log("🌐 Opened in browser")
        else:
            self.log("❌ No exported website found. Click 'Export to HTML' first.")

    def show_about(self):
        messagebox.showinfo("About", "PlainPi Studio\nModern IDE for PlainPi\n\nCreate games and websites with ease!")

    def run(self):
        # Load example code
        example = """Window:[PlainPi Demo] | Size:[800,600]
Background:[#2d5a27]
Sprite:[player.png] | Name:[Player] | In:[Main] | Locate:[100,100]
Move:[Player] | To:[300,100] | Speed:[5]
Sound:[click.wav] | Type:[sfx]
Text:[Hello PlainPi!] | Name:[Title] | In:[Main] | Locate:[100,50]
Button:[Click Me!] | Name:[Btn1] | In:[Main] | Locate:[100,150]
Input:[Enter name...] | Name:[Input1] | In:[Main] | Locate:[100,200]
Link:[https://google.com] | Name:[Google] | In:[Main] | Locate:[100,250]"""

        self.editor.insert("1.0", example)
        self.log("✅ PlainPi Studio Ready!")

        self.root.mainloop()


if __name__ == "__main__":
    studio = PlainPiStudio()
    studio.run()
