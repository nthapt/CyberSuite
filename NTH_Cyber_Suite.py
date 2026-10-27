import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import psutil
import socket
import subprocess
import hashlib
import os
import platform
import threading
import time
from datetime import datetime

class NTHCyberSuite:
    def __init__(self, root):
        self.root = root
        self.root.title("NTH CYBER SUITE v1.0 | Advanced Security Toolkit")
        self.root.geometry("1500x950")
        self.root.configure(bg="#0b0b12") # Fundo escuro profundo
        
        # Paleta RGB Profissional
        self.CYAN = "#00f3ff"
        self.MAGENTA = "#ff00ff"
        self.GREEN = "#00ff88"
        self.RED = "#ff3333"
        self.YELLOW = "#ffcc00"
        self.TEXT = "#e0e0e0"
        self.PANEL = "#151520"
        self.DARK = "#0b0b12"

        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configuração dos Widgets
        self.style.configure("TNotebook", background=self.PANEL, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=self.PANEL, foreground=self.TEXT, padding=[15, 10], font=("Segoe UI", 11, "bold"))
        self.style.map("TNotebook.Tab", background=[("selected", self.CYAN)], foreground=[("selected", self.DARK)])
        
        self.create_ui()
        self.start_monitoring()

    def create_ui(self):
        # Container Principal
        main_container = tk.Frame(self.root, bg=self.DARK)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # --- HEADER (Logo NTH) ---
        header_frame = tk.Frame(main_container, bg=self.PANEL, height=90)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)

        # Logo NTH Grande com efeito RGB (Simulado com cores)
        logo_label = tk.Label(header_frame, text="NTH", font=("Impact", 50), bg=self.PANEL, fg=self.CYAN)
        logo_label.pack(side=tk.LEFT, padx=30)
        
        # Efeito RGB no texto (Alternância simples de cores via after)
        self.rgb_colors = [self.CYAN, self.MAGENTA, self.GREEN]
        self.rgb_index = 0
        self.animate_logo(logo_label)

        tagline = tk.Label(header_frame, text="CYBERSECURITY SUITE", font=("Consolas", 14, "bold"), bg=self.PANEL, fg=self.MAGENTA)
        tagline.pack(side=tk.LEFT, padx=10, pady=30)

        # Status do Sistema
        self.status_label = tk.Label(header_frame, text="STATUS: ONLINE", font=("Consolas", 12, "bold"), bg=self.PANEL, fg=self.GREEN)
        self.status_label.pack(side=tk.RIGHT, padx=30)

        # --- TABS ---
        notebook = ttk.Notebook(main_container)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Abas
        self.tab_dashboard = self.create_tab(notebook, "📊 DASHBOARD & MONITOR")
        self.tab_files = self.create_tab(notebook, "📁 FILE ANALYSIS")
        self.tab_network = self.create_tab(notebook, "🌐 NETWORK DEFENSE")
        self.tab_ports = self.create_tab(notebook, "🔍 PORT SCANNER")
        self.tab_logs = self.create_tab(notebook, "📝 LOG ANALYZER")
        self.tab_defense = self.create_tab(notebook, "🛡️ DEFENSE & AUDIT")

    def animate_logo(self, label):
        """Animar a cor da logo para efeito RGB"""
        colors = [self.CYAN, self.MAGENTA, self.GREEN]
        current = colors[self.rgb_index % len(colors)]
        label.config(fg=current)
        self.rgb_index += 1
        self.root.after(500, lambda: self.animate_logo(label))

    def create_tab(self, parent, name):
        tab = tk.Frame(parent, bg=self.DARK)
        parent.add(tab, text=name)
        return tab

    # =========================================================================
    # FERRAMENTA 1: DASHBOARD & MONITORAMENTO EM TEMPO REAL
    # =========================================================================
    def build_dashboard(self, tab):
        # Grid de Layout
        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)

        # Painel Esquerdo: Métricas
        left_frame = tk.LabelFrame(tab, text=" REAL-TIME SYSTEM METRICS ", font=("Segoe UI", 12, "bold"), fg=self.CYAN, bg=self.PANEL, padx=10, pady=10)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)

        self.cpu_var = tk.DoubleVar(value=0)
        self.ram_var = tk.DoubleVar(value=0)
        self.disk_var = tk.DoubleVar(value=0)
        self.net_rx = tk.DoubleVar(value=0)
        self.net_tx = tk.DoubleVar(value=0)

        metrics_data = [
            ("CPU USAGE", "CPU", self.cpu_var),
            ("RAM USAGE", "RAM", self.ram_var),
            ("DISK USAGE", "DISK", self.disk_var),
        ]

        for i, (label, key, var) in enumerate(metrics_data):
            tk.Label(left_frame, text=label, font=("Consolas", 10, "bold"), bg=self.PANEL, fg=self.TEXT).grid(row=i*2, column=0, sticky="w", pady=5)
            progress = ttk.Progressbar(left_frame, orient="horizontal", length=200, variable=var)
            progress.grid(row=i*2, column=1, sticky="e", padx=10)
            self.progress_widgets = {}
            self.progress_widgets[key] = progress
            
            value_label = tk.Label(left_frame, text="0%", font=("Consolas", 10), bg=self.PANEL, fg=self.GREEN)
            value_label.grid(row=i*2+1, column=1, sticky="e", padx=10)
            self.value_labels = {}
            self.value_labels[key] = value_label

        # Painel Direito: Processos
        right_frame = tk.LabelFrame(tab, text=" TOP PROCESSES BY CPU ", font=("Segoe UI", 12, "bold"), fg=self.MAGENTA, bg=self.PANEL, padx=10, pady=10)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)

        cols = ("PID", "NAME", "CPU", "RAM")
        self.proc_tree = ttk.Treeview(right_frame, columns=cols, show="headings", height=10)
        self.proc_tree.heading("PID", text="PID")
        self.proc_tree.heading("NAME", text="Process")
        self.proc_tree.heading("CPU", text="CPU %")
        self.proc_tree.heading("RAM", text="RAM %")
        self.proc_tree.column("PID", width=60)
        self.proc_tree.column("NAME", width=150)
        self.proc_tree.column("CPU", width=60)
        self.proc_tree.column("RAM", width=60)
        self.proc_tree.pack(fill=tk.BOTH, expand=True)

        # Painel Inferior: Log de Eventos
        log_frame = tk.LabelFrame(tab, text=" SYSTEM EVENT LOG ", font=("Segoe UI", 12, "bold"), fg=self.GREEN, bg=self.PANEL, padx=10, pady=10)
        log_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        
        self.main_log = scrolledtext.ScrolledText(log_frame, height=8, bg="#000000", fg="#00ff00", font=("Consolas", 9), insertbackground="white")
        self.main_log.pack(fill=tk.BOTH, expand=True)
        self.log("NTH Cyber Suite Inicializado. Monitoramento ativo.")

    def start_monitoring(self):
        """Loop de atualização do Dashboard"""
        self.monitor_running = True
        self.update_dashboard()

    def update_dashboard(self):
        if not self.monitor_running: return
        
        # Coletar Dados
        cpu = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        net = psutil.net_io_counters()

        # Atualizar Barras
        self.cpu_var.set(cpu)
        self.ram_var.set(ram)
        self.disk_var.set(disk)
        
        # Atualizar Labels
        self.value_labels["CPU"].config(text=f"{cpu:.1f}%")
        self.value_labels["RAM"].config(text=f"{ram:.1f}%")
        self.value_labels["DISK"].config(text=f"{disk:.1f}%")

        # Atualizar Processos
        self.proc_tree.delete(*self.proc_tree.get_children())
        processes = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']), key=lambda p: p.info['cpu_percent'] or 0, reverse=True)[:10]
        for p in processes:
            if p.info['name']:
                self.proc_tree.insert("", tk.END, values=(p.info['pid'], p.info['name'], f"{p.info['cpu_percent']:.1f}", f"{p.info['memory_percent']:.1f}"))

        # Log de Alertas (Simulado)
        if cpu > 80:
            self.log("ALERTA: Uso de CPU elevado detectado.")
        if ram > 85:
            self.log("ALERTA: Memória RAM crítica.")

        # Agendar próxima atualização
        self.root.after(1000, self.update_dashboard)

    def log(self, widget, message, color=None):
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        widget.insert(tk.END, f"{timestamp} | {message}\n")
        widget.see(tk.END)

    # =========================================================================
    # FERRAMENTA 2: ANÁLISE DE ARQUIVOS (VÍRUS/INTEGRIDADE)
    # =========================================================================
    def build_file_analysis(self, tab):
        frame = tk.Frame(tab, bg=self.PANEL)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(frame, text="FILE INTEGRITY & MALWARE SIGNATURE CHECK", font=("Segoe UI", 14, "bold"), fg=self.CYAN, bg=self.PANEL).pack(pady=10)

        # Controles
        control_frame = tk.Frame(frame, bg=self.PANEL)
        control_frame.pack(pady=10)
        
        tk.Button(control_frame, text="Select File for Hashing", command=lambda: self.process_file("file"), bg=self.CYAN, fg="black", font=("Segoe UI", 10, "bold"), width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Scan Directory", command=lambda: self.process_file("dir"), bg=self.MAGENTA, fg="black", font=("Segoe UI", 10, "bold"), width=20).pack(side=tk.LEFT, padx=5)

        # Resultados
        result_frame = tk.LabelFrame(frame, text=" ANALYSIS RESULTS ", font=("Segoe UI", 10, "bold"), fg=self.GREEN, bg=self.PANEL)
        result_frame.pack(fill=tk.BOTH, expand=True)
        self.file_log = scrolledtext.ScrolledText(result_frame, height=15, bg="#000000", fg="#00ff00", font=("Consolas", 9))
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
            self.log(self.file_log, f"Analisando arquivo: {os.path.basename(filepath)}")
            try:
                # Cálculo de Hash para Integridade
                with open(filepath, "rb") as f:
                    md5 = hashlib.md5()
                    sha256 = hashlib.sha256()
                    for chunk in iter(lambda: f.read(8192), b""):
                        md5.update(chunk)
                        sha256.update(chunk)
                
                self.log(self.file_log, f"MD5:    {md5.hexdigest()}")
                self.log(self.file_log, f"SHA256: {sha256.hexdigest()}")
                
                # Heurística Básica de Extensão
                ext = os.path.splitext(filepath)[1].lower()
                if ext in ['.exe', '.bat', '.scr', '.vbs', '.js', '.ps1']:
                    self.log(self.file_log, "AVISO: Arquivo executável detectado. Verifique a origem.")
                    if 'temp' in filepath.lower() or 'appdata' in filepath.lower():
                        self.log(self.file_log, "ALERTA: Arquivo em diretório de sistema temporário. Possível ameaça.")
                
                self.log(self.file_log, "Análise de integridade concluída.")
            except Exception as e:
                self.log(self.file_log, f"Erro na análise: {str(e)}")
        threading.Thread(target=_worker, daemon=True).start()

    def analyze_directory(self, dir_path):
        def _worker():
            self.log(self.file_log, f"Iniciando scan em: {dir_path}")
            count = 0
            suspicious = []
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    count += 1
                    if file.endswith(('.exe', '.dll', '.sys')):
                        suspicious.append(file)
            self.log(self.file_log, f"Scan concluído. Total de arquivos: {count}")
            self.log(self.file_log, f"Arquivos potencialmente críticos encontrados: {len(suspicious)}")
            if suspicious:
                self.log(self.file_log, "Exemplos: " + ", ".join(suspicious[:5]))
        threading.Thread(target=_worker, daemon=True).start()

    # =========================================================================
    # FERRAMENTA 3: ANÁLISE DE REDE (ATACOS E TRÁFEGO)
    # =========================================================================
    def build_network_analysis(self, tab):
        frame = tk.Frame(tab, bg=self.PANEL)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(frame, text="NETWORK INTRUSION DETECTION & MONITORING", font=("Segoe UI", 14, "bold"), fg=self.CYAN, bg=self.PANEL).pack(pady=10)

        control_frame = tk.Frame(frame, bg=self.PANEL)
        control_frame.pack(pady=10)
        tk.Button(control_frame, text="Active Connections", command=self.show_connections, bg=self.GREEN, fg="black", font=("Segoe UI", 10, "bold"), width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="IP Configuration", command=self.show_ip_config, bg=self.CYAN, fg="black", font=("Segoe UI", 10, "bold"), width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Ping Test", command=self.ping_test, bg=self.MAGENTA, fg="black", font=("Segoe UI", 10, "bold"), width=20).pack(side=tk.LEFT, padx=5)

        result_frame = tk.LabelFrame(frame, text=" NETWORK LOG ", font=("Segoe UI", 10, "bold"), fg=self.GREEN, bg=self.PANEL)
        result_frame.pack(fill=tk.BOTH, expand=True)
        self.net_log = scrolledtext.ScrolledText(result_frame, height=15, bg="#000000", fg="#00ff00", font=("Consolas", 9))
        self.net_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def show_connections(self):
        def _worker():
            self.log(self.net_log, "Coletando conexões ativas...")
            conns = psutil.net_connections(kind='inet')
            self.log(self.net_log, f"Total de conexões ativas: {len(conns)}")
            for conn in conns[:10]: # Limita a 10 para performance
                status = conn.status
                laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
                raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                self