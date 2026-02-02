import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import socket
import threading
import time
import platform
import subprocess
import ctypes
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as pdf_canvas

DEFAULT_DNS_SERVERS = {
    'Google': '8.8.8.8',
    'Cloudflare': '1.1.1.1',
    'OpenDNS': '208.67.222.222',
    'Quad9': '9.9.9.9'
}

# Theme colors
THEMES = {
    'dark': {
        'bg': '#1e1e1e',
        'fg': '#ffffff',
        'accent': "#6fff00",
        'text_bg': '#111111',
        'text_fg': 'lime',
        'tree_bg': '#2e2e2e',
        'tree_fg': 'white',
        'tree_field': '#2e2e2e',
        'tree_heading': '#333333',
        'button_bg': '#008080',
        'export_bg': '#444444',
        'figure_facecolor': '#1e1e1e',
        'axis_color': 'white'
    },
    'light': {
        'bg': '#f0f0f0',
        'fg': '#000000',
        'accent': '#0066cc',
        'text_bg': '#ffffff',
        'text_fg': 'black',
        'tree_bg': '#ffffff',
        'tree_fg': 'black',
        'tree_field': '#ffffff',
        'tree_heading': '#e0e0e0',
        'button_bg': '#4CAF50',
        'export_bg': '#607d8b',
        'figure_facecolor': '#f5f5f5',
        'axis_color': 'black'
    }
}

def is_admin():
    """Check if the program is running with admin privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Restart the program with admin privileges"""
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

def change_dns_windows(interface, dns_server):
    """Change DNS settings on Windows"""
    try:
        subprocess.run(f'netsh interface ip set dns name="{interface}" static {dns_server} primary', shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error changing DNS: {e}")
        return False

def change_dns_linux(dns_server):
    """Change DNS settings on Linux"""
    try:
        with open('/etc/resolv.conf', 'w') as f:
            f.write(f"nameserver {dns_server}\n")
        return True
    except PermissionError:
        print("Permission denied - need sudo")
        return False

def measure_latency(dns_ip, timeout=2):
    try:
        start = time.time()
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((dns_ip, 53))
        latency = (time.time() - start) * 1000
        return round(latency, 2)
    except:
        return None

class DNSAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DNS Analyzer Tool")
        self.root.geometry("800x650")
        
        self.current_theme = 'dark'
        self.dns_servers = DEFAULT_DNS_SERVERS.copy()
        self.results = []
        self.fastest_dns = None
        
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Main frames
        self.header_frame = tk.Frame(self.root)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        
        self.content_frame = tk.Frame(self.root)
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        
        # Header
        self.title_label = tk.Label(self.header_frame, text="DNS Analyzer Tool", font=("Segoe UI", 20))
        self.title_label.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.theme_button = tk.Button(self.header_frame, text="☀️", command=self.toggle_theme, font=("Segoe UI", 12))
        self.theme_button.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # DNS Entry
        self.entry_frame = tk.Frame(self.content_frame)
        self.entry_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(self.entry_frame, text="Add Custom DNS IP:").grid(row=0, column=0, padx=5)
        self.custom_entry = tk.Entry(self.entry_frame)
        self.custom_entry.grid(row=0, column=1, sticky="ew", padx=5)
        tk.Button(self.entry_frame, text="Add", command=self.add_custom_dns).grid(row=0, column=2, padx=5)
        
        # Control Frame
        self.control_frame = tk.Frame(self.content_frame)
        self.control_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Analysis Button and Progress
        self.button_frame = tk.Frame(self.control_frame)
        self.button_frame.pack(fill=tk.X)
        
        self.analyze_button = tk.Button(self.button_frame, text="Analyze DNS Servers", command=self.start_analysis)
        self.analyze_button.pack(side=tk.LEFT)
        
        self.progress = ttk.Progressbar(self.button_frame, mode='determinate')
        self.progress.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=10)
        
        # Results Table
        self.tree = ttk.Treeview(self.control_frame, columns=("IP", "Latency"), show='headings', height=6)
        self.tree.heading("IP", text="DNS IP")
        self.tree.heading("Latency", text="Latency (ms)")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Graph
        self.figure = plt.Figure(figsize=(6, 3), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.control_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Status Log
        self.status_text = tk.Text(self.control_frame, height=6, font=("Consolas", 10))
        self.status_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Export Button
        self.export_button = tk.Button(self.content_frame, text="Export Summary as PDF", command=self.export_to_pdf)
        self.export_button.pack(pady=10)

    def apply_theme(self):
        theme = THEMES[self.current_theme]
        
        # Apply to root and frames
        self.root.configure(bg=theme['bg'])
        self.header_frame.configure(bg=theme['bg'])
        self.content_frame.configure(bg=theme['bg'])
        self.entry_frame.configure(bg=theme['bg'])
        self.control_frame.configure(bg=theme['bg'])
        self.button_frame.configure(bg=theme['bg'])
        
        # Apply to widgets
        self.title_label.configure(bg=theme['bg'], fg=theme['accent'])
        self.theme_button.configure(bg=theme['bg'], fg=theme['fg'], activebackground=theme['bg'])
        
        for child in self.entry_frame.winfo_children():
            if isinstance(child, tk.Label):
                child.configure(bg=theme['bg'], fg=theme['fg'])
            elif isinstance(child, tk.Entry):
                child.configure(bg='white', fg='black')  # Keep entry fields readable
        
        self.analyze_button.configure(bg=theme['button_bg'], fg='white')
        self.export_button.configure(bg=theme['export_bg'], fg='white')
        
        # Configure Treeview
        self.style.configure("Treeview",
                            background=theme['tree_bg'],
                            foreground=theme['tree_fg'],
                            fieldbackground=theme['tree_field'])
        self.style.configure("Treeview.Heading",
                            background=theme['tree_heading'],
                            foreground=theme['tree_fg'])
        
        # Configure status text
        self.status_text.configure(bg=theme['text_bg'], fg=theme['text_fg'])
        
        # Configure graph
        self.figure.set_facecolor(theme['figure_facecolor'])
        self.ax.set_title("DNS Server Latency", color=theme['axis_color'])
        self.ax.set_xlabel("Latency (ms)", color=theme['axis_color'])
        self.ax.tick_params(colors=theme['axis_color'])
        self.ax.spines['bottom'].set_color(theme['axis_color'])
        self.ax.spines['top'].set_color(theme['axis_color'])
        self.ax.spines['left'].set_color(theme['axis_color'])
        self.ax.spines['right'].set_color(theme['axis_color'])
        
        # Redraw if we have data
        if hasattr(self, 'results') and self.results:
            self.redraw_graph()

    def toggle_theme(self):
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        self.theme_button.config(text="🌙" if self.current_theme == 'dark' else "☀️")
        self.apply_theme()

    def redraw_graph(self):
        if not hasattr(self, 'results') or not self.results:
            return
            
        min_latency = min([r[2] for r in self.results if isinstance(r[2], float)], default=0)
        
        self.ax.clear()
        names = [f"{name}\n{ip}" for name, ip, _ in self.results]
        latencies = [latency if isinstance(latency, float) else 0 for _, _, latency in self.results]
        theme = THEMES[self.current_theme]
        colors = ['#00ff00' if isinstance(lat, float) and lat == min_latency else theme['accent'] for _, _, lat in self.results]
        
        self.ax.barh(names, latencies, color=colors)
        self.ax.set_title("DNS Server Latency", color=theme['axis_color'])
        self.ax.set_xlabel("Latency (ms)", color=theme['axis_color'])
        self.ax.tick_params(colors=theme['axis_color'])
        self.figure.tight_layout()
        self.canvas.draw()

    def log_status(self, msg):
        self.status_text.insert(tk.END, msg + "\n")
        self.status_text.see(tk.END)

    def add_custom_dns(self):
        ip = self.custom_entry.get().strip()
        if ip:
            name = f"Custom-{ip}"
            self.dns_servers[name] = ip
            self.custom_entry.delete(0, tk.END)
            messagebox.showinfo("Success", f"Added {ip} to test list")
        else:
            messagebox.showwarning("Input Error", "Please enter a valid IP")

    def start_analysis(self):
        threading.Thread(target=self.analyze_dns_servers).start()

    def analyze_dns_servers(self):
        self.tree.delete(*self.tree.get_children())
        self.ax.clear()
        self.results = []
        self.status_text.delete("1.0", tk.END)
        self.progress["maximum"] = len(self.dns_servers)
        self.progress["value"] = 0

        best = None
        min_latency = float('inf')

        for i, (name, ip) in enumerate(self.dns_servers.items(), 1):
            self.log_status(f"Testing {name} ({ip})...")
            latency = measure_latency(ip)
            if latency is not None:
                self.results.append((name, ip, latency))
                if latency < min_latency:
                    best = (name, ip)
                    min_latency = latency
                self.log_status(f"→ Latency: {latency} ms")
            else:
                self.results.append((name, ip, "Timeout"))
                self.log_status(f"→ Timeout")

            self.progress["value"] = i
            self.root.update_idletasks()

        for _, ip, latency in self.results:
            self.tree.insert('', tk.END, values=(ip, latency))

        self.redraw_graph()

        if best:
            self.fastest_dns = best
            self.log_status(f"\nFastest DNS: {best[0]} ({best[1]}) - {min_latency} ms")
            self.prompt_dns_change(best[1])
        else:
            messagebox.showerror("Error", "No DNS servers responded")

    def prompt_dns_change(self, dns_ip):
        response = messagebox.askyesno(
            "Change DNS Settings",
            f"Do you want to change your system DNS to {dns_ip}?\n\n"
            "This requires administrator privileges.",
            icon='question'
        )
        
        if response:
            if not is_admin():
                messagebox.showwarning(
                    "Admin Required",
                    "The application needs administrator privileges to change DNS settings.\n"
                    "Please restart the program as administrator."
                )
                return
            
            os_name = platform.system()
            success = False
            
            if os_name == "Windows":
                try:
                    result = subprocess.run('netsh interface show interface', shell=True, capture_output=True, text=True)
                    interfaces = [line.split()[-1] for line in result.stdout.split('\n') if "Connected" in line]
                    
                    for interface in interfaces:
                        if change_dns_windows(interface, dns_ip):
                            success = True
                            self.log_status(f"Changed DNS to {dns_ip} on interface {interface}")
                except Exception as e:
                    self.log_status(f"Error changing DNS: {str(e)}")
            
            elif os_name == "Linux":
                if change_dns_linux(dns_ip):
                    success = True
                    self.log_status(f"Changed DNS to {dns_ip}")
            
            if success:
                messagebox.showinfo("Success", f"DNS successfully changed to {dns_ip}")
            else:
                messagebox.showerror("Error", "Failed to change DNS settings")

    def export_to_pdf(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not file_path:
            return

        pdf = pdf_canvas.Canvas(file_path, pagesize=A4)
        pdf.setFont("Helvetica", 14)
        pdf.drawString(50, 800, "DNS Analyzer Tool Summary")
        pdf.setFont("Helvetica", 12)

        y = 770
        for name, ip, latency in self.results:
            text = f"{name} - {ip} -> {latency} ms" if isinstance(latency, float) else f"{name} - {ip} -> Timeout"
            pdf.drawString(50, y, text)
            y -= 20
            if y < 100:
                pdf.showPage()
                pdf.setFont("Helvetica", 12)
                y = 800

        pdf.save()
        messagebox.showinfo("Exported", "Summary exported to PDF successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = DNSAnalyzerApp(root)
    root.mainloop()