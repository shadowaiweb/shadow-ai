from __future__ import annotations

import argparse
import json
import logging
import os
import sys

from core.logging_setup import configure_logging
from core.preflight import run_preflight
from core.single_instance import InstanceLock
from core.startup_guard import StartupGuard
from core.version import version_string

def _args():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument(
        "--diagnostics-only",
        action="store_true",
        help="Run release preflight checks and exit.",
    )
    parser.add_argument(
        "--safe-mode",
        action="store_true",
        help="Start SHADOW with automation/proactive/voice output limited.",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print version and exit.",
    )
    return parser.parse_args()

def _diagnostics_exit():
    report = run_preflight()
    print(json.dumps(report.to_dict(), indent=2))
    return 0 if report.ok else 2

def main():
    args = _args()

    if args.version:
        print(version_string())
        return 0

    configure_logging()
    logger = logging.getLogger("shadow")
    logger.info("SHADOW startup requested.")

    if args.diagnostics_only:
        return _diagnostics_exit()

    if args.safe_mode:
        os.environ["SHADOW_SAFE_MODE"] = "1"

    instance = InstanceLock()
    if not instance.acquire():
        # Avoid loading the full UI when another SHADOW instance is active.
        logger.warning("Second SHADOW instance blocked.")
        return 3

    guard = StartupGuard()
    previous_unclean = guard.begin()

    try:
        from PyQt6.QtGui import QFont
        from PyQt6.QtWidgets import QApplication, QMessageBox

        from core.crash_handler import install_crash_handler
        from ui.main_window import ShadowMainWindow

        app = QApplication(sys.argv[:1])
        app.setApplicationName("SHADOW")
        app.setApplicationDisplayName("SHADOW 3.0")
        app.setOrganizationName("SHADOW AI")
        app.setFont(QFont("Segoe UI", 10))

        def crash_notice(exc, path):
            try:
                QMessageBox.critical(
                    None,
                    "SHADOW Error",
                    "SHADOW encountered an unexpected error.\n\n"
                    f"A crash report was saved to:\n{path}",
                )
            except Exception:
                pass

        install_crash_handler(crash_notice)

        if previous_unclean and os.getenv("SHADOW_SAFE_MODE") != "1":
            answer = QMessageBox.question(
                None,
                "Previous SHADOW Session",
                "The previous SHADOW session did not shut down normally.\n\n"
                "Start in Safe Mode for this run?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if answer == QMessageBox.StandardButton.Yes:
                os.environ["SHADOW_SAFE_MODE"] = "1"

        window = ShadowMainWindow()
        window.show()
        logger.info(
            "SHADOW UI launched. Safe mode=%s",
            os.getenv("SHADOW_SAFE_MODE") == "1",
        )
        return int(app.exec())
    finally:
        guard.end()
        instance.release()
        logger.info("SHADOW shutdown complete.")

if __name__ == "__main__":
    raise SystemExit(main())
