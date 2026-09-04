# PlainPi.py - PlainPi v2 (FINAL + 4 HATA DUZELTILDI)
# 1. Sonsuz Blok Kilitlenmesi
# 2. Parametre Ayristirma
# 3. String Degerleri Otomatik Tirnak
# 4. If Kontrolu String Duzeltme

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import json
import os
import sys
import time
import math
import random
from datetime import datetime
import winsound
import re


class PlainPiWindow:
    def __init__(self, title="PlainPi", width=800, height=600, bg_color="#1e1e1e"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        self.root.configure(bg=bg_color)
        
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg=bg_color, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.sprites = {}
        self.widgets = {}
        self.variables = {}
        self.functions = {}
        self.image_cache = {}
        self.widget_counter = 0
        self.loop_stack = []
        
    def resolve(self, value):
        if not isinstance(value, str):
            return value
        while "${" in value:
            start = value.find("${")
            end = value.find("}", start)
            if end == -1:
                break
            var_name = value[start+2:end]
            var_value = str(self.variables.get(var_name, ""))
            if isinstance(var_value, str) and var_value.startswith('"') and var_value.endswith('"'):
                var_value = var_value.strip('"')
            value = value[:start] + var_value + value[end+1:]
        return value
    
    def parse_params(self, line):
        params = {}
        parts = line.split("|")
        for part in parts:
            part = part.strip()
            if ":" in part:
                key, value = part.split(":", 1)
                key = key.strip().lower()
                value = value.strip()
                match = re.search(r"\[([^\]]+)\]", value)
                if match:
                    value = match.group(1)
                params[key] = value
        return params
    
    def add_sprite(self, name, x, y, width=50, height=50, color="red", image=None):
        image = self.resolve(image) if image else None
        if image and os.path.exists(image):
            try:
                img = Image.open(image).resize((width, height), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                sprite = self.canvas.create_image(x, y, anchor=tk.NW, image=photo)
                self.sprites[name] = {"id": sprite, "x": x, "y": y, "photo": photo}
            except:
                sprite = self.canvas.create_rectangle(x, y, x+width, y+height, fill=color, outline="")
                self.sprites[name] = {"id": sprite, "x": x, "y": y, "width": width, "height": height}
        else:
            sprite = self.canvas.create_rectangle(x, y, x+width, y+height, fill=color, outline="")
            self.sprites[name] = {"id": sprite, "x": x, "y": y, "width": width, "height": height}
        
        label = self.canvas.create_text(x, y-5, text=name, fill="white", anchor=tk.S, font=("Arial", 10))
        self.sprites[name]["label"] = label
    
    def move_sprite(self, name, to_x, to_y, speed=5):
        if name not in self.sprites:
            return
        sprite_data = self.sprites[name]
        dx = to_x - sprite_data["x"]
        dy = to_y - sprite_data["y"]
        dist = (dx**2 + dy**2)**0.5
        steps = int(dist / speed) if speed > 0 else 1
        step_x = dx / steps
        step_y = dy / steps
        
        def animate(step=0):
            if step >= steps:
                sprite_data["x"] = to_x
                sprite_data["y"] = to_y
                return
            self.canvas.move(sprite_data["id"], step_x, step_y)
            self.canvas.move(sprite_data["label"], step_x, step_y)
            sprite_data["x"] += step_x
            sprite_data["y"] += step_y
            self.root.after(16, lambda: animate(step+1))
        animate()
    
    def create_widget_id(self, name):
        self.widget_counter += 1
        return f"{name}_{self.widget_counter}"
    
    def execute_lines(self, lines, start=0, end=None):
        if end is None:
            end = len(lines)
        i = start
        while i < end:
            line = lines[i].strip()
            if self.loop_stack and self.loop_stack[-1]["type"] == "if":
                if not self.loop_stack[-1]["result"] and not self.loop_stack[-1]["executed"]:
                    if line.lower().startswith("else:"):
                        self.loop_stack[-1]["executed"] = True
                    elif line.lower().startswith("endif:"):
                        self.loop_stack.pop()
                    i += 1
                    continue
                elif line.lower().startswith("else:"):
                    i += 1
                    continue
                elif line.lower().startswith("endif:"):
                    self.loop_stack.pop()
                    i += 1
                    continue
            if not line or line.startswith("#"):
                i += 1
                continue
            skip = self.execute_line(line, lines, i)
            if skip:
                i = skip
            else:
                i += 1
    
    def execute_line(self, line, all_lines=None, current_index=0):
        line = self.resolve(line)
        if not line.strip() or line.strip().startswith("#"):
            return False
        
        params = self.parse_params(line)
        cmd = line.split(":")[0].strip().lower()
        
        if cmd == "if":
            condition = params.get("if", "")
            try:
                eval_vars = {}
                for k, v in self.variables.items():
                    if isinstance(v, str) and v.startswith('"') and v.endswith('"'):
                        eval_vars[k] = v.strip('"')
                    else:
                        eval_vars[k] = v
                result = eval(condition, {"__builtins__": {}}, eval_vars)
                self.loop_stack.append({"type": "if", "result": bool(result), "executed": False})
            except:
                self.loop_stack.append({"type": "if", "result": False, "executed": False})
            return False
        elif cmd == "else":
            if self.loop_stack and self.loop_stack[-1]["type"] == "if":
                self.loop_stack[-1]["executed"] = not self.loop_stack[-1]["result"]
            return False
        elif cmd == "endif":
            if self.loop_stack and self.loop_stack[-1]["type"] == "if":
                self.loop_stack.pop()
            return False
        elif cmd == "for":
            var = params.get("for", "i")
            from_val = int(params.get("from", "0"))
            to_val = int(params.get("to", "10"))
            self.loop_stack.append({"type": "for", "var": var, "from": from_val, "to": to_val, "current": from_val, "start_line": current_index + 1})
            self.variables[var] = from_val
            return False
        elif cmd == "endfor":
            if self.loop_stack and self.loop_stack[-1]["type"] == "for":
                loop = self.loop_stack[-1]
                loop["current"] += 1
                if loop["current"] <= loop["to"]:
                    self.variables[loop["var"]] = loop["current"]
                    return loop["start_line"]
                else:
                    self.loop_stack.pop()
            return False
        elif cmd == "while":
            condition = params.get("while", "")
            self.loop_stack.append({"type": "while", "condition": condition, "start_line": current_index + 1})
            return False
        elif cmd == "endwhile":
            if self.loop_stack and self.loop_stack[-1]["type"] == "while":
                loop = self.loop_stack[-1]
                try:
                    result = eval(loop["condition"], {"__builtins__": {}}, self.variables)
                    if result:
                        return loop["start_line"]
                    else:
                        self.loop_stack.pop()
                except:
                    self.loop_stack.pop()
            return False
        elif cmd == "repeat":
            times = int(params.get("repeat", "1"))
            self.loop_stack.append({"type": "repeat", "times": times, "current": 0, "start_line": current_index + 1})
            return False
        elif cmd == "endrepeat":
            if self.loop_stack and self.loop_stack[-1]["type"] == "repeat":
                loop = self.loop_stack[-1]
                loop["current"] += 1
                if loop["current"] < loop["times"]:
                    return loop["start_line"]
                else:
                    self.loop_stack.pop()
            return False
        elif cmd == "function":
            func_name = params.get("function", "")
            body = []
            i = current_index + 1
            while i < len(all_lines) and not all_lines[i].strip().lower().startswith("endfunction"):
                body.append(all_lines[i])
                i += 1
            self.functions[func_name] = body
            return i
        elif cmd == "endfunction":
            return False
        elif cmd == "call":
            func_name = params.get("call", "")
            args = params.get("args", "").split(",")
            if func_name in self.functions:
                for i, arg in enumerate(args):
                    self.variables[f"arg{i+1}"] = arg.strip()
                self.execute_lines(self.functions[func_name])
            return False
        elif cmd == "try":
            self.loop_stack.append({"type": "try", "error": False})
            return False
        elif cmd == "except":
            return False
        elif cmd == "endtry":
            if self.loop_stack and self.loop_stack[-1]["type"] == "try":
                self.loop_stack.pop()
            return False
        
        handler = getattr(self, f"cmd_{cmd}", None)
        if handler:
            try:
                handler(params)
            except Exception as e:
                if self.loop_stack and self.loop_stack[-1]["type"] == "try":
                    self.loop_stack[-1]["error"] = True
                else:
                    print(f"Error in {cmd}: {e}")
        else:
            print(f"Unknown command: {cmd}")
        return False
    
    def cmd_text(self, params):
        text = self.resolve(params.get("text", "Hello"))
        name = self.resolve(params.get("name", f"label_{self.widget_counter}"))
        color = self.resolve(params.get("color", "white"))
        size = int(self.resolve(params.get("size", "12")))
        font = self.resolve(params.get("font", "Arial"))
        locate = params.get("locate", "0,0")
        label = tk.Label(self.root, text=text, bg=self.root.cget("bg"), fg=color, font=(font, size))
        x, y = map(int, locate.split(","))
        label.place(x=x, y=y)
        self.widgets[name] = label
    
    def cmd_button(self, params):
        text = self.resolve(params.get("button", "Click"))
        bg = self.resolve(params.get("background", "#4CAF50"))
        fg = self.resolve(params.get("color", "white"))
        width = int(self.resolve(params.get("width", "10")))
        height = int(self.resolve(params.get("height", "1")))
        locate = params.get("locate", "0,0")
        btn = tk.Button(self.root, text=text, bg=bg, fg=fg, width=width, height=height)
        x, y = map(int, locate.split(","))
        btn.place(x=x, y=y)
        name = self.create_widget_id("button")
        self.widgets[name] = btn
    
    def cmd_input(self, params):
        default = self.resolve(params.get("input", "Enter text"))
        name = self.resolve(params.get("name", f"entry_{self.widget_counter}"))
        width = int(self.resolve(params.get("width", "20")))
        locate = params.get("locate", "0,0")
        password = params.get("password", "false").lower() == "true"
        entry = tk.Entry(self.root, width=width, show="*" if password else "")
        entry.insert(0, default)
        x, y = map(int, locate.split(","))
        entry.place(x=x, y=y)
        self.widgets[name] = entry
    
    def cmd_image(self, params):
        path = self.resolve(params.get("path", ""))
        width = int(self.resolve(params.get("width", "100")))
        height = int(self.resolve(params.get("height", "100")))
        locate = params.get("locate", "0,0")
        if path in self.image_cache:
            img_tk = self.image_cache[path]
        else:
            img = Image.open(path).resize((width, height), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            self.image_cache[path] = img_tk
        label = tk.Label(self.root, image=img_tk, bg=self.root.cget("bg"))
        label.image = img_tk
        x, y = map(int, locate.split(","))
        label.place(x=x, y=y)
        name = self.create_widget_id("image")
        self.widgets[name] = label
    
    def cmd_canvas(self, params):
        width = int(self.resolve(params.get("width", "400")))
        height = int(self.resolve(params.get("height", "300")))
        name = self.resolve(params.get("name", f"canvas_{self.widget_counter}"))
        locate = params.get("locate", "0,0")
        canvas = tk.Canvas(self.root, width=width, height=height, bg="white")
        x, y = map(int, locate.split(","))
        canvas.place(x=x, y=y)
        self.widgets[name] = canvas
    
    def cmd_set(self, params):
        name = self.resolve(params.get("set", ""))
        value = self.resolve(params.get("to", ""))
        try:
            self.variables[name] = int(value)
        except:
            try:
                self.variables[name] = float(value)
            except:
                self.variables[name] = f'"{value}"'
                self.variables[f"{name}_str"] = value
    
    def cmd_get(self, params):
        widget_name = self.resolve(params.get("get", ""))
        to_var = self.resolve(params.get("to", ""))
        widget = self.widgets.get(widget_name)
        if isinstance(widget, tk.Entry):
            self.variables[to_var] = widget.get()
        elif isinstance(widget, tk.Listbox):
            selection = widget.curselection()
            if selection:
                self.variables[to_var] = widget.get(selection[0])
        elif isinstance(widget, tuple):
            _, var = widget
            self.variables[to_var] = var.get()
    
    def cmd_change(self, params):
        widget_name = self.resolve(params.get("change", ""))
        widget = self.widgets.get(widget_name)
        if isinstance(widget, tk.Label):
            text = self.resolve(params.get("to", ""))
            widget.config(text=text)
        elif isinstance(widget, tk.Button):
            text = self.resolve(params.get("to", ""))
            widget.config(text=text)
    
    def cmd_clear(self, params):
        widget_name = self.resolve(params.get("clear", ""))
        widget = self.widgets.get(widget_name)
        if isinstance(widget, tk.Entry):
            widget.delete(0, tk.END)
        elif isinstance(widget, tk.Listbox):
            widget.delete(0, tk.END)
        elif isinstance(widget, tk.Canvas):
            widget.delete("all")
    
    def cmd_print(self, params):
        text = self.resolve(params.get("print", ""))
        print(text)
    
    def cmd_message(self, params):
        msg = self.resolve(params.get("message", "Hello"))
        title = self.resolve(params.get("title", "Info"))
        msg_type = self.resolve(params.get("type", "info")).lower()
        if msg_type == "error":
            messagebox.showerror(title, msg)
        elif msg_type == "warning":
            messagebox.showwarning(title, msg)
        elif msg_type == "question":
            result = messagebox.askquestion(title, msg)
            self.variables["result"] = result
        else:
            messagebox.showinfo(title, msg)
    
    def cmd_delay(self, params):
        ms = int(self.resolve(params.get("delay", "1000")))
        time.sleep(ms / 1000)
    
    def cmd_exit(self, params):
        self.root.quit()
    
    def cmd_readfile(self, params):
        path = self.resolve(params.get("readfile", ""))
        to_var = self.resolve(params.get("to", "content"))
        with open(path, "r", encoding="utf-8") as f:
            self.variables[to_var] = f.read()
    
    def cmd_writefile(self, params):
        path = self.resolve(params.get("writefile", ""))
        content = self.resolve(params.get("content", ""))
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    
    def cmd_appendfile(self, params):
        path = self.resolve(params.get("appendfile", ""))
        content = self.resolve(params.get("content", ""))
        with open(path, "a", encoding="utf-8") as f:
            f.write(content)
    
    def cmd_makefolder(self, params):
        path = self.resolve(params.get("makefolder", ""))
        os.makedirs(path, exist_ok=True)
    
    def cmd_listfolder(self, params):
        path = self.resolve(params.get("listfolder", "."))
        to_var = self.resolve(params.get("to", "files"))
        self.variables[to_var] = "\n".join(os.listdir(path))
    
    def cmd_now(self, params):
        to_var = self.resolve(params.get("now", "now"))
        fmt = self.resolve(params.get("format", "%Y-%m-%d %H:%M:%S"))
        self.variables[to_var] = datetime.now().strftime(fmt)
    
    def cmd_formatdate(self, params):
        date_str = self.resolve(params.get("date", ""))
        fmt = self.resolve(params.get("format", "%Y-%m-%d %H:%M:%S"))
        to_var = self.resolve(params.get("to", "formatted"))
        try:
            dt = datetime.strptime(date_str, fmt)
            self.variables[to_var] = dt.strftime(fmt)
        except:
            self.variables[to_var] = date_str
    
    def cmd_random(self, params):
        min_val = int(self.resolve(params.get("min", "0")))
        max_val = int(self.resolve(params.get("max", "100")))
        to_var = self.resolve(params.get("to", "random"))
        self.variables[to_var] = random.randint(min_val, max_val)
    
    def cmd_add(self, params):
        var = self.resolve(params.get("add", ""))
        by = float(self.resolve(params.get("by", "1")))
        self.variables[var] = self.variables.get(var, 0) + by
    
    def cmd_subtract(self, params):
        var = self.resolve(params.get("subtract", ""))
        by = float(self.resolve(params.get("by", "1")))
        self.variables[var] = self.variables.get(var, 0) - by
    
    def cmd_multiply(self, params):
        var = self.resolve(params.get("multiply", ""))
        by = float(self.resolve(params.get("by", "1")))
        self.variables[var] = self.variables.get(var, 0) * by
    
    def cmd_divide(self, params):
        var = self.resolve(params.get("divide", ""))
        by = float(self.resolve(params.get("by", "1")))
        if by != 0:
            self.variables[var] = self.variables.get(var, 0) / by
    
    def cmd_mod(self, params):
        var = self.resolve(params.get("mod", ""))
        by = float(self.resolve(params.get("by", "1")))
        if by != 0:
            self.variables[var] = self.variables.get(var, 0) % by
    
    def cmd_dict(self, params):
        name = self.resolve(params.get("dict", ""))
        data = self.resolve(params.get("data", ""))
        items = data.split(";")
        d = {}
        for item in items:
            if ":" in item:
                k, v = item.split(":", 1)
                d[k.strip()] = v.strip()
        self.variables[name] = json.dumps(d)
    
    def cmd_parsejson(self, params):
        json_str = self.resolve(params.get("parsejson", ""))
        to_var = self.resolve(params.get("to", "parsed"))
        try:
            self.variables[to_var] = json.loads(json_str)
        except:
            self.variables[to_var] = {}
    
    def cmd_import(self, params):
        module = self.resolve(params.get("import", ""))
        try:
            globals()[module] = __import__(module)
        except Exception as e:
            print(f"Failed to import {module}: {e}")
    
    def run(self, code):
        self.loop_stack = []
        lines = code.strip().split("\n")
        self.execute_lines(lines)
        self.root.mainloop()


def run_plainpi(code):
    window = None
    bg_color = "#1e1e1e"
    lines = code.strip().split("\n")
    
    for line in lines:
        line = line.strip()
        if "Window:" in line:
            match = re.search(r"Window:\[([^\]]+)\].*?Size:\[([^\]]+)\]", line)
            if match:
                title = match.group(1)
                size = match.group(2)
                w, h = map(int, size.split(","))
                window = PlainPiWindow(title, w, h, bg_color)
            break
    
    for line in lines:
        if "Background:" in line:
            match = re.search(r"Background:\[([^\]]+)\]", line)
            if match:
                bg_color = match.group(1)
                if window:
                    window.root.configure(bg=bg_color)
                    window.canvas.configure(bg=bg_color)
    
    if window:
        window.loop_stack = []
        window.run(code)


if __name__ == "__main__":
    test_code = """Window:[Test] | Size:[800,600]
Set:[isim] | To:[Ahmet]
If:[isim == "Ahmet"]
Print:[Isim Ahmet!]
EndIf:
Sprite:[player.png] | Name:[Player] | Locate:[100,100]
Move:[Player] | To:[300,100] | Speed:[5]
Sound:[click.wav] | Type:[sfx]"""
    run_plainpi(test_code)