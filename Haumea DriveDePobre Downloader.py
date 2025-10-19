import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import requests
import os
import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import webbrowser
import math
import logging
from datetime import datetime

# Obrigado por usar o Haumea!

class DriveDePobreGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Haumea DriveDePobre Downloader")
        self.root.geometry("1280x800")
        self.root.configure(bg='#0d1117')
        
        # Configurar logging
        self.setup_logging()
        
        # Variáveis
        self.files_data = []
        self.selected_files = {}
        self.download_folder = "downloads"
        self.folder_structure = {}
        self.tree_items = {}
        
        # Configurar tema escuro
        self.setup_dark_theme()
        
        # Configurar sessão
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
        })
        
        self.create_widgets()
        self.create_download_folder()
    
    def setup_logging(self):
        """Configura o sistema de logging"""
        log_folder = "logs"
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_folder, f"download_log_{timestamp}.txt")
        
        # Configurar logging para arquivo e console
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("=" * 60)
        self.logger.info("🌟 Haumea DriveDePobre Downloader v2.0")
        self.logger.info(f"Arquivo de log: {log_file}")
        self.logger.info("=" * 60)
    
    def setup_dark_theme(self):
        """Configura o tema escuro moderno"""
        style = ttk.Style()
        
        # Configurar cores do tema - Paleta moderna e vibrante
        self.colors = {
            'bg': '#0d1117',
            'bg_secondary': '#161b22',
            'bg_tertiary': '#21262d',
            'bg_card': '#1c2128',
            'fg': '#f0f6fc',
            'fg_secondary': '#8b949e',
            'fg_tertiary': '#6e7681',
            'accent': '#58a6ff',
            'accent_hover': '#79c0ff',
            'accent_dark': '#1f6feb',
            'success': '#3fb950',
            'success_hover': '#56d364',
            'warning': '#d29922',
            'danger': '#f85149',
            'border': '#30363d',
            'border_hover': '#484f58',
            'purple': '#bc8cff',
            'pink': '#ff7eb6',
            'orange': '#ffa657'
        }
        
        # Configurar estilo
        style.theme_use('clam')
        
        # Configurar estilos personalizados
        style.configure('Dark.TFrame', background=self.colors['bg'])
        style.configure('Dark.TLabel', background=self.colors['bg'], foreground=self.colors['fg'])
        style.configure('Dark.TLabelframe', background=self.colors['bg'], foreground=self.colors['fg'])
        style.configure('Dark.TLabelframe.Label', background=self.colors['bg'], foreground=self.colors['fg'])
        style.configure('Dark.TButton', 
                       background=self.colors['bg_tertiary'],
                       foreground=self.colors['fg'],
                       borderwidth=1,
                       relief='flat',
                       focuscolor='none',
                       padding=(16, 10))
        style.map('Dark.TButton',
                 background=[('active', self.colors['border_hover']),
                           ('disabled', self.colors['bg_secondary'])],
                 bordercolor=[('active', self.colors['border_hover'])])
        
        style.configure('Accent.TButton',
                       background=self.colors['accent'],
                       foreground='#ffffff',
                       borderwidth=0,
                       relief='flat',
                       padding=(24, 12))
        style.map('Accent.TButton',
                 background=[('active', self.colors['accent_hover']),
                           ('disabled', self.colors['bg_tertiary'])])
        
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground='#ffffff',
                       borderwidth=0,
                       relief='flat',
                       padding=(20, 10))
        style.map('Success.TButton',
                 background=[('active', self.colors['success_hover'])])
        
        style.configure('Treeview',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['fg'],
                       fieldbackground=self.colors['bg_secondary'],
                       borderwidth=0,
                       relief='flat')
        style.configure('Treeview.Heading',
                       background=self.colors['bg_tertiary'],
                       foreground=self.colors['fg'],
                       relief='flat',
                       borderwidth=0)
        style.map('Treeview.Heading',
                 background=[('active', self.colors['bg_tertiary'])])
        
        style.configure('Dark.Horizontal.TProgressbar',
                       background=self.colors['accent'],
                       troughcolor=self.colors['bg_tertiary'],
                       borderwidth=0,
                       lightcolor=self.colors['accent'],
                       darkcolor=self.colors['accent'])
        
        style.configure('Dark.TEntry',
                       fieldbackground=self.colors['bg_secondary'],
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['fg'],
                       insertcolor=self.colors['fg'],
                       borderwidth=1,
                       relief='flat')
        style.map('Dark.TEntry',
                 fieldbackground=[('focus', self.colors['bg_tertiary'])])
    
    def create_download_folder(self):
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
    
    def create_widgets(self):
        # Frame principal com padding moderno
        main_container = ttk.Frame(self.root, style='Dark.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header moderno com design aprimorado
        header_frame = ttk.Frame(main_container, style='Dark.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Logo e título
        title_container = ttk.Frame(header_frame, style='Dark.TFrame')
        title_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        
        # Título principal com destaque
        title_label = tk.Label(title_container, 
                              text="🌟 Haumea",
                              font=('Segoe UI', 28, 'bold'),
                              bg=self.colors['bg'],
                              fg=self.colors['accent'])
        title_label.pack(anchor=tk.W, pady=(0, 0))
        
        # Subtítulo do projeto
        subtitle_label = tk.Label(title_container,
                                 text="DriveDePobre Downloader",
                                 font=('Segoe UI', 14),
                                 bg=self.colors['bg'],
                                 fg=self.colors['fg_secondary'])
        subtitle_label.pack(anchor=tk.W, pady=(0, 0))
        
        # Badge de versão
        version_label = tk.Label(header_frame,
                                text="v2.0",
                                font=('Segoe UI', 10, 'bold'),
                                bg=self.colors['bg_tertiary'],
                                fg=self.colors['purple'],
                                padx=12, pady=6)
        version_label.pack(side=tk.RIGHT, anchor=tk.N)
        
        # URL Input Frame com visual moderno
        url_frame = ttk.LabelFrame(main_container, text="  🔗  URL da Pasta  ", 
                                  style='Dark.TLabelframe', padding=15)
        url_frame.pack(fill=tk.X, pady=(0, 15))
        
        url_inner = ttk.Frame(url_frame, style='Dark.TFrame')
        url_inner.pack(fill=tk.X)
        
        url_label = tk.Label(url_inner, text="🌐 URL:", font=('Segoe UI', 11, 'bold'),
                            bg=self.colors['bg'], fg=self.colors['accent'])
        url_label.pack(side=tk.LEFT, padx=(0, 15))
        
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(url_inner, textvariable=self.url_var, 
                                  font=('Segoe UI', 11), width=60, style='Dark.TEntry')
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.scan_button = ttk.Button(url_inner, text="🔍  Escanear Pasta", 
                                     command=self.scan_folder, style='Accent.TButton')
        self.scan_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Frame principal com árvore - Design aprimorado
        tree_frame = ttk.LabelFrame(main_container, text="  📁  Arquivos Encontrados  ", 
                                   style='Dark.TLabelframe', padding=15)
        tree_frame.pack(fill=tk.BOTH, expand=False, pady=(0, 15))
        
        # Configurar árvore com colunas
        columns = ("select", "size", "status")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="tree headings", 
                                height=10, style='Treeview')
        
        # Configurar colunas
        self.tree.heading("#0", text="Nome", anchor=tk.W)
        self.tree.heading("select", text="✓", anchor=tk.CENTER)
        self.tree.heading("size", text="📊 Tamanho", anchor=tk.W)
        self.tree.heading("status", text="📋 Status", anchor=tk.W)
        
        self.tree.column("#0", width=400, minwidth=200)
        self.tree.column("select", width=50, minwidth=50, anchor=tk.CENTER)
        self.tree.column("size", width=120, minwidth=100, anchor=tk.W)
        self.tree.column("status", width=150, minwidth=100, anchor=tk.W)
        
        # Scrollbars
        tree_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, 
                                      command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind para clique duplo
        self.tree.bind("<Double-1>", self.toggle_selection)
        
        # Controles Frame
        controls_frame = ttk.Frame(main_container, style='Dark.TFrame')
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Botões de seleção
        selection_frame = ttk.Frame(controls_frame, style='Dark.TFrame')
        selection_frame.pack(side=tk.LEFT)
        
        ttk.Button(selection_frame, text="✅  Selecionar Todos", 
                  command=self.select_all, style='Success.TButton').pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(selection_frame, text="❌  Desmarcar Todos", 
                  command=self.deselect_all, style='Dark.TButton').pack(side=tk.LEFT, padx=(0, 8))
        
        # Botões de expansão
        expand_frame = ttk.Frame(controls_frame, style='Dark.TFrame')
        expand_frame.pack(side=tk.LEFT, padx=(20, 0))
        
        ttk.Button(expand_frame, text="📂  Expandir Tudo", 
                  command=self.expand_all, style='Dark.TButton').pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(expand_frame, text="📁  Colapsar Tudo", 
                  command=self.collapse_all, style='Dark.TButton').pack(side=tk.LEFT)
        
        # Download Frame
        download_frame = ttk.Frame(controls_frame, style='Dark.TFrame')
        download_frame.pack(side=tk.RIGHT)
        
        # Pasta de destino
        folder_label = tk.Label(download_frame, text="💾  Pasta:", 
                               font=('Segoe UI', 10, 'bold'), bg=self.colors['bg'], fg=self.colors['fg'])
        folder_label.pack(side=tk.LEFT, padx=(0, 8))
        
        self.folder_var = tk.StringVar(value=self.download_folder)
        folder_entry = ttk.Entry(download_frame, textvariable=self.folder_var, 
                                width=25, style='Dark.TEntry')
        folder_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(download_frame, text="📂", width=3, command=self.choose_folder,
                  style='Dark.TButton').pack(side=tk.LEFT, padx=(0, 15))
        
        self.download_button = ttk.Button(download_frame, text="⬇️  Baixar Selecionados", 
                                       command=self.start_download, state="disabled",
                                       style='Accent.TButton')
        self.download_button.pack(side=tk.LEFT, padx=(10, 0))
        
        # Progress Frame
        progress_frame = ttk.Frame(main_container, style='Dark.TFrame')
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Barra de progresso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                          maximum=100, style='Dark.Horizontal.TProgressbar')
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        # Status
        self.status_var = tk.StringVar(value="🚀 Pronto para começar")
        status_label = tk.Label(progress_frame, textvariable=self.status_var,
                               font=('Segoe UI', 10), bg=self.colors['bg'], 
                               fg=self.colors['fg_secondary'])
        status_label.pack()
        
        # Footer
        footer_frame = ttk.Frame(main_container, style='Dark.TFrame')
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        
        footer_left = ttk.Frame(footer_frame, style='Dark.TFrame')
        footer_left.pack(side=tk.LEFT)
        
        footer_label = tk.Label(footer_left, text="💜 Criado por ",
                              font=('Segoe UI', 11), bg=self.colors['bg'],
                              fg=self.colors['fg_tertiary'])
        footer_label.pack(side=tk.LEFT)
        
        riique_link = tk.Label(footer_left, text="@riiquestudies",
                               font=('Segoe UI', 11, 'bold underline'),
                               bg=self.colors['bg'], fg=self.colors['purple'],
                               cursor='hand2')
        riique_link.pack(side=tk.LEFT)
        riique_link.bind("<Button-1>", lambda e: self.open_link("https://x.com/riiquestudies"))
        
        # Efeito hover no link
        def on_enter(e):
            riique_link.config(fg=self.colors['pink'])
        
        def on_leave(e):
            riique_link.config(fg=self.colors['purple'])
        
        riique_link.bind("<Enter>", on_enter)
        riique_link.bind("<Leave>", on_leave)
        
        # Informação adicional no footer
        footer_right = tk.Label(footer_frame, 
                               text="🚀 Powered by Haumea Technology",
                               font=('Segoe UI', 10, 'italic'),
                               bg=self.colors['bg'],
                               fg=self.colors['fg_tertiary'])
        footer_right.pack(side=tk.RIGHT)
    
    def format_file_size(self, size_str):
        """Formata o tamanho do arquivo de forma legível"""
        if size_str == 'Pasta' or size_str == 'Desconhecido':
            return size_str
        
        try:
            # Converter para bytes se for string numérica
            size_bytes = int(size_str)
            
            # Definir unidades
            units = ['B', 'KB', 'MB', 'GB', 'TB']
            unit_index = 0
            
            while size_bytes >= 1024 and unit_index < len(units) - 1:
                size_bytes /= 1024.0
                unit_index += 1
            
            # Formatar com 2 casas decimais se necessário
            if unit_index == 0:
                return f"{int(size_bytes)} {units[unit_index]}"
            else:
                return f"{size_bytes:.1f} {units[unit_index]}"
                
        except (ValueError, TypeError):
            return str(size_str)
    
    def open_link(self, url):
        webbrowser.open_new(url)
    
    def scan_folder(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("❌ Erro", "Por favor, insira uma URL válida")
            return
        
        # Extrair ID da pasta
        try:
            if "/pasta/" in url:
                pasta_id = url.split("/pasta/")[-1].split("/")[0]
            else:
                messagebox.showerror("❌ Erro", "URL inválida. Use o formato: https://drivedepobre.com/pasta/ID")
                return
        except:
            messagebox.showerror("❌ Erro", "Não foi possível extrair o ID da pasta")
            return
        
        # Executar scan em thread separada
        self.scan_button.config(state="disabled")
        self.download_button.config(state="disabled")
        self.status_var.set("🔍 Escaneando pasta...")
        self.progress_var.set(0)
        
        thread = threading.Thread(target=self._scan_folder_thread, args=(pasta_id,))
        thread.daemon = True
        thread.start()
    
    def _scan_folder_thread(self, pasta_id):
        try:
            self.files_data = []
            self.folder_structure = {}
            self.tree_items = {}
            
            # Escanear pasta recursivamente com limite de profundidade
            self._scan_folder_recursive(pasta_id, "", max_depth=3)
            
            # Atualizar interface na thread principal
            self.root.after(0, self._build_tree_structure)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("❌ Erro", f"Erro ao escanear pasta: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.scan_button.config(state="normal"))
            self.root.after(0, lambda: self.progress_var.set(0))
    
    def _scan_folder_recursive(self, pasta_id, path_prefix, max_depth=5):
        """Escaneia uma pasta recursivamente com limite de profundidade"""
        if max_depth <= 0:
            print(f"Limite de profundidade atingido para pasta: {path_prefix}")
            return
            
        offset = 0
        limit = 50
        items_found = 0
        
        while True:
            url = f"https://api.drivedepobre.com/listFolder?id={pasta_id}&offset={offset}&limit={limit}"
            
            try:
                response = self.session.get(url, timeout=10)
                
                if response.status_code != 200:
                    print(f"Erro HTTP {response.status_code} para pasta {pasta_id}")
                    break
                
                items = response.json()
                if not items or len(items) == 0:
                    break
                
                items_found += len(items)
                current_path = path_prefix or 'raiz'
                print(f"Processando {len(items)} itens em {current_path}")
                
                # Atualizar status na interface
                self.root.after(0, lambda: self.status_var.set(f"🔍 Escaneando: {current_path} ({len(self.files_data)} itens encontrados)"))
                
                for item in items:
                    item_id = item.get('id')
                    item_name = item.get('name', 'Sem nome')
                    item_size = item.get('size', 'Desconhecido')
                    
                    if not item_id:
                        continue
                    
                    full_path = f"{path_prefix}/{item_name}" if path_prefix else item_name
                    
                    # Usar heurística mais simples para detectar pastas
                    is_likely_folder = (
                        '.' not in item_name or 
                        item_size == 'Desconhecido' or 
                        item_size == '' or
                        item_size is None
                    )
                    
                    if is_likely_folder:
                        # Verificar se realmente é pasta fazendo uma requisição rápida
                        is_folder = self._quick_folder_check(item_id)
                        
                        if is_folder:
                            # É uma pasta
                            folder_data = {
                                'id': item_id,
                                'name': f"📁 {full_path}",
                                'size': 'Pasta',
                                'url': f"https://drivedepobre.com/pasta/{item_id}",
                                'type': 'folder',
                                'path': full_path,
                                'selected': False,
                                'status': 'Pronto'
                            }
                            self.files_data.append(folder_data)
                            
                            # Escanear conteúdo da pasta recursivamente com profundidade reduzida
                            try:
                                self._scan_folder_recursive(item_id, full_path, max_depth - 1)
                            except Exception as e:
                                print(f"Erro ao escanear subpasta {item_name}: {e}")
                        else:
                            # É um arquivo mesmo sem extensão
                            file_data = {
                                'id': item_id,
                                'name': f"📄 {full_path}",
                                'size': item_size,
                                'url': f"https://drivedepobre.com/arquivo/{item_id}",
                                'type': 'file',
                                'path': full_path,
                                'selected': False,
                                'status': 'Pronto'
                            }
                            self.files_data.append(file_data)
                    else:
                        # Claramente é um arquivo (tem extensão)
                        file_data = {
                            'id': item_id,
                            'name': f"📄 {full_path}",
                            'size': item_size,
                            'url': f"https://drivedepobre.com/arquivo/{item_id}",
                            'type': 'file',
                            'path': full_path,
                            'selected': False,
                            'status': 'Pronto'
                        }
                        self.files_data.append(file_data)
                
                offset += limit
                
                # Limite de segurança para evitar loop infinito
                if items_found > 1000:
                    print(f"Limite de 1000 itens atingido para pasta {path_prefix}")
                    break
                    
                time.sleep(0.3)  # Pausa maior entre requisições
                
            except Exception as e:
                print(f"Erro ao processar pasta {pasta_id}: {e}")
                break
    
    def _quick_folder_check(self, item_id):
        """Verificação rápida se um item é uma pasta"""
        try:
            url = f"https://api.drivedepobre.com/listFolder?id={item_id}&offset=0&limit=1"
            response = self.session.get(url, timeout=5)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    return isinstance(data, list)
                except:
                    return False
            else:
                return False
        except:
            return False
    
    def _build_tree_structure(self):
        """Constrói a estrutura hierárquica da árvore"""
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.tree_items = {}
        
        # Organizar dados por estrutura de pastas
        root_items = []
        folder_contents = {}
        
        for file_data in self.files_data:
            path_parts = file_data['path'].split('/')
            
            if len(path_parts) == 1:
                # Item na raiz
                root_items.append(file_data)
            else:
                # Item dentro de pasta
                parent_path = '/'.join(path_parts[:-1])
                if parent_path not in folder_contents:
                    folder_contents[parent_path] = []
                folder_contents[parent_path].append(file_data)
        
        # Construir árvore recursivamente
        self._build_tree_recursive("", root_items, folder_contents)
        
        self.download_button.config(state="normal" if self.files_data else "disabled")
        
        # Contar arquivos e pastas
        files_count = len([f for f in self.files_data if f['type'] == 'file'])
        folders_count = len([f for f in self.files_data if f['type'] == 'folder'])
        
        status_text = f"📊 {files_count} arquivos"
        if folders_count > 0:
            status_text += f" e {folders_count} pastas"
        status_text += " encontrados"
        
        self.status_var.set(status_text)
    
    def _build_tree_recursive(self, parent_id, items, folder_contents):
        """Constrói a árvore recursivamente"""
        for file_data in items:
            select_text = "☑" if file_data['selected'] else "☐"
            
            # Preparar nome para exibição com ícone
            if file_data['type'] == 'folder':
                display_name = file_data['name'].replace('📁 ', '')
            else:
                display_name = file_data['name'].replace('📄 ', '')
            
            # Formatar tamanho
            formatted_size = self.format_file_size(file_data['size'])
            
            # Inserir item na árvore
            item_id = self.tree.insert(
                parent_id, 
                "end",
                text=display_name,
                values=(select_text, formatted_size, file_data['status']),
                open=False  # Pastas começam fechadas
            )
            
            # Mapear ID do arquivo para item da árvore
            self.tree_items[file_data['id']] = {
                'tree_item': item_id,
                'data': file_data
            }
            
            # Se é uma pasta, adicionar seus filhos
            if file_data['type'] == 'folder' and file_data['path'] in folder_contents:
                children = folder_contents[file_data['path']]
                self._build_tree_recursive(item_id, children, folder_contents)
    
    def toggle_selection(self, event):
        if not self.tree.selection():
            return
            
        tree_item = self.tree.selection()[0]
        
        # Encontrar dados do arquivo pelo item da árvore
        file_data = None
        for item_info in self.tree_items.values():
            if item_info['tree_item'] == tree_item:
                file_data = item_info['data']
                break
        
        if not file_data:
            return
        
        # Alternar seleção
        file_data['selected'] = not file_data['selected']
        selected = file_data['selected']
        
        # Se é uma pasta, selecionar/desselecionar todos os arquivos dentro dela
        if file_data['type'] == 'folder':
            folder_path = file_data['path']
            self._select_folder_contents(folder_path, selected)
        
        # Atualizar display de todos os itens afetados
        self._update_tree_selection_display()
    
    def _select_folder_contents(self, folder_path, selected):
        """Seleciona/deseleciona todos os arquivos dentro de uma pasta"""
        for file_data in self.files_data:
            if file_data['path'].startswith(folder_path + "/") or file_data['path'] == folder_path:
                file_data['selected'] = selected
    
    def _update_tree_selection_display(self):
        """Atualiza o display de seleção de todos os itens na árvore"""
        for file_data in self.files_data:
            if file_data['id'] in self.tree_items:
                tree_item = self.tree_items[file_data['id']]['tree_item']
                select_text = "☑" if file_data['selected'] else "☐"
                
                # Atualizar valores do item
                current_values = list(self.tree.item(tree_item, "values"))
                current_values[0] = select_text
                self.tree.item(tree_item, values=current_values)
    
    def select_all(self):
        for file_data in self.files_data:
            file_data['selected'] = True
        self._update_tree_selection_display()
    
    def deselect_all(self):
        for file_data in self.files_data:
            file_data['selected'] = False
        self._update_tree_selection_display()
    
    def expand_all(self):
        """Expande todas as pastas na árvore"""
        def expand_item(item):
            self.tree.item(item, open=True)
            for child in self.tree.get_children(item):
                expand_item(child)
        
        for item in self.tree.get_children():
            expand_item(item)
    
    def collapse_all(self):
        """Colapsa todas as pastas na árvore"""
        def collapse_item(item):
            self.tree.item(item, open=False)
            for child in self.tree.get_children(item):
                collapse_item(child)
        
        for item in self.tree.get_children():
            collapse_item(item)
    
    def choose_folder(self):
        folder = filedialog.askdirectory(initialdir=self.download_folder)
        if folder:
            self.folder_var.set(folder)
            self.download_folder = folder
    
    def start_download(self):
        selected_files = [f for f in self.files_data if f['selected']]
        if not selected_files:
            messagebox.showwarning("⚠️ Aviso", "Nenhum arquivo selecionado")
            return
        
        self.download_folder = self.folder_var.get()
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
        
        # Iniciar download em thread separada
        self.download_button.config(state="disabled")
        thread = threading.Thread(target=self._download_thread, args=(selected_files,))
        thread.daemon = True
        thread.start()
    
    def _download_thread(self, selected_files):
        # Filtrar apenas arquivos (não pastas) para download
        files_to_download = [f for f in selected_files if f['type'] == 'file']
        total_files = len(files_to_download)
        successful = 0
        failed = 0
        
        for i, file_data in enumerate(files_to_download):
            try:
                # Atualizar status
                self.root.after(0, lambda f=file_data: self._update_file_status(f, "⬇️ Baixando..."))
                self.root.after(0, lambda: self.status_var.set(f"⬇️ Baixando {i+1}/{total_files}: {file_data['name']}"))
                self.root.after(0, lambda: self.progress_var.set((i / total_files) * 100))
                
                # Baixar arquivo
                if self._download_file(file_data):
                    successful += 1
                    self.root.after(0, lambda f=file_data: self._update_file_status(f, "✅ Concluído"))
                else:
                    failed += 1
                    self.root.after(0, lambda f=file_data: self._update_file_status(f, "❌ Erro"))
                
                time.sleep(0.5)  # Pausa entre downloads
                
            except Exception as e:
                failed += 1
                self.root.after(0, lambda f=file_data: self._update_file_status(f, f"❌ Erro: {str(e)[:20]}"))
        
        # Finalizar
        self.root.after(0, lambda: self.progress_var.set(100))
        self.root.after(0, lambda: self.status_var.set(f"🎉 Concluído! {successful} sucessos, {failed} falhas"))
        self.root.after(0, lambda: self.download_button.config(state="normal"))
    
    def _update_file_status(self, file_data, status):
        """Atualiza o status de um arquivo na árvore"""
        try:
            # Encontrar o arquivo nos dados
            for item in self.files_data:
                if item['id'] == file_data['id']:
                    item['status'] = status
                    break
            
            # Atualizar na árvore se existir
            if file_data['id'] in self.tree_items:
                tree_item = self.tree_items[file_data['id']]['tree_item']
                current_values = list(self.tree.item(tree_item, "values"))
                current_values[2] = status  # Status é a 3ª coluna (índice 2)
                self.tree.item(tree_item, values=current_values)
                
        except Exception as e:
            print(f"Erro ao atualizar status: {e}")
    
    def _download_file(self, file_data):
        try:
            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"Iniciando download: {file_data['name']}")
            self.logger.info(f"ID: {file_data['id']}")
            self.logger.info(f"URL: {file_data['url']}")
            self.logger.info(f"Tipo: {file_data['type']}")
            
            # Pular se for pasta
            if file_data['type'] == 'folder':
                self.logger.info("Item é pasta, pulando...")
                return True
            
            # Obter URL real de download
            self.logger.info("Obtendo URL real de download...")
            download_url = self._get_download_url(file_data['url'])
            
            if not download_url:
                self.logger.error("ERRO: Não foi possível obter URL de download")
                self.logger.error(f"URL tentada: {file_data['url']}")
                return False
            
            self.logger.info(f"URL de download obtida: {download_url[:100]}...")
            
            # Baixar arquivo
            self.logger.info("Iniciando requisição de download...")
            response = self.session.get(download_url, stream=True, timeout=30)
            response.raise_for_status()
            self.logger.info(f"Status Code: {response.status_code}")
            self.logger.info(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
            
            # Preparar caminho do arquivo mantendo estrutura de pastas
            file_path = file_data['path']
            # Remover emoji do nome
            clean_path = file_path.replace('📄 ', '').replace('📁 ', '')
            
            # Sanitizar nome do arquivo
            clean_path = re.sub(r'[<>:"/\\|?*]', '_', clean_path)
            
            # Criar caminho completo
            full_path = os.path.join(self.download_folder, clean_path)
            self.logger.info(f"Caminho de destino: {full_path}")
            
            # Criar diretórios se necessário
            dir_path = os.path.dirname(full_path)
            if dir_path and not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
                self.logger.info(f"Diretório criado: {dir_path}")
            
            # Evitar sobrescrever arquivos
            counter = 1
            original_full_path = full_path
            while os.path.exists(full_path):
                name, ext = os.path.splitext(original_full_path)
                full_path = f"{name}_{counter}{ext}"
                counter += 1
            
            if counter > 1:
                self.logger.info(f"Arquivo já existe, usando: {full_path}")
            
            # Salvar arquivo
            self.logger.info("Salvando arquivo...")
            bytes_written = 0
            with open(full_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        bytes_written += len(chunk)
            
            self.logger.info(f"✅ Download concluído com sucesso!")
            self.logger.info(f"Bytes salvos: {bytes_written}")
            self.logger.info(f"{'='*60}\n")
            return True
            
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"❌ ERRO HTTP ao baixar {file_data['name']}: {e}")
            self.logger.error(f"Status Code: {e.response.status_code if hasattr(e, 'response') else 'N/A'}")
            self.logger.error(f"Response: {e.response.text[:500] if hasattr(e, 'response') else 'N/A'}")
            return False
        except requests.exceptions.RequestException as e:
            self.logger.error(f"❌ ERRO de requisição ao baixar {file_data['name']}: {e}")
            return False
        except Exception as e:
            self.logger.error(f"❌ ERRO GERAL ao baixar {file_data['name']}: {e}")
            self.logger.exception("Stack trace completo:")
            return False
    
    def _get_download_url(self, file_url):
        try:
            self.logger.info(f"\n--- Obtendo URL de download ---")
            self.logger.info(f"URL da página: {file_url}")
            
            response = self.session.get(file_url, timeout=15)
            response.raise_for_status()
            
            self.logger.info(f"Status da página: {response.status_code}")
            self.logger.info(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
            
            # Salvar HTML para debug
            html_content = response.content.decode('utf-8', errors='ignore')
            self.logger.debug(f"Tamanho do HTML: {len(html_content)} caracteres")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            scripts = soup.find_all('script')
            
            self.logger.info(f"Número de scripts encontrados: {len(scripts)}")
            
            # Tentar diferentes padrões
            patterns_to_try = [
                (r'downloadUrl\s*=\s*`([^`]+)`', 'downloadUrl com crase', 1),
                (r'downloadUrl\s*=\s*"([^"]+)"', 'downloadUrl com aspas duplas', 1),
                (r'downloadUrl\s*=\s*\'([^\']+)\'', 'downloadUrl com aspas simples', 1),
                (r'download[Uu]rl["\']\s*:\s*["\']([^"\',]+)', 'downloadUrl como propriedade JSON', 1),
                (r'const\s+\w+\s*=\s*["\']([^"\']+s3[^"\']+)["\']', 'const com URL S3', 1),
                (r'let\s+\w+\s*=\s*["\']([^"\']+s3[^"\']+)["\']', 'let com URL S3', 1),
                (r'var\s+\w+\s*=\s*["\']([^"\']+s3[^"\']+)["\']', 'var com URL S3', 1),
                (r'href\s*=\s*["\']([^"\']+s3[^"\']+)["\']', 'href com S3', 1),
                (r'url:\s*["\']([^"\']+s3[^"\']+)["\']', 'url JSON com S3', 1),
                (r'data-url\s*=\s*["\']([^"\']+)["\']', 'data-url attribute', 1),
                (r'data-download\s*=\s*["\']([^"\']+)["\']', 'data-download attribute', 1),
                (r'(https?://[^\s"\'>]+\.s3[^\s"\'>]*amazonaws[^\s"\'>]+)', 'URL S3 AWS completa', 1),
                (r'(https?://[^\s"\'>]+/download/[^\s"\'>]+)', 'URL de download direta', 1),
            ]
            
            for idx, script in enumerate(scripts):
                if script.string:
                    script_content = script.string
                    self.logger.debug(f"\nScript #{idx+1} (primeiros 300 chars):")
                    self.logger.debug(script_content[:300])
                    
                    # Primeiro tentar padrões específicos
                    for pattern, pattern_name, group_index in patterns_to_try:
                        match = re.search(pattern, script_content)
                        if match:
                            url = match.group(group_index)
                            self.logger.info(f"✅ URL encontrada com padrão '{pattern_name}': {url[:100]}...")
                            return url
                    
                    # Se não encontrou, tentar extrair todas as strings que parecem URLs
                    # Buscar por padrões tipo: ="https://..." ou ='https://...' ou =`https://...`
                    all_urls = re.findall(r'[=:]\s*["\']?(https?://[^\s"\'<>]+)["\']?', script_content)
                    if all_urls:
                        self.logger.debug(f"URLs encontradas no script #{idx+1}: {len(all_urls)}")
                        for url in all_urls:
                            # Filtrar apenas URLs que parecem ser de download (S3, cloudfront, etc)
                            if any(keyword in url.lower() for keyword in ['s3', 'cloudfront', 'download', 'amazonaws', 'storage']):
                                self.logger.info(f"✅ URL de download encontrada por busca agressiva: {url[:100]}...")
                                return url
            
            # Se não encontrou nos scripts, tentar em elementos HTML específicos
            self.logger.warning("URL não encontrada em scripts, procurando em elementos HTML...")
            
            # Procurar em botões e links
            download_buttons = soup.find_all(['a', 'button'], id=lambda x: x and 'download' in x.lower())
            self.logger.info(f"Botões de download encontrados: {len(download_buttons)}")
            
            for btn in download_buttons:
                for attr in ['href', 'data-url', 'data-download', 'data-link', 'onclick']:
                    if btn.has_attr(attr):
                        value = btn[attr]
                        self.logger.debug(f"Atributo {attr}: {str(value)[:100]}")
                        
                        # Procurar URLs no atributo
                        for pattern, pattern_name, group_index in patterns_to_try:
                            match = re.search(pattern, str(value))
                            if match:
                                url = match.group(group_index)
                                self.logger.info(f"✅ URL encontrada em elemento HTML ({attr}) com padrão '{pattern_name}': {url[:100]}...")
                                return url
            
            # Se não encontrou nos elementos, tentar no HTML completo
            self.logger.warning("URL não encontrada em elementos, tentando no HTML completo...")
            for pattern, pattern_name, group_index in patterns_to_try:
                match = re.search(pattern, html_content)
                if match:
                    url = match.group(group_index)
                    self.logger.info(f"✅ URL encontrada no HTML com padrão '{pattern_name}': {url[:100]}...")
                    return url
            
            # Tentar obter URL via API do site
            self.logger.warning("Tentando obter URL de download via API...")
            file_id = file_url.split('/')[-1]
            api_endpoints = [
                f"https://api.drivedepobre.com/file/{file_id}",
                f"https://api.drivedepobre.com/getFile?id={file_id}",
                f"https://api.drivedepobre.com/download/{file_id}",
                f"https://drivedepobre.com/api/file/{file_id}",
            ]
            
            for api_url in api_endpoints:
                try:
                    self.logger.debug(f"Tentando API: {api_url}")
                    api_response = self.session.get(api_url, timeout=10)
                    if api_response.status_code == 200:
                        try:
                            api_data = api_response.json()
                            self.logger.debug(f"Resposta da API: {str(api_data)[:200]}")
                            
                            # Procurar por campos que possam conter a URL
                            possible_keys = ['downloadUrl', 'download_url', 'url', 'file_url', 'link', 'download_link', 's3_url']
                            for key in possible_keys:
                                if key in api_data and api_data[key]:
                                    url = api_data[key]
                                    self.logger.info(f"✅ URL encontrada via API ({key}): {url[:100]}...")
                                    return url
                        except:
                            pass
                except:
                    pass
            
            # Salvar HTML para análise
            debug_file = os.path.join("logs", f"html_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            self.logger.warning(f"HTML salvo para análise em: {debug_file}")
            
            self.logger.error("❌ Nenhum padrão de URL de download encontrado!")
            return None
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"❌ Erro de requisição ao obter URL: {e}")
            return None
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter URL de download: {e}")
            self.logger.exception("Stack trace:")
            return None

def main():
    root = tk.Tk()
    app = DriveDePobreGUI(root)
    
    # Centralizar janela
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()
