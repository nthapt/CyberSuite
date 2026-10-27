import sys
import subprocess
import platform
import os
import threading
import socket
import hashlib
import time
from datetime import datetime


def ensure_dependencies():
    """
    Garante que as dependências necessárias estão instaladas.
    Se não, instala automaticamente.
    """
    try:
        import psutil
        print("[OK] psutil já instalado.")
    except ImportError:
        print("[INFO] psutil não encontrado. Instalando automaticamente...")
        if input("Confirmar instalação via pip? (s/n): ").lower() == 's':
            subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
            print("[OK] Dependências instaladas com sucesso.")
        else:
            print("[ERRO] Instalação cancelada. O script pode não funcionar corretamente.")
            sys.exit(1)


# Garante que as dependências estão presentes antes de importar
ensure_dependencies()

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import psutil


class NTHCyberSuite:
    def __init__(self, root):
        self.root = root
        self.root.title("NTH CYBER SUITE | Professional Security Toolkit")
        self.root.geometry("1600x950")
        self.root.configure(bg="#0d0d14")  # Background Dark

        # Paleta RGB Profissional
        self.CYAN = "#00f3ff"
        self.MAGENTA = "#ff00ff"
        self.GREEN = "#00ff88"
        self.RED = "#ff3333"
        self.YELLOW = "#ffcc00"
        self.TEXT = "#e0e0e0"
        self.PANEL = "#161622"
        self.DARK = "#0d0d14"

        self.os_name = platform.system()

        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Configuração Estilizada
        self.style.configure("TNotebook", background=self.PANEL, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=self.PANEL, foreground=self.TEXT, padding=[15, 10],
                             font=("Segoe UI", 11, "bold"))
        self.style.map("TNotebook.Tab", background=[("selected", self.CYAN)], foreground=[("selected", self.DARK)])

        self.create_ui()
        self._init_tabs()
        self.start_monitoring()

    def create_ui(self):
        main_container = tk.Frame(self.root, bg=self.DARK)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # --- HEADER RGB ---
        header_frame = tk.Frame(main_container, bg=self.PANEL, height=100)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)

        # Logo NTH Grande
        logo_label = tk.Label(header_frame, text="NTH", font=("Impact", 55), bg=self.PANEL, fg=self.CYAN)
        logo_label.pack(side=tk.LEFT, padx=30)
        self.animate_logo(logo_label)

        tagline = tk.Label(header_frame, text="CYBERSECURITY SUITE", font=("Consolas", 14, "bold"), bg=self.PANEL,
                           fg=self.MAGENTA)
        tagline.pack(side=tk.LEFT, padx=10, pady=35)

        self.status_label = tk.Label(header_frame, text=f"STATUS: ONLINE | OS: {self.os_name}",
                                     font=("Consolas", 12, "bold"), bg=self.PANEL, fg=self.GREEN)
        self.status_label.pack(side=tk.RIGHT, padx=30)

        # --- TABS ---
        notebook = ttk.Notebook(main_container)
        notebook.pack(fill=tk.BOTH, expand=True)

        self.tab_dashboard = self.create_tab(notebook, "📊 DASHBOARD")
        self.tab_files = self.create_tab(notebook, "📁 FILE SENTINEL")
        self.tab_network = self.create_tab(notebook, "🌐 NETWORK DEFENSE")
        self.tab_logs = self.create_tab(notebook, "📝 LOG HUNTER")
        self.tab_processes = self.create_tab(notebook, "🔎 PROCESS AUDITOR")
        self.tab_audit = self.create_tab(notebook, "🛡️ SYSTEM AUDIT")

    def animate_logo(self, label):
        colors = [self.CYAN, self.MAGENTA, self.GREEN]
        current = colors[int(time.time()) % len(colors)]
        label.config(fg=current)
        self.root.after(500, lambda: self.animate_logo(label))

    def create_tab(self, parent, name):
        tab = tk.Frame(parent, bg=self.DARK)
        parent.add(tab, text=name)
        return tab

    # =========================================================================
    # UTILITÁRIOS
    # =========================================================================
    def log(self, widget, message, level="INFO"):
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        color_map = {"INFO": self.GREEN, "WARN": self.YELLOW, "CRIT": self.RED, "NET": self.CYAN}
        color = color_map.get(level, self.TEXT)

        tag_name = f"tag_{level}"
        widget.tag_config(tag_name, foreground=color)
        widget.insert(tk.END, f"{timestamp} | [{level}] {message}\n", tag_name)
        widget.see(tk.END)

    def run_command(self, cmd):
        """Executa comando de sistema de forma segura e retorna a saída."""
        try:
            if isinstance(cmd, str):
                cmd = cmd.split()
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=15,
                                    encoding='utf-8', errors='ignore')
            return result.stdout
        except Exception as e:
            return f"Error: {str(e)}"

    # =========================================================================
    # FERRAMENTA 1: DASHBOARD
    # =========================================================================
    def build_dashboard(self, tab):
        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)

        # Métricas
        left_frame = tk.LabelFrame(tab, text=" REAL-TIME METRICS ", font=("Segoe UI", 12, "bold"), fg=self.CYAN,
                                   bg=self.PANEL, padx=10, pady=10)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)

        self.cpu_var = tk.DoubleVar(value=0)
        self.ram_var = tk.DoubleVar(value=0)
        self.disk_var = tk.DoubleVar(value=0)

        metrics_data = [("CPU", "CPU", self.cpu_var), ("RAM", "RAM", self.ram_var), ("DISK", "DISK", self.disk_var)]
        self.progress_widgets = {}
        self.value_labels = {}

        for i, (label, key, var) in enumerate(metrics_data):
            tk.Label(left_frame, text=label, font=("Consolas", 10, "bold"), bg=self.PANEL, fg=self.TEXT).grid(
                row=i * 2, column=0, sticky="w", pady=5)
            progress = ttk.Progressbar(left_frame, orient="horizontal", length=200, variable=var)
            progress.grid(row=i * 2, column=1, sticky="e", padx=10)
            self.progress_widgets[key] = progress
            value_label = tk.Label(left_frame, text="0%", font=("Consolas", 10), bg=self.PANEL, fg=self.GREEN)
            value_label.grid(row=i * 2 + 1, column=1, sticky="e", padx=10)
            self.value_labels[key] = value_label

        # Processos
        right_frame = tk.LabelFrame(tab, text=" TOP PROCESSES ", font=("Segoe UI", 12, "bold"), fg=self.MAGENTA,
                                    bg=self.PANEL, padx=10, pady=10)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        cols = ("PID", "NAME", "CPU", "RAM")
        self.proc_tree = ttk.Treeview(right_frame, columns=cols, show="headings", height=10)
        self.proc_tree.heading("PID", text="PID")
        self.proc_tree.heading("NAME", text="Name")
        self.proc_tree.heading("CPU", text="CPU %")
        self.proc_tree.heading("RAM", text="RAM %")
        self.proc_tree.column("PID", width=60)
        self.proc_tree.column("NAME", width=150)
        self.proc_tree.column("CPU", width=60)
        self.proc_tree.column("RAM", width=60)
        self.proc_tree.pack(fill=tk.BOTH, expand=True)

        # Log
        log_frame = tk.LabelFrame(tab, text=" SYSTEM LOG ", font=("Segoe UI", 12, "bold"), fg=self.GREEN, bg=self.PANEL,
                                  padx=10, pady=10)
        log_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.main_log = scrolledtext.ScrolledText(log_frame, height=8, bg="#000000", fg="#00ff00", font=("Consolas", 9),
                                                  insertbackground="white")
        self.main_log.pack(fill=tk.BOTH, expand=True)
        self.log(self.main_log, "NTH Cyber Suite Inicializado.", "INFO")

    def start_monitoring(self):
        self.monitor_running = True
        self.update_dashboard()

    def update_dashboard(self):
        if not self.monitor_running:
            return

        try:
            cpu = psutil.cpu_percent(interval=0.5)
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent

            self.cpu_var.set(cpu)
            self.ram_var.set(ram)
            self.disk_var.set(disk)
            self.value_labels["CPU"].config(text=f"{cpu:.1f}%")
            self.value_labels["RAM"].config(text=f"{ram:.1f}%")
            self.value_labels["DISK"].config(text=f"{disk:.1f}%")

            self.proc_tree.delete(*self.proc_tree.get_children())
            processes = sorted(
                psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']),
                key=lambda p: p.info['cpu_percent'] or 0,
                reverse=True
            )[:10]
            for p in processes:
                if p.info['name']:
                    self.proc_tree.insert(
                        "", tk.END,
                        values=(
                            p.info['pid'],
                            p.info['name'],
                            f"{p.info['cpu_percent']:.1f}",
                            f"{p.info['memory_percent']:.1f}"
                        )
                    )

            if cpu > 80:
                self.log(self.main_log, f"ALERTA: CPU em {cpu:.1f}%", "WARN")
            if ram > 85:
                self.log(self.main_log, f"ALERTA: RAM em {ram:.1f}%", "WARN")
        except Exception as e:
            self.log(self.main_log, f"Erro no monitoramento: {e}", "CRIT")

        self.root.after(1000, self.update_dashboard)

    # =========================================================================
    # FERRAMENTA 2: FILE SENTINEL
    # =========================================================================
    def build_file_sentinel(self, tab):
        frame = tk.Frame(tab, bg=self.PANEL)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(frame, text="FILE INTEGRITY & MALWARE SIGNATURE CHECK", font=("Segoe UI", 14, "bold"),
                 fg=self.CYAN, bg=self.PANEL).pack(pady=10)

        control_frame = tk.Frame(frame, bg=self.PANEL)
        control_frame.pack(pady=10)
        tk.Button(control_frame, text="Select File for Hashing", command=lambda: self.process_file("file"),
                  bg=self.CYAN, fg="black", font=("Segoe UI", 10, "bold"), width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Scan Directory", command=lambda: self.process_file("dir"), bg=self.MAGENTA,
                  fg="black", font=("Segoe UI", 10, "bold"), width=20).pack(side=tk.LEFT, padx=5)

        result_frame = tk.LabelFrame(frame, text=" ANALYSIS RESULTS ", font=("Segoe UI", 10, "bold"), fg=self.GREEN,
                                     bg=self.PANEL)
        result_frame.pack(fill=tk.BOTH, expand=True)
        self.file_log = scrolledtext.ScrolledText(result_frame, height=15, bg="#000000", fg="#00ff00",
                                                  font=("Consolas", 9))
        self.file_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def process_file(self, mode):
        if mode == "file":
            path = filedialog.askopenfilename(title="Select File")
            if path:
                self.analyze_file(path)
        else:
            path = filedialog.askdirectory(title="Select Directory")
            if path:
                self.analyze_directory(path)

    def analyze_file(self, filepath):
        def _worker():
            self.log(self.file_log, f"Analisando: {os.path.basename(filepath)}", "INFO")
            try:
                with open(filepath, "rb") as f:
                    md5 = hashlib.md5()
                    sha256 = hashlib.sha256()
                    for chunk in iter(lambda: f.read(8192), b""):
                        md5.update(chunk)
                        sha256.update(chunk)
                self.log(self.file_log, f"MD5:    {md5.hexdigest()}", "INFO")
                self.log(self.file_log, f"SHA256: {sha256.hexdigest()}", "INFO")

                ext = os.path.splitext(filepath)[1].lower()
                if ext in ['.exe', '.bat', '.scr', '.vbs', '.js', '.ps1']:
                    self.log(self.file_log, "AVISO: Arquivo executável detectado.", "WARN")
                if 'temp' in filepath.lower() or 'appdata' in filepath.lower():
                    self.log(self.file_log, "ALERTA: Arquivo em diretório de sistema. Possível ameaça.", "CRIT")
                self.log(self.file_log, "Análise concluída.", "INFO")
            except Exception as e:
                self.log(self.file_log, f"Erro: {str(e)}", "CRIT")

        threading.Thread(target=_worker, daemon=True).start()

    def analyze_directory(self, dir_path):
        def _worker():
            self.log(self.file_log, f"Scan em: {dir_path}", "INFO")
            count = 0
            suspicious = []
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    count += 1
                    if file.endswith(('.exe', '.dll', '.sys', '.sh', '.bat', '.ps1', '.vbs')):
                        suspicious.append(file)
            self.log(self.file_log, f"Total: {count} arquivos.", "INFO")
            self.log(self.file_log, f"Suspicious executables: {len(suspicious)}", "WARN")
            if suspicious:
                self.log(self.file_log, "Exemplos: " + ", ".join(suspicious[:5]), "CRIT")

        threading.Thread(target=_worker, daemon=True).start()

    # =========================================================================
    # FERRAMENTA 3: NETWORK DEFENSE
    # =========================================================================
    def build_network_defense(self, tab):
        frame = tk.Frame(tab, bg=self.PANEL)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(frame, text="NETWORK INTRUSION DETECTION", font=("Segoe UI", 14, "bold"), fg=self.CYAN,
                 bg=self.PANEL).pack(pady=10)

        control_frame = tk.Frame(frame, bg=self.PANEL)
        control_frame.pack(pady=10)
        tk.Button(control_frame, text="Active Connections", command=self.show_connections, bg=self.GREEN,
                  fg="black", font=("Segoe UI", 10, "bold"), width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="IP Configuration", command=self.show_ip_config, bg=self.CYAN, fg="black",
                  font=("Segoe UI", 10, "bold"), width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Port Scan (Local)", command=self.scan_local_ports, bg=self.MAGENTA,
                  fg="black", font=("Segoe UI", 10, "bold"), width=20).pack(side=tk.LEFT, padx=5)

        result_frame = tk.LabelFrame(frame, text=" NETWORK LOG ", font=("Segoe UI", 10, "bold"), fg=self.GREEN,
                                     bg=self.PANEL)
        result_frame.pack(fill=tk.BOTH, expand=True)
        self.net_log = scrolledtext.ScrolledText(result_frame, height=15, bg="#000000", fg="#00ff00",
                                                 font=("Consolas", 9))
        self.net_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def show_connections(self):
        def _worker():
            self.log(self.net_log, "Coletando conexões ativas...", "NET")
            try:
                conns = psutil.net_connections(kind='inet')
                self.log(self.net_log, f"Total de conexões ativas: {len(conns)}", "NET")
                for conn in conns[:15]:
                    status = conn.status
                    laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
                    raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                    self.log(self.net_log, f"[{status}] Local: {laddr} | Remote: {raddr}", "NET")
            except Exception as e:
                self.log(self.net_log, f"Erro ao coletar conexões: {e}", "CRIT")

        threading.Thread(target=_worker, daemon=True).start()

    def show_ip_config(self):
        def _worker():
            self.log(self.net_log, "Coletando configuração de IP...", "NET")
            if self.os_name == "Windows":
                cmd = "ipconfig"
            else:
                cmd = "ifconfig" if self.os_name != "Linux" else "ip addr"
            output = self.run_command(cmd)
            self.log(self.net_log, output, "NET")

        threading.Thread(target=_worker, daemon=True).start()

    def scan_local_ports(self):
        def _worker():
            self.log(self.net_log, "Iniciando varredura de portas locais (1-1024)...", "NET")
            open_ports = []
            for port in range(1, 1025):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.05)
                    result = sock.connect_ex(('127.0.0.1', port))
                    if result == 0:
                        open_ports.append(port)
                        self.log(self.net_log, f"Porta Aberta: {port}", "CRIT")
                    sock.close()
                except Exception:
                    pass
            if not open_ports:
                self.log(self.net_log, "Nenhuma porta crítica aberta.", "INFO")
            else:
                self.log(self.net_log, f"Portas abertas encontradas: {open_ports}", "WARN")

        threading.Thread(target=_worker, daemon=True).start()

    # =========================================================================
    # FERRAMENTA 4: LOG HUNTER
    # =========================================================================
    def build_log_hunter(self, tab):
        frame = tk.Frame(tab, bg=self.PANEL)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(frame, text="SYSTEM LOG ANALYSIS & THREAT DETECTION", font=("Segoe UI", 14, "bold"), fg=self.CYAN,
                 bg=self.PANEL).pack(pady=10)

        control_frame = tk.Frame(frame, bg=self.PANEL)
        control_frame.pack(pady=10)
        tk.Button(control_frame, text="Analyze System Logs", command=self.analyze_system_logs, bg=self.MAGENTA,
                  fg="black", font=("Segoe UI", 10, "bold"), width=20).pack(side=tk.LEFT, padx=5)

        result_frame = tk.LabelFrame(frame, text=" LOG ANALYSIS RESULTS ", font=("Segoe UI", 10, "bold"),
                                     fg=self.GREEN, bg=self.PANEL)
        result_frame.pack(fill=tk.BOTH, expand=True)
        self.log_analyzer = scrolledtext.ScrolledText(result_frame, height=15, bg="#000000", fg="#00ff00",
                                                      font=("Consolas", 9))
        self.log_analyzer.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def analyze_system_logs(self):
        def _worker():
            self.log(self.log_analyzer, "Iniciando análise de logs de sistema...", "INFO")

            if self.os_name == "Windows":
                cmd = [
                    "powershell", "-command",
                    "Get-WinEvent -LogName Security, System -MaxEvents 50 | "
                    "Where-Object {$_.Message -match 'denied|failed|error|attack|sudo|unauthorized'} | "
                    "Format-Table TimeCreated, Id, Message -AutoSize"
                ]
                output = self.run_command(cmd)
            elif self.os_name == "Darwin":  # macOS
                cmd = [
                    "log", "show", "--last", "1h",
                    "--predicate",
                    'eventMessage CONTAINS[c] "denied" OR eventMessage CONTAINS[c] "failed" OR eventMessage CONTAINS[c] "attack"',
                    "--style", "compact"
                ]
                output = self.run_command(cmd)
            else:  # Linux
                cmd = "journalctl --since '1 hour ago' --no-pager | grep -iE 'denied|failed|error|attack|sudo|unauthorized' | tail -n 20"
                output = self.run_command(cmd)

            self.log(self.log_analyzer, f"Análise concluída. Eventos suspeitos encontrados:\n\n{output}", "CRIT")

        threading.Thread(target=_worker, daemon=True).start()

    # =========================================================================
    # FERRAMENTA 5: PROCESS AUDITOR
    # =========================================================================
    def build_process_auditor(self, tab):
        frame = tk.Frame(tab, bg=self.PANEL)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(frame, text="PROCESS AUDIT & PRIVILEGE ESCALATION CHECK", font=("Segoe UI", 14, "bold"),
                 fg=self.CYAN, bg=self.PANEL).pack(pady=10)

        control_frame = tk.Frame(frame, bg=self.PANEL)
        control_frame.pack(pady=10)
        tk.Button(control_frame, text="Audit Processes", command=self.audit_processes, bg=self.GREEN, fg="black",
                  font=("Segoe UI", 10, "bold"), width=20).pack(side=tk.LEFT, padx=5)

        result_frame = tk.LabelFrame(frame, text=" PROCESS AUDIT RESULTS ", font=("Segoe UI", 10, "bold"),
                                     fg=self.GREEN, bg=self.PANEL)
        result_frame.pack(fill=tk.BOTH, expand=True)
        self.proc_audit_log = scrolledtext.ScrolledText(result_frame, height=15, bg="#000000", fg="#00ff00",
                                                        font=("Consolas", 9))
        self.proc_audit_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def audit_processes(self):
        def _worker():
            self.log(self.proc_audit_log, "Auditoria de processos iniciada...", "INFO")
            suspicious_patterns = ['powershell', 'cmd', 'sh', 'bash', 'python', 'perl', 'ruby', 'node', 'curl', 'wget']
            high_priv = []

            for proc in psutil.process_iter(['pid', 'name', 'username', 'cmdline']):
                try:
                    name = (proc.info['name'] or "").lower()
                    user = proc.info['username'] or "unknown"
                    cmdline = ' '.join(proc.info['cmdline'] or [])

                    is_scripting = any(pattern in name for pattern in suspicious_patterns) or any(
                        pattern in cmdline for pattern in suspicious_patterns)

                    is_elevated = user.lower() in ['root', 'administrator', 'system']

                    if is_scripting and is_elevated:
                        high_priv.append(f"PID {proc.info['pid']} | User: {user} | Cmd: {cmdline[:100]}")
                        self.log(self.proc_audit_log,
                                 f"ALERTA: Processo elevado detectado: {proc.info['name']} (User: {user})", "CRIT")

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            if not high_priv:
                self.log(self.proc_audit_log, "Nenhum processo de script com privilégios elevados detectado.", "INFO")
            else:
                self.log(self.proc_audit_log, f"Total de processos suspeitos com privilégios: {len(high_priv)}", "WARN")

        threading.Thread(target=_worker, daemon=True).start()

    # =========================================================================
    # FERRAMENTA 6: SYSTEM AUDIT
    # =========================================================================
    def build_system_audit(self, tab):
        frame = tk.Frame(tab, bg=self.PANEL)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(frame, text="SYSTEM HARDWARE & SECURITY POSTURE AUDIT", font=("Segoe UI", 14, "bold"),
                 fg=self.CYAN, bg=self.PANEL).pack(pady=10)

        control_frame = tk.Frame(frame, bg=self.PANEL)
        control_frame.pack(pady=10)
        tk.Button(control_frame, text="Run Full Audit", command=self.run_system_audit, bg=self.MAGENTA, fg="black",
                  font=("Segoe UI", 10, "bold"), width=20).pack(side=tk.LEFT, padx=5)

        result_frame = tk.LabelFrame(frame, text=" AUDIT REPORT ", font=("Segoe UI", 10, "bold"), fg=self.GREEN,
                                     bg=self.PANEL)
        result_frame.pack(fill=tk.BOTH, expand=True)
        self.audit_log = scrolledtext.ScrolledText(result_frame, height=15, bg="#000000", fg="#00ff00",
                                                   font=("Consolas", 9))
        self.audit_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def run_system_audit(self):
        def _worker():
            self.log(self.audit_log, "Gerando relatório de auditoria de sistema...", "INFO")

            # 1. Informações Básicas
            self.log(self.audit_log, f"SO: {platform.system()} {platform.release()} ({platform.machine()})", "INFO")
            self.log(self.audit_log, f"Hostname: {socket.gethostname()}", "INFO")

            # 2. Uptime
            boot_time = psutil.boot_time()
            uptime_seconds = time.time() - boot_time
            uptime_hours = uptime_seconds / 3600
            self.log(self.audit_log, f"Uptime: {uptime_hours:.2f} horas", "INFO")

            # 3. Firewall Status
            if self.os_name == "Windows":
                cmd = "netsh advfirewall show allprofiles state"
                output = self.run_command(cmd)
                if "Ativado" in output or "Enabled" in output:
                    self.log(self.audit_log, "Firewall: ATIVO", "INFO")
                else:
                    self.log(self.audit_log, "Firewall: INATIVO OU DESCONHECIDO", "CRIT")
            elif self.os_name == "Darwin":
                cmd = "pfctl -s info"
                output = self.run_command(cmd)
                if "Status: Enabled" in output or "Status: for enabled" in output:
                    self.log(self.audit_log, "Firewall (pf): ATIVO", "INFO")
                else:
                    self.log(self.audit_log, "Firewall (pf): INATIVO", "CRIT")
            else:
                # Linux: Verifica iptables/nftables
                cmd = "iptables -L -n"
                output = self.run_command(cmd)
                if "Chain" in output:
                    self.log(self.audit_log, "Firewall (iptables): ATIVO", "INFO")
                else:
                    self.log(self.audit_log, "Firewall (iptables): INATIVO OU SEM REGRAS", "CRIT")

            # 4. Usuários Ativos
            users = psutil.users()
            self.log(self.audit_log, f"Usuários logados: {len(users)}", "INFO")
            for user in users:
                self.log(self.audit_log, f"  - {user.name}", "INFO")

            # 5. Serviços de Rede (Portas Ouvindo)
            listening_ports = []
            try:
                for conn in psutil.net_connections(kind='inet'):
                    if conn.status == 'LISTEN' and conn.laddr:
                        listening_ports.append(f"{conn.laddr.ip}:{conn.laddr.port}")
            except Exception:
                pass

            self.log(self.audit_log, f"Portas em escuta: {len(listening_ports)}", "INFO")
            for port in listening_ports[:10]:
                self.log(self.audit_log, f"  - {port}", "NET")

            self.log(self.audit_log, "Auditoria concluída.", "INFO")

        threading.Thread(target=_worker, daemon=True).start()

    # =========================================================================
    # INICIALIZAÇÃO DAS ABAS
    # =========================================================================
    def _init_tabs(self):
        self.build_dashboard(self.tab_dashboard)
        self.build_file_sentinel(self.tab_files)
        self.build_network_defense(self.tab_network)
        self.build_log_hunter(self.tab_logs)
        self.build_process_auditor(self.tab_processes)
        self.build_system_audit(self.tab_audit)


# =========================================================================
# PONTO DE ENTRADA
# =========================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = NTHCyberSuite(root)
    root.mainloop()
