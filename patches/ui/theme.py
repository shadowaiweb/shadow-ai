BG = "#020912"
PANEL = "#07111d"
PANEL_2 = "#091827"
BORDER = "#183654"
TEXT = "#e8f5ff"
MUTED = "#7892aa"
CYAN = "#18c8ff"
CYAN_SOFT = "#6fe8ff"
GREEN = "#18e3b7"
WARN = "#ffb84d"
ALERT = "#ff5a72"

APP_QSS = f"""
QMainWindow {{
    background: {BG};
}}
QWidget {{
    color: {TEXT};
    font-family: 'Segoe UI';
}}
QFrame#sidebar, QFrame#rightPanel {{
    background: rgba(4, 14, 24, 235);
    border: 1px solid {BORDER};
    border-radius: 18px;
}}
QPushButton {{
    border: 1px solid transparent;
    border-radius: 12px;
    padding: 10px 14px;
    text-align: left;
    color: {TEXT};
    background: transparent;
}}
QPushButton:hover {{
    background: rgba(24, 200, 255, 24);
    border-color: rgba(24, 200, 255, 80);
}}
QPushButton[active="true"] {{
    background: rgba(24, 200, 255, 30);
    border: 1px solid {CYAN};
    color: {CYAN_SOFT};
}}
QLineEdit {{
    background: rgba(4, 15, 25, 230);
    border: 1px solid {CYAN};
    border-radius: 22px;
    padding: 12px 18px;
    color: {TEXT};
    selection-background-color: {CYAN};
}}
QLabel#muted {{
    color: {MUTED};
}}
QFrame#card {{
    background: rgba(5, 17, 28, 235);
    border: 1px solid {BORDER};
    border-radius: 16px;
}}
"""

APP_QSS += f"""
QMenu {{
    background: #07111d;
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 6px;
    color: {TEXT};
}}
QMenu::item {{
    padding: 9px 28px 9px 12px;
    border-radius: 7px;
}}
QMenu::item:selected {{
    background: rgba(24, 200, 255, 28);
    color: {CYAN_SOFT};
}}
"""
