# PlainPiW.py - PlainPi Web Designer (FINAL)
# HATA 2: Link Yazisi Sorunu DUZELTILDI (Content parametresi)
# HATA 3: Isinlanma Sorunu DUZELTILDI (CSS transition)

import re
import json

class PlainPiW:
    def __init__(self):
        self.elements = {}
        self.commands = []
    
    def parse(self, code):
        lines = code.strip().split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Sprite
            if "Sprite:" in line and "Button:" not in line:
                match = re.search(r"Sprite:\[([^\]]+)\].*?Name:\[([^\]]+)\].*?In:\[([^\]]+)\].*?Locate:\[([^\]]+)\]", line)
                if match:
                    image, name, scene, locate = match.groups()
                    x, y = map(int, locate.split(","))
                    self.elements[name] = {"type": "sprite", "image": image, "scene": scene, "x": x, "y": y}
            
            # Text
            elif "Text:" in line:
                match = re.search(r"Text:\[([^\]]+)\].*?Name:\[([^\]]+)\].*?In:\[([^\]]+)\].*?Locate:\[([^\]]+)\]", line)
                if match:
                    text, name, scene, locate = match.groups()
                    x, y = map(int, locate.split(","))
                    self.elements[name] = {"type": "text", "content": text, "scene": scene, "x": x, "y": y}
            
            # Button
            elif "Button:" in line:
                match = re.search(r"Button:\[([^\]]+)\].*?Name:\[([^\]]+)\].*?In:\[([^\]]+)\].*?Locate:\[([^\]]+)\]", line)
                if match:
                    text, name, scene, locate = match.groups()
                    x, y = map(int, locate.split(","))
                    self.elements[name] = {"type": "button", "content": text, "scene": scene, "x": x, "y": y}
            
            # Input
            elif "Input:" in line:
                match = re.search(r"Input:\[([^\]]+)\].*?Name:\[([^\]]+)\].*?In:\[([^\]]+)\].*?Locate:\[([^\]]+)\]", line)
                if match:
                    placeholder, name, scene, locate = match.groups()
                    x, y = map(int, locate.split(","))
                    self.elements[name] = {"type": "input", "placeholder": placeholder, "scene": scene, "x": x, "y": y}
            
            # Link (HATA 2 DUZELTILDI: Content parametresi)
            elif "Link:" in line:
                match = re.search(r"Link:\[([^\]]+)\].*?Name:\[([^\]]+)\].*?In:\[([^\]]+)\].*?Locate:\[([^\]]+)\].*?Content:\[([^\]]+)\]", line)
                if match:
                    url, name, scene, locate, content = match.groups()
                    x, y = map(int, locate.split(","))
                    self.elements[name] = {"type": "link", "url": url, "content": content, "scene": scene, "x": x, "y": y}
                else:
                    # Content yoksa name kullan
                    match = re.search(r"Link:\[([^\]]+)\].*?Name:\[([^\]]+)\].*?In:\[([^\]]+)\].*?Locate:\[([^\]]+)\]", line)
                    if match:
                        url, name, scene, locate = match.groups()
                        x, y = map(int, locate.split(","))
                        self.elements[name] = {"type": "link", "url": url, "content": name, "scene": scene, "x": x, "y": y}
            
            # Move
            elif "Move:" in line:
                match = re.search(r"Move:\[([^\]]+)\].*?To:\[([^\]]+)\].*?Speed:\[([^\]]+)\]", line)
                if match:
                    name, to, speed = match.groups()
                    tx, ty = map(int, to.split(","))
                    self.commands.append({"type": "move", "name": name, "to": (tx, ty), "speed": int(speed)})
            
            # Sound
            elif "Sound:" in line:
                match = re.search(r"Sound:\[([^\]]+)\].*?Type:\[([^\]]+)\]", line)
                if match:
                    sound, stype = match.groups()
                    self.commands.append({"type": "sound", "sound": sound, "stype": stype})
        
        return self.elements, self.commands
    
    def export_html(self, output_file="website.html"):
        html = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PlainPi Web Site</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background: #f0f0f0;
            font-family: Arial, sans-serif;
        }
        .container {
            position: relative;
            width: 100%;
            min-height: 100vh;
        }
"""
        
        # CSS stilleri (HATA 3 DUZELTILDI: Transition eklendi)
        for name, elem in self.elements.items():
            html += f"        #{name} {{\n"
            html += f"            position: absolute;\n"
            html += f"            left: {elem['x']}px;\n"
            html += f"            top: {elem['y']}px;\n"
            html += f"            transition: left 0.5s ease, top 0.5s ease;\n"
            
            if elem['type'] == 'sprite':
                html += f"            width: 200px;\n"
                html += f"            height: 150px;\n"
                html += f"            background: url('{elem['image']}') no-repeat center;\n"
                html += f"            background-size: cover;\n"
                html += f"            background-color: #4CAF50;\n"
            elif elem['type'] == 'text':
                html += f"            color: #333;\n"
                html += f"            font-size: 16px;\n"
                html += f"            padding: 10px;\n"
            elif elem['type'] == 'button':
                html += f"            background: #4CAF50;\n"
                html += f"            color: white;\n"
                html += f"            padding: 10px 20px;\n"
                html += f"            border: none;\n"
                html += f"            border-radius: 5px;\n"
                html += f"            cursor: pointer;\n"
                html += f"            font-size: 14px;\n"
            elif elem['type'] == 'input':
                html += f"            padding: 10px;\n"
                html += f"            border: 1px solid #ccc;\n"
                html += f"            border-radius: 5px;\n"
                html += f"            font-size: 14px;\n"
                html += f"            width: 200px;\n"
            elif elem['type'] == 'link':
                html += f"            color: #2196F3;\n"
                html += f"            text-decoration: none;\n"
                html += f"            font-size: 14px;\n"
                html += f"            padding: 10px;\n"
            
            html += f"        }}\n\n"
        
        html += """    </style>
</head>
<body>
    <div class="container">
"""
        
        # HTML elementleri
        for name, elem in self.elements.items():
            if elem['type'] == 'sprite':
                html += f'        <div id="{name}"></div>\n'
            elif elem['type'] == 'text':
                html += f'        <div id="{name}">{elem["content"]}</div>\n'
            elif elem['type'] == 'button':
                html += f'        <button id="{name}" onclick="alert(\'Tiklandi: {name}\')">{elem["content"]}</button>\n'
            elif elem['type'] == 'input':
                html += f'        <input type="text" id="{name}" placeholder="{elem["placeholder"]}">\n'
            elif elem['type'] == 'link':
                # HATA 2 DUZELTILDI: Content kullan
                html += f'        <a href="{elem["url"]}" id="{name}" target="_blank">{elem["content"]}</a>\n'
        
        # Move komutlari
        if self.commands:
            html += """    </div>
    <script>
        // PlainPi Web - Otomatik olusturuldu
"""
            for cmd in self.commands:
                if cmd['type'] == 'move':
                    html += f"        setTimeout(() => {{\n"
                    html += f"            document.getElementById('{cmd['name']}').style.left = '{cmd['to'][0]}px';\n"
                    html += f"            document.getElementById('{cmd['name']}').style.top = '{cmd['to'][1]}px';\n"
                    html += f"        }}, 500);\n"
                elif cmd['type'] == 'sound':
                    html += f"        console.log('Sound: {cmd['sound']} ({cmd['stype']})');\n"
            
            html += """    </script>
"""
        
        html += """    </div>
</body>
</html>"""
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)
        
        print(f"Web sitesi olusturuldu: {output_file}")
        return output_file


# Test
if __name__ == "__main__":
    test_code = """Sprite:[header.png] | Name:[Header] | In:[Main] | Locate:[0,0]
Text:[PlainPi Web Sitesi] | Name:[Title] | In:[Main] | Locate:[50,100]
Button:[Tikla!] | Name:[Btn1] | In:[Main] | Locate:[50,150]
Input:[Adinizi girin...] | Name:[Input1] | In:[Main] | Locate:[50,200]
Link:[https://google.com] | Name:[Google] | In:[Main] | Locate:[50,250] | Content:[Google'a Git]
Move:[Header] | To:[0,0] | Speed:[0]
Sound:[click.wav] | Type:[sfx]"""
    
    piw = PlainPiW()
    elements, commands = piw.parse(test_code)
    print("Elements:", json.dumps(elements, indent=2))
    print("Commands:", json.dumps(commands, indent=2))
    piw.export_html("test_website_final.html")