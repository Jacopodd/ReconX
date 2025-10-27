import sys
import asyncio
from PyQt6 import QtWidgets, QtGui, QtCore
from reconx.core.engine import run_scan
from reconx.core.storage import export_results
import threading
import json
import os

APP_TITLE = "ReconX — Sentinel Recon Module"
APP_VERSION = "v0.1"
LOGO_PATH = os.path.join("assets", "ReconX_logo.png")


# === Worker thread per scansione asincrona ===
class ScanWorker(QtCore.QThread):
    progress = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal(list)

    def __init__(self, target):
        super().__init__()
        self.target = target

    def run(self):
        import os
        import pathlib

        # Imposta la working directory del processo sul livello root del progetto
        project_root = pathlib.Path(__file__).resolve().parent.parent
        os.chdir(project_root)

        self.progress.emit(f"[ReconX] Starting scan for {self.target}...\n")
        try:
            results = asyncio.run(run_scan(self.target))
            self.finished.emit(results)
        except Exception as e:
            self.progress.emit(f"[!] Errore durante la scansione: {e}\n")
            self.finished.emit([])


# === Finestra principale ===
class ReconXMain(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.setWindowIcon(QtGui.QIcon(LOGO_PATH))
        self.resize(1100, 700)

        # Tema scuro
        with open(os.path.join("assets", "style.qss"), "r") as f:
            self.setStyleSheet(f.read())

        # Layout principale
        self.tabs = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tabs)

        # Schede
        self.scan_tab = self._build_scan_tab()
        self.results_tab = self._build_results_tab()
        self.plugins_tab = self._build_plugins_tab()

        self.tabs.addTab(self.scan_tab, "🎯 Scan")
        self.tabs.addTab(self.results_tab, "📊 Results")
        self.tabs.addTab(self.plugins_tab, "🧩 Plugins")

        # Splash screen
        self._show_splash()

    # --- Splash screen ---
    def _show_splash(self):
        splash_pix = QtGui.QPixmap(LOGO_PATH)
        splash = QtWidgets.QSplashScreen(splash_pix)
        splash.showMessage("Loading ReconX...", QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignCenter, QtGui.QColor("#FF6B35"))
        splash.show()
        QtWidgets.QApplication.processEvents()
        QtCore.QThread.sleep(2)
        splash.close()

    # --- Scheda SCAN ---
    def _build_scan_tab(self):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        self.target_input = QtWidgets.QLineEdit()
        self.target_input.setPlaceholderText("Enter target (e.g. example.com)")
        self.target_input.setStyleSheet("padding: 8px; font-size: 15px;")

        self.scan_button = QtWidgets.QPushButton("Start Scan")
        self.scan_button.clicked.connect(self.start_scan)

        self.console_output = QtWidgets.QTextEdit()
        self.console_output.setReadOnly(True)

        layout.addWidget(QtWidgets.QLabel("Target:"))
        layout.addWidget(self.target_input)
        layout.addWidget(self.scan_button)
        layout.addWidget(QtWidgets.QLabel("Console:"))
        layout.addWidget(self.console_output)

        widget.setLayout(layout)
        return widget

    # --- Scheda RESULTS ---
    def _build_results_tab(self):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)

        # Area scrollabile per contenere i risultati come card
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.results_container = QtWidgets.QWidget()
        self.results_layout = QtWidgets.QVBoxLayout(self.results_container)
        self.scroll_area.setWidget(self.results_container)

        # Pulsanti di esportazione
        self.export_json_btn = QtWidgets.QPushButton("Export JSON")
        self.export_json_btn.clicked.connect(lambda: self.export_results("json"))
        self.export_csv_btn = QtWidgets.QPushButton("Export CSV")
        self.export_csv_btn.clicked.connect(lambda: self.export_results("csv"))

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(self.export_json_btn)
        btn_layout.addWidget(self.export_csv_btn)

        layout.addWidget(self.scroll_area)
        layout.addLayout(btn_layout)
        return widget

    # --- Scheda PLUGINS ---
    def _build_plugins_tab(self):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        self.plugins_list = QtWidgets.QListWidget()
        layout.addWidget(QtWidgets.QLabel("Available Plugins:"))
        layout.addWidget(self.plugins_list)

        # Popola lista plugin
        self._load_plugins()
        widget.setLayout(layout)
        return widget

    # --- Caricamento plugin ---
    def _load_plugins(self):
        import pathlib

        # Percorso base del progetto (2 livelli sopra la GUI)
        base_dir = pathlib.Path(__file__).resolve().parent.parent
        plugins_dir = base_dir / "plugins"

        # Verifica presenza della cartella
        if not plugins_dir.exists():
            self.plugins_list.addItem("⚠️ Nessuna directory 'plugins' trovata.")
            return

        found = 0
        for d in plugins_dir.iterdir():
            plugin_path = d / "plugin.py"
            if plugin_path.exists():
                self.plugins_list.addItem(f"{d.name} — ✅ Loaded")
                found += 1

        if found == 0:
            self.plugins_list.addItem("⚠️ Nessun plugin trovato nella directory.")

    # --- Avvio scansione ---
    def start_scan(self):
        target = self.target_input.text().strip()
        if not target:
            self.console_output.append("[!] Please enter a valid target.\n")
            return

        self.console_output.append(f"[*] Running scan for {target}...\n")
        self.worker = ScanWorker(target)
        self.worker.progress.connect(self.console_output.append)
        self.worker.finished.connect(self.show_results)
        self.worker.start()

    # --- Mostra risultati nella tabella ---
    def show_results(self, results):
        """Mostra i risultati in formato card leggibile"""
        self.current_results = results or []

        # Pulisce eventuali card precedenti
        for i in reversed(range(self.results_layout.count())):
            widget = self.results_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        if not results:
            msg = QtWidgets.QLabel("Nessun risultato disponibile.")
            msg.setStyleSheet("font-size:16px; color:#aaa; padding:10px;")
            self.results_layout.addWidget(msg)
            return

        for r in results:
            card = QtWidgets.QFrame()
            card.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            card.setStyleSheet("""
                QFrame {
                    background-color: #0F1724;
                    border: 1px solid #1F2A38;
                    border-radius: 10px;
                    padding: 12px;
                    margin-bottom: 10px;
                }
                QLabel { color: #E6EEF6; }
            """)

            vbox = QtWidgets.QVBoxLayout(card)

            # Header (module + type)
            header = QtWidgets.QLabel(f"🧩 <b>{r.get('module', '')}</b> — <i>{r.get('type', '')}</i>")
            header.setTextFormat(QtCore.Qt.TextFormat.RichText)
            header.setStyleSheet("font-size:15px; color:#FF6B35; margin-bottom:4px;")
            vbox.addWidget(header)

            # Info principali
            info_lines = [
                f"<b>Target:</b> {r.get('target', '')}",
                f"<b>Confidence:</b> {r.get('confidence', '')}",
                f"<b>Priority:</b> {r.get('priority', '')}",
                f"<b>Scanned At:</b> {r.get('scanned_at', '')}",
            ]
            info_label = QtWidgets.QLabel("<br>".join(info_lines))
            info_label.setTextFormat(QtCore.Qt.TextFormat.RichText)
            info_label.setStyleSheet("margin-left:10px; margin-bottom:6px;")
            vbox.addWidget(info_label)

            # Evidence
            ev_label = QtWidgets.QLabel("<b>Evidence:</b>")
            vbox.addWidget(ev_label)
            for ev in r.get("evidence", []):
                ev_item = QtWidgets.QLabel(f"• {ev.get('label', '')}: {ev.get('value', '')}")
                ev_item.setStyleSheet("margin-left:20px; color:#AFC3DA;")
                vbox.addWidget(ev_item)

            # Meta (pretty JSON)
            meta_pretty = json.dumps(r.get("meta", {}), indent=2)
            meta_label = QtWidgets.QLabel("<b>Meta:</b>")
            vbox.addWidget(meta_label)

            meta_text = QtWidgets.QTextEdit(meta_pretty)
            meta_text.setReadOnly(True)
            meta_text.setMinimumHeight(80)
            meta_text.setStyleSheet(
                "background-color:#0B1220; color:#9FC2FF; font-family:'JetBrains Mono'; font-size:11px;"
            )
            vbox.addWidget(meta_text)

            self.results_layout.addWidget(card)

        self.console_output.append(f"[+] Visualizzati {len(results)} risultati in formato card.\n")

    def copy_selected_json(self):
        """Copia negli appunti il JSON completo del risultato selezionato."""
        row = self.results_table.currentRow()
        if not hasattr(self, "current_results") or row < 0 or row >= len(getattr(self, "current_results", [])):
            self.console_output.append("[!] Nessuna riga selezionata.\n")
            return

        data = self.current_results[row]
        payload = json.dumps(data, indent=2, ensure_ascii=False)
        QtWidgets.QApplication.clipboard().setText(payload)
        self.console_output.append("[✓] JSON copiato negli appunti.\n")

    # --- Esportazione risultati ---
    def export_results(self, fmt):
        out_path = f"export_{fmt}.{fmt}"
        export_results(out_path, fmt)
        self.console_output.append(f"[✓] Results exported to {out_path}\n")

    def update_result_details(self):
        """Aggiorna il pannello dettagli con evidence/meta del record selezionato."""
        if not hasattr(self, "current_results") or not self.current_results:
            self.detail_view.clear()
            return

        row = self.results_table.currentRow()
        if row < 0 or row >= len(self.current_results):
            self.detail_view.clear()
            return

        r = self.current_results[row]
        target = r.get("target", "")
        module = r.get("module", "")
        rtype = r.get("type", "")
        conf = r.get("confidence", "")
        prio = r.get("priority", "")
        scanned = r.get("scanned_at", "")

        # Evidence (lista di dict con label/value)
        evidence = r.get("evidence", [])
        ev_lines = []
        for e in evidence or []:
            label = str(e.get("label", ""))
            value = e.get("value", "")
            ev_lines.append(f"• {label}: {value}")
        ev_block = "\n".join(ev_lines) if ev_lines else "(no evidence)"

        # Meta pretty JSON
        meta = r.get("meta", {})
        try:
            meta_pretty = json.dumps(meta, indent=2, ensure_ascii=False)
        except Exception:
            meta_pretty = str(meta)

        text = (
            f"Target    : {target}\n"
            f"Module    : {module}\n"
            f"Type      : {rtype}\n"
            f"Confidence: {conf}\n"
            f"Priority  : {prio}\n"
            f"Scanned At: {scanned}\n"
            f"\n== Evidence ==\n{ev_block}\n"
            f"\n== Meta ==\n{meta_pretty}\n"
        )

        self.detail_view.setPlainText(text)


# === Avvio App ===
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ReconXMain()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
