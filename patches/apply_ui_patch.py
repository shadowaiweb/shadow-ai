from pathlib import Path

p = Path('ui/main_window.py')
s = p.read_text(encoding='utf-8')

s = s.replace('    QTextBrowser\n)', '    QTextBrowser, QMenu\n)')

start = s.index('    def _build_sidebar(self):')
end = s.index('    def _build_center(self):')
sidebar = '''    def _build_sidebar(self):
        panel = QFrame()
        panel.setObjectName("sidebar")
        panel.setFixedWidth(205)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(14, 18, 14, 16)
        layout.setSpacing(5)

        brand = QLabel("SHADOW")
        brand.setStyleSheet(
            "font-size: 18px; font-weight: 700; letter-spacing: 5px; "
            "color: #eaf8ff; padding: 4px 8px 18px 8px;"
        )
        layout.addWidget(brand)

        for text, active, callback in [
            ("Home", True, None),
            ("Workspace", False, self._open_workspace_hub),
            ("Tasks", False, None),
            ("Documents", False, self._open_document_studio),
            ("Agents", False, self._open_agent_center),
            ("Knowledge", False, self._open_memory_hub),
        ]:
            b = QPushButton(text)
            b.setProperty("active", active)
            b.setMinimumHeight(40)
            if callback:
                b.clicked.connect(callback)
            layout.addWidget(b)

        more = QPushButton("More   ···")
        more.setMinimumHeight(40)
        menu = QMenu(more)
        for label, callback in [
            ("System Check", self._open_release_center),
            ("Proactive", self._open_proactive_center),
            ("Security", self._open_security_center),
            ("News", self._open_news_center),
            ("Integrations", self._open_integration_center),
            ("Remote", self._open_remote_center),
            ("Computer Control", self._open_computer_center),
            ("AI Settings", self._open_ai_settings),
            ("Voice Output", self._open_tts_settings),
            ("Voice Input", self._open_voice_settings),
        ]:
            action = menu.addAction(label)
            action.triggered.connect(callback)
        more.setMenu(menu)
        layout.addWidget(more)

        layout.addStretch(1)
        status = QLabel("● ONLINE")
        status.setStyleSheet(
            "color: #18e3b7; font-size: 10px; letter-spacing: 2px; padding: 8px;"
        )
        layout.addWidget(status)
        user = QLabel("SIR  ·  PERSONAL")
        user.setStyleSheet("padding: 2px 8px; color: #9db8ca; font-size: 10px;")
        layout.addWidget(user)
        motto = QLabel("A MORE CAPABLE YOU.")
        motto.setObjectName("muted")
        motto.setStyleSheet("letter-spacing: 2px; font-size: 8px; padding: 4px 8px;")
        layout.addWidget(motto)
        return panel

'''
s = s[:start] + sidebar + s[end:]

s = s.replace('panel.setFixedWidth(300)', 'panel.setFixedWidth(255)')
s = s.replace('self.resize(1600, 900)', 'self.resize(1500, 900)')
s = s.replace('self.setMinimumSize(1180, 700)', 'self.setMinimumSize(1100, 700)')
s = s.replace('self.response.setMaximumHeight(118)', 'self.response.setMaximumHeight(132)')
s = s.replace('self.response.setMinimumHeight(72)', 'self.response.setMinimumHeight(86)')
s = s.replace('font-size: 30px; font-weight: 300;', 'font-size: 27px; font-weight: 300;')

# Keep controls readable on Windows where emoji glyphs can render inconsistently.
s = s.replace('self.mic = QPushButton("🎙")', 'self.mic = QPushButton("MIC")')
s = s.replace('self.send = QPushButton("➤")', 'self.send = QPushButton("SEND")')
s = s.replace('self.send.setText("➤")', 'self.send.setText("SEND")')
s = s.replace('self.send.setText("■")', 'self.send.setText("STOP")')

p.write_text(s, encoding='utf-8')
print('Applied compact SHADOW desktop UI patch')
