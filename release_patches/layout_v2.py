from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QMenu, QMainWindow
)


def _nav_button(text, parent, *, active=False, height=44):
    button = QPushButton(text, parent)
    button.setProperty("active", active)
    button.setMinimumHeight(height)
    button.setMaximumHeight(height)
    return button


def _build_sidebar_v2(self):
    panel = QFrame()
    panel.setObjectName("sidebar")
    panel.setFixedWidth(214)
    layout = QVBoxLayout(panel)
    layout.setContentsMargins(16, 18, 16, 16)
    layout.setSpacing(6)

    brand = QLabel("S H A D O W")
    brand.setStyleSheet(
        "font-size: 17px; font-weight: 650; color: #eefbff;"
        "letter-spacing: 3px; padding: 3px 8px 1px 8px;"
    )
    layout.addWidget(brand)

    brand_sub = QLabel("PERSONAL INTELLIGENCE")
    brand_sub.setStyleSheet(
        "color: #5f829b; letter-spacing: 2px; font-size: 8px;"
        "padding: 0px 8px 16px 8px;"
    )
    layout.addWidget(brand_sub)

    nav = [
        ("⌂  Home", True, None),
        ("□  Workspace", False, self._open_workspace_hub),
        ("✓  Tasks", False, None),
        ("▤  Documents", False, self._open_document_studio),
        ("◉  Agents", False, self._open_agent_center),
        ("◎  Knowledge", False, self._open_memory_hub),
    ]
    for text, active, callback in nav:
        button = _nav_button(text, panel, active=active)
        if callback:
            button.clicked.connect(callback)
        layout.addWidget(button)

    more = _nav_button("•••  More", panel)
    more.clicked.connect(lambda: self._show_more_menu(more))
    layout.addWidget(more)

    layout.addStretch(1)

    divider = QFrame()
    divider.setFixedHeight(1)
    divider.setStyleSheet("background: rgba(24, 200, 255, 38); border: none;")
    layout.addWidget(divider)

    quick = QHBoxLayout()
    quick.setSpacing(6)

    system = QPushButton("✓  Check")
    system.setToolTip("System Check")
    system.setMinimumHeight(38)
    system.clicked.connect(self._open_release_center)
    quick.addWidget(system, 1)

    settings = QPushButton("⚙  Settings")
    settings.setToolTip("AI and voice settings")
    settings.setMinimumHeight(38)
    settings.clicked.connect(self._open_ai_settings)
    quick.addWidget(settings, 1)
    layout.addLayout(quick)

    user = QLabel("SIR  •  LOCAL PROFILE")
    user.setStyleSheet(
        "padding: 10px 8px 3px 8px; color: #b8d6e7;"
        "font-size: 9px; letter-spacing: 1px;"
    )
    layout.addWidget(user)

    motto = QLabel("A MORE CAPABLE YOU.")
    motto.setObjectName("muted")
    motto.setStyleSheet(
        "letter-spacing: 2px; font-size: 8px; padding: 2px 8px 6px 8px;"
    )
    layout.addWidget(motto)
    return panel


def _show_more_menu(self, anchor):
    menu = QMenu(anchor)
    menu.setStyleSheet("""
        QMenu {
            background: #07111d;
            color: #e8f5ff;
            border: 1px solid #183654;
            border-radius: 10px;
            padding: 7px;
        }
        QMenu::item {
            padding: 8px 22px 8px 12px;
            border-radius: 7px;
        }
        QMenu::item:selected {
            background: rgba(24, 200, 255, 35);
            color: #79dfff;
        }
        QMenu::separator {
            height: 1px;
            background: #183654;
            margin: 5px 8px;
        }
    """)

    items = [
        ("News", self._open_news_center),
        ("Memory", self._open_memory_hub),
        ("Workspace Hub", self._open_workspace_hub),
        ("Proactive", self._open_proactive_center),
        ("Security", self._open_security_center),
        (None, None),
        ("Integrations", self._open_integration_center),
        ("Remote", self._open_remote_center),
        ("Computer Control", self._open_computer_center),
        (None, None),
        ("Voice Input", self._open_voice_settings),
        ("Voice Output", self._open_tts_settings),
        ("AI Settings", self._open_ai_settings),
        ("System Check", self._open_release_center),
    ]
    for label, callback in items:
        if label is None:
            menu.addSeparator()
            continue
        action = menu.addAction(label)
        action.triggered.connect(callback)

    menu.exec(anchor.mapToGlobal(anchor.rect().bottomLeft()))


def _build_center_v2(self):
    wrap = self._shadow_original_build_center()
    try:
        self.core.setMinimumSize(430, 430)
        self.greeting.setStyleSheet(
            "font-size: 27px; font-weight: 300; padding-top: 0px;"
        )
        self.response.setMinimumHeight(78)
        self.response.setMaximumHeight(132)
        self.command.setMinimumHeight(46)
        self.system_status.setStyleSheet(
            "font-size: 9px; color: #7892aa; padding: 2px 8px 4px 8px;"
        )
    except Exception:
        pass
    return wrap


def _build_right_panel_v2(self):
    panel = QFrame()
    panel.setObjectName("rightPanel")
    panel.setFixedWidth(252)
    self.right_panel = panel

    layout = QVBoxLayout(panel)
    layout.setContentsMargins(12, 14, 12, 14)
    layout.setSpacing(10)

    ai_cfg = self.config.get("ai", {})
    tts_cfg = self.config.get("tts", {})
    provider = str(ai_cfg.get("provider", "gemini")).title()
    voice = str(tts_cfg.get("provider", "auto")).title()

    layout.addWidget(self._card("System", [
        f"AI        ·  {provider}",
        f"Voice     ·  {voice}",
        f"Runtime   ·  {'SAFE MODE' if self.safe_mode else 'NORMAL'}",
        "Status    ·  Online",
    ]))

    layout.addWidget(self._card("Shortcuts", [
        "F9        ·  Push to talk",
        "Esc       ·  Stop active task",
        "Enter     ·  Send command",
    ]))

    layout.addStretch(1)

    hint = QLabel("Use MORE for tools, integrations,\nsecurity and advanced controls.")
    hint.setWordWrap(True)
    hint.setObjectName("muted")
    hint.setStyleSheet(
        "color: #7892aa; font-size: 9px; padding: 8px 6px;"
    )
    layout.addWidget(hint)

    foot = QLabel("SHADOW 3.0")
    foot.setAlignment(Qt.AlignmentFlag.AlignRight)
    foot.setObjectName("muted")
    foot.setStyleSheet("letter-spacing: 3px; font-size: 8px; padding: 4px;")
    layout.addWidget(foot)
    return panel


def _resize_event_v2(self, event):
    QMainWindow.resizeEvent(self, event)
    panel = getattr(self, "right_panel", None)
    if panel is not None:
        panel.setVisible(self.width() >= 1360)


def install_layout_v2(cls):
    if getattr(cls, "_shadow_layout_v2_installed", False):
        return
    cls._shadow_layout_v2_installed = True
    cls._shadow_original_build_center = cls._build_center
    cls._build_sidebar = _build_sidebar_v2
    cls._show_more_menu = _show_more_menu
    cls._build_center = _build_center_v2
    cls._build_right_panel = _build_right_panel_v2
    cls.resizeEvent = _resize_event_v2
