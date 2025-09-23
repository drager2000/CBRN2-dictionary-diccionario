import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import itertools
import re
from threading import Thread
import time
import random

class PersonalDictionaryGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title(" CBRN ")
        self.root.geometry("1280x700")
        self.root.configure(bg="#0b442b")
        
        # Variables
        self.nombres = tk.StringVar(value="")
        self.apellidos = tk.StringVar(value="")
        self.anios = tk.StringVar(value="")
        self.correos = tk.StringVar(value="")
        self.opcionales = tk.StringVar(value="")
        self.min_anio = tk.IntVar(value=1990)
        self.max_anio = tk.IntVar(value=2024)
        self.dominios = tk.StringVar(value="gmail.com,yahoo.com,hotmail.com,outlook.com")
        self.include_variantes = tk.BooleanVar(value=True)
        self.include_numeros = tk.BooleanVar(value=True)
        self.include_especiales = tk.BooleanVar(value=False)
        self.filename = tk.StringVar(value=" CBRN ")
        self.dictionary_size = tk.StringVar(value="0")
        self.passwords_created = tk.StringVar(value="0")
        self.generation_time = tk.StringVar(value="0.0s")
        self.max_passwords = tk.IntVar(value=0)  # 0 = ilimitado
        self.limit_passwords = tk.BooleanVar(value=False)
        
        # Variables para el progreso
        self.is_generating = False
        self.total_passwords = 0
        
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill='both', expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, 
                               text=" CBRN ",
                               font=('Arial', 19, 'bold'),
                               foreground="#05531A")
        title_label.pack(pady=(0, 20))
        
        # Notebook para pestañas
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)
        
        # Pestañas
        tab_datos = ttk.Frame(notebook, padding="10")
        tab_opciones = ttk.Frame(notebook, padding="10")
        tab_limites = ttk.Frame(notebook, padding="10")
        tab_vista = ttk.Frame(notebook, padding="10")
        
        notebook.add(tab_datos, text="Datos Personales")
        notebook.add(tab_opciones, text="Opciones")
        notebook.add(tab_limites, text="Límites")
        notebook.add(tab_vista, text="Vista Previa")
        
        # Configurar pestañas
        self.setup_datos_tab(tab_datos)
        self.setup_opciones_tab(tab_opciones)
        self.setup_limites_tab(tab_limites)
        self.setup_vista_tab(tab_vista)
        
        # Barra de estado y botones
        self.setup_actions(main_frame)
    
    def setup_datos_tab(self, tab):
        # Frame para datos personales
        datos_frame = ttk.LabelFrame(tab, text="Información Personal", padding="10")
        datos_frame.pack(fill='both', expand=True, pady=5)
        
        # Nombres
        ttk.Label(datos_frame, text="Nombres (separados por coma):", 
                 font=('Arial', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        nombres_entry = ttk.Entry(datos_frame, textvariable=self.nombres, width=50)
        nombres_entry.pack(fill='x', pady=(0, 10))
        ttk.Label(datos_frame, text="Ej: juan,maria,carlos,ana", 
                 foreground='gray', font=('Arial', 8)).pack(anchor='w')
        
        # Apellidos
        ttk.Label(datos_frame, text="Apellidos (separados por coma):", 
                 font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10, 5))
        apellidos_entry = ttk.Entry(datos_frame, textvariable=self.apellidos, width=50)
        apellidos_entry.pack(fill='x', pady=(0, 10))
        ttk.Label(datos_frame, text="Ej: perez,gomez,rodriguez,lopez", 
                 foreground='gray', font=('Arial', 8)).pack(anchor='w')
        
        # Años personalizados
        ttk.Label(datos_frame, text="Años específicos (separados por coma):", 
                 font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10, 5))
        anios_entry = ttk.Entry(datos_frame, textvariable=self.anios, width=50)
        anios_entry.pack(fill='x', pady=(0, 10))
        ttk.Label(datos_frame, text="Ej: 1990,1995,2000,2005 (o deja vacío para usar rango)", 
                 foreground='gray', font=('Arial', 8)).pack(anchor='w')
        
        # Correos
        ttk.Label(datos_frame, text="Correos/usuarios (separados por coma):", 
                 font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10, 5))
        correos_entry = ttk.Entry(datos_frame, textvariable=self.correos, width=50)
        correos_entry.pack(fill='x', pady=(0, 10))
        ttk.Label(datos_frame, text="Ej: juan.perez,maria.gomez,carlos.rodriguez", 
                 foreground='gray', font=('Arial', 8)).pack(anchor='w')
        
        # Opcionales
        ttk.Label(datos_frame, text="Palabras opcionales (separadas por coma):", 
                 font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10, 5))
        opcionales_entry = ttk.Entry(datos_frame, textvariable=self.opcionales, width=50)
        opcionales_entry.pack(fill='x', pady=(0, 10))
        ttk.Label(datos_frame, text="Ej: password,123,admin,user,welcome", 
                 foreground='gray', font=('Arial', 8)).pack(anchor='w')
    
    def setup_opciones_tab(self, tab):
        # Frame principal
        opciones_frame = ttk.LabelFrame(tab, text="Opciones de Generación", padding="10")
        opciones_frame.pack(fill='both', expand=True, pady=5)
        
        # Rango de años
        ttk.Label(opciones_frame, text="Rango de años (si no se especifican años):", 
                 font=('Arial', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        
        anio_frame = ttk.Frame(opciones_frame)
        anio_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Label(anio_frame, text="Desde:").pack(side='left')
        ttk.Entry(anio_frame, textvariable=self.min_anio, width=8).pack(side='left', padx=(5, 20))
        ttk.Label(anio_frame, text="Hasta:").pack(side='left')
        ttk.Entry(anio_frame, textvariable=self.max_anio, width=8).pack(side='left', padx=(5, 0))
        
        # Dominios de correo
        ttk.Label(opciones_frame, text="Dominios de correo (separados por coma):", 
                 font=('Arial', 10, 'bold')).pack(anchor='w', pady=(5, 5))
        dominios_entry = ttk.Entry(opciones_frame, textvariable=self.dominios, width=50)
        dominios_entry.pack(fill='x', pady=(0, 15))
        ttk.Label(opciones_frame, text="Ej: gmail.com,yahoo.com,hotmail.com", 
                 foreground='gray', font=('Arial', 8)).pack(anchor='w')
        
        # Opciones de variantes
        variants_frame = ttk.LabelFrame(opciones_frame, text="Variantes a incluir", padding="10")
        variants_frame.pack(fill='x', pady=(10, 5))
        
        ttk.Checkbutton(variants_frame, text="Incluir variantes (minúsculas, MAYÚSCULAS, Capitalizado)", 
                       variable=self.include_variantes).pack(anchor='w')
        ttk.Checkbutton(variants_frame, text="Incluir combinaciones con números (123, 1234, etc.)", 
                       variable=self.include_numeros).pack(anchor='w')
        ttk.Checkbutton(variants_frame, text="Incluir caracteres especiales (!@#$%)", 
                       variable=self.include_especiales).pack(anchor='w')
        
        # Estadísticas en tiempo real
        stats_frame = ttk.LabelFrame(opciones_frame, text="Estadísticas", padding="10")
        stats_frame.pack(fill='x', pady=(15, 5))
        
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill='x')
        
        ttk.Label(stats_grid, text="Contraseñas creadas:", font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky='w', padx=(0, 10))
        ttk.Label(stats_grid, textvariable=self.passwords_created, font=('Arial', 9, 'bold'), foreground='green').grid(row=0, column=1, sticky='w', padx=(0, 20))
        
        ttk.Label(stats_grid, text="Tiempo de generación:", font=('Arial', 9, 'bold')).grid(row=0, column=2, sticky='w', padx=(0, 10))
        ttk.Label(stats_grid, textvariable=self.generation_time, font=('Arial', 9, 'bold'), foreground='blue').grid(row=0, column=3, sticky='w')
        
        # Ejemplos
        ttk.Label(opciones_frame, text="Ejemplos de combinaciones que se generarán:", 
                 font=('Arial', 10, 'bold')).pack(anchor='w', pady=(15, 5))
        
        examples = """
• juan1990 • juan.perez • juan@email.com • juan123 • JuanPerez
• maria.gomez2020 • MARIA • MariaGomez! • admin123 • welcome2024
• Combinaciones numéricas: juan1, juan12, juan123, ..., juan123456789
"""
        example_label = ttk.Label(opciones_frame, text=examples, 
                                foreground='darkgreen', font=('Courier', 9))
        example_label.pack(anchor='w')
    
    def setup_limites_tab(self, tab):
        # Frame para límites
        limites_frame = ttk.LabelFrame(tab, text="Límites de Generación", padding="10")
        limites_frame.pack(fill='both', expand=True, pady=5)
        
        # Checkbox para limitar contraseñas
        limit_frame = ttk.Frame(limites_frame)
        limit_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Checkbutton(limit_frame, text="Limitar número máximo de contraseñas", 
                       variable=self.limit_passwords, 
                       command=self.toggle_password_limit).pack(anchor='w')
        
        # Entrada para máximo de contraseñas
        self.max_entry_frame = ttk.Frame(limites_frame)
        self.max_entry_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Label(self.max_entry_frame, text="Máximo de contraseñas:").pack(side='left')
        max_entry = ttk.Entry(self.max_entry_frame, textvariable=self.max_passwords, width=15)
        max_entry.pack(side='left', padx=(10, 5))
        ttk.Label(self.max_entry_frame, text="(0 = ilimitado)").pack(side='left')
        
        # Opciones de selección cuando se limita
        selection_frame = ttk.LabelFrame(limites_frame, text="Método de Selección", padding="10")
        selection_frame.pack(fill='x', pady=(0, 15))
        
        self.selection_method = tk.StringVar(value="aleatorio")
        
        ttk.Radiobutton(selection_frame, text="Selección aleatoria", 
                       variable=self.selection_method, value="aleatorio").pack(anchor='w')
        ttk.Radiobutton(selection_frame, text="Primeras N contraseñas", 
                       variable=self.selection_method, value="primeras").pack(anchor='w')
        ttk.Radiobutton(selection_frame, text="Últimas N contraseñas", 
                       variable=self.selection_method, value="ultimas").pack(anchor='w')
        
        # Información sobre límites
        info_frame = ttk.LabelFrame(limites_frame, text="Información", padding="10")
        info_frame.pack(fill='x', pady=(0, 5))
        
        info_text = """
• Use límites para diccionarios más manejables
• 'Aleatorio': Mezcla las contraseñas y toma una muestra
• 'Primeras': Toma las primeras N contraseñas ordenadas
• 'Últimas': Toma las últimas N contraseñas ordenadas
• 0 = Sin límite (genera todas las combinaciones posibles)
"""
        ttk.Label(info_frame, text=info_text, foreground='darkblue', 
                 font=('Arial', 8), justify='left').pack(anchor='w')
        
        # Actualizar estado inicial
        self.toggle_password_limit()
    
    def toggle_password_limit(self):
        """Habilita o deshabilita los controles de límite"""
        state = 'normal' if self.limit_passwords.get() else 'disabled'
        
        for widget in self.max_entry_frame.winfo_children():
            if isinstance(widget, ttk.Entry):
                widget.config(state=state)
    
    def setup_vista_tab(self, tab):
        # Frame para vista previa
        vista_frame = ttk.LabelFrame(tab, text="Vista Previa del Diccionario", padding="10")
        vista_frame.pack(fill='both', expand=True, pady=5)
        
        self.preview_text = scrolledtext.ScrolledText(vista_frame, height=20, 
                                                    font=('Courier', 9), wrap=tk.WORD)
        self.preview_text.pack(fill='both', expand=True)
        
        # Contador en vista previa
        preview_stats = ttk.Frame(vista_frame)
        preview_stats.pack(fill='x', pady=(5, 0))
        
        ttk.Label(preview_stats, text="Mostrando:", font=('Arial', 8)).pack(side='left')
        self.preview_count = ttk.Label(preview_stats, text="0 contraseñas", font=('Arial', 8, 'bold'), foreground='purple')
        self.preview_count.pack(side='left', padx=(5, 20))
        
        ttk.Label(vista_frame, 
                 text="Nota: La vista previa muestra solo una muestra representativa del diccionario completo.",
                 foreground='gray', font=('Arial', 8)).pack(anchor='w', pady=(5, 0))
    
    def setup_actions(self, parent):
        # Frame para acciones
        action_frame = ttk.Frame(parent)
        action_frame.pack(fill='x', pady=(15, 5))
        
        # Información de tamaño
        info_frame = ttk.Frame(action_frame)
        info_frame.pack(side='left', fill='x', expand=True)
        
        ttk.Label(info_frame, text="Tamaño estimado:", 
                 font=('Arial', 10, 'bold')).pack(side='left')
        ttk.Label(info_frame, textvariable=self.dictionary_size, 
                 font=('Arial', 10, 'bold'), foreground='blue').pack(side='left', padx=(5, 20))
        
        ttk.Label(info_frame, text="Nombre archivo:").pack(side='left')
        ttk.Entry(info_frame, textvariable=self.filename, width=20).pack(side='left', padx=(5, 5))
        ttk.Label(info_frame, text=".txt").pack(side='left')
        
        # Botones
        button_frame = ttk.Frame(action_frame)
        button_frame.pack(side='right')
        
        ttk.Button(button_frame, text="Generar Vista Previa", 
                  command=self.generate_preview).pack(side='left', padx=(0, 10))
        ttk.Button(button_frame, text="Guardar Diccionario", 
                  command=self.start_save_dictionary).pack(side='left', padx=(0, 10))
        ttk.Button(button_frame, text="Limpiar Todo", 
                  command=self.clear_all).pack(side='left')
    
    def parse_input(self, input_text):
        """Convierte texto de entrada en lista limpia"""
        if not input_text.strip():
            return []
        return [item.strip() for item in input_text.split(',') if item.strip()]
    
    def generate_variants(self, word):
        """Genera variantes de una palabra"""
        variants = set()
        
        # Versión original
        variants.add(word)
        
        if self.include_variantes.get():
            # Minúsculas
            variants.add(word.lower())
            # Mayúsculas
            variants.add(word.upper())
            # Capitalizado
            variants.add(word.capitalize())
        
        if self.include_numeros.get():
            # Con números comunes y combinaciones hasta 9
            number_combinations = ['', '1', '12', '123', '1234', '12345', '123456', '1234567', '12345678', '123456789',
                                  '00', '000', '0000', '00000', '000000', '0000000', '00000000', '000000000',
                                  '01', '02', '03', '04', '05', '06', '07', '08', '09',
                                  '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
                                  '20', '21', '22', '23', '24', '25', '26', '27', '28', '29',
                                  '69', '99', '100', '200', '300', '400', '500', '600', '700', '800', '900']
            
            for num in number_combinations:
                variants.add(f"{word}{num}")
                if self.include_variantes.get():
                    variants.add(f"{word.lower()}{num}")
                    variants.add(f"{word.upper()}{num}")
                    variants.add(f"{word.capitalize()}{num}")
        
        if self.include_especiales.get():
            # Con caracteres especiales
            for special in ['', '!', '@', '#', '$', '%', '&', '*', '_', '-']:
                variants.add(f"{word}{special}")
                if self.include_variantes.get():
                    variants.add(f"{word.lower()}{special}")
                    variants.add(f"{word.upper()}{special}")
                    variants.add(f"{word.capitalize()}{special}")
        
        return variants
    
    def generate_email_variants(self, username):
        """Genera variantes de correo electrónico"""
        variants = set()
        dominios = self.parse_input(self.dominios.get())
        
        for dominio in dominios:
            variants.add(f"{username}@{dominio}")
            variants.add(f"{username.lower()}@{dominio}")
            variants.add(f"{username.upper()}@{dominio}")
        
        return variants
    
    def update_progress(self, count):
        """Actualiza el contador de contraseñas en tiempo real"""
        self.passwords_created.set(f"{count:,}")
        self.root.update_idletasks()
    
    def generate_preview(self):
        """Genera vista previa del diccionario"""
        try:
            # Obtener datos
            nombres = self.parse_input(self.nombres.get())
            apellidos = self.parse_input(self.apellidos.get())
            anios_especificos = self.parse_input(self.anios.get())
            correos = self.parse_input(self.correos.get())
            opcionales = self.parse_input(self.opcionales.get())
            
            if not any([nombres, apellidos, correos, opcionales]):
                messagebox.showwarning("Advertencia", "Debe ingresar al menos un nombre, apellido, correo o palabra opcional.")
                return
            
            # Generar años
            if anios_especificos:
                anios = anios_especificos
            else:
                anios = [str(year) for year in range(self.min_anio.get(), self.max_anio.get() + 1)]
            
            # Generar combinaciones de muestra
            sample_passwords = set()
            count = 0
            max_samples = 100
            
            # Combinaciones básicas
            for nombre in nombres[:3]:  # Solo primeros 3 para vista previa
                variants = self.generate_variants(nombre)
                sample_passwords.update(list(variants)[:5])
                count += len(variants)
                
                for apellido in apellidos[:2]:
                    # Nombre + Apellido
                    combo = f"{nombre}{apellido}"
                    variants = self.generate_variants(combo)
                    sample_passwords.update(list(variants)[:3])
                    count += len(variants)
                    
                    # Nombre.Apellido
                    combo = f"{nombre}.{apellido}"
                    variants = self.generate_variants(combo)
                    sample_passwords.update(list(variants)[:3])
                    count += len(variants)
            
            # Años
            for anio in anios[:5]:  # Solo primeros 5 años
                for nombre in nombres[:2]:
                    combo = f"{nombre}{anio}"
                    variants = self.generate_variants(combo)
                    sample_passwords.update(list(variants)[:2])
                    count += len(variants)
            
            # Correos
            for correo in correos[:3]:
                email_variants = self.generate_email_variants(correo)
                sample_passwords.update(list(email_variants)[:3])
                count += len(email_variants)
            
            # Opcionales
            for opcional in opcionales[:3]:
                variants = self.generate_variants(opcional)
                sample_passwords.update(list(variants)[:3])
                count += len(variants)
            
            # Aplicar límite si está activado
            if self.limit_passwords.get() and self.max_passwords.get() > 0:
                sample_passwords = self.apply_password_limit(sample_passwords, self.max_passwords.get())
            
            # Actualizar vista previa
            self.preview_text.delete('1.0', tk.END)
            sorted_passwords = sorted(sample_passwords)
            for password in sorted_passwords:
                self.preview_text.insert(tk.END, password + '\n')
            
            # Actualizar contador de vista previa
            self.preview_count.config(text=f"{len(sorted_passwords):,} contraseñas")
            
            # Calcular tamaño estimado
            total_size = self.calculate_total_size()
            self.dictionary_size.set(f"{total_size:,}")
            
            messagebox.showinfo("Vista Previa", 
                               f"Vista previa generada con éxito!\n"
                               f"Mostrando: {len(sorted_passwords):,} contraseñas\n"
                               f"Tamaño estimado del diccionario: {total_size:,} entradas")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar vista previa: {str(e)}")
    
    def apply_password_limit(self, passwords, max_count):
        """Aplica el límite de contraseñas según el método seleccionado"""
        password_list = list(passwords)
        
        if len(password_list) <= max_count:
            return passwords
        
        method = self.selection_method.get()
        
        if method == "aleatorio":
            # Mezclar y tomar una muestra aleatoria
            random.shuffle(password_list)
            return set(password_list[:max_count])
        
        elif method == "primeras":
            # Tomar las primeras N contraseñas ordenadas
            return set(sorted(password_list)[:max_count])
        
        elif method == "ultimas":
            # Tomar las últimas N contraseñas ordenadas
            return set(sorted(password_list)[-max_count:])
        
        return passwords
    
    def calculate_total_size(self):
        """Calcula el tamaño total estimado del diccionario"""
        nombres = self.parse_input(self.nombres.get())
        apellidos = self.parse_input(self.apellidos.get())
        anios_especificos = self.parse_input(self.anios.get())
        correos = self.parse_input(self.correos.get())
        opcionales = self.parse_input(self.opcionales.get())
        dominios = self.parse_input(self.dominios.get())
        
        # Calcular años
        if anios_especificos:
            anios_count = len(anios_especificos)
        else:
            anios_count = self.max_anio.get() - self.min_anio.get() + 1
        
        # Calcular variantes por palabra
        variants_per_word = 1  # Original
        if self.include_variantes.get():
            variants_per_word += 3  # lower, upper, capitalize
        if self.include_numeros.get():
            variants_per_word *= 60  # 60 opciones de números (más combinaciones)
        if self.include_especiales.get():
            variants_per_word *= 6  # 6 opciones de especiales
        
        total = 0
        
        # Nombres individuales
        total += len(nombres) * variants_per_word
        
        # Combinaciones nombre + apellido
        total += len(nombres) * len(apellidos) * variants_per_word * 2  # con y sin punto
        
        # Combinaciones con años
        total += (len(nombres) + len(apellidos)) * anios_count * variants_per_word
        
        # Correos electrónicos
        total += len(correos) * len(dominios) * 3  # 3 variantes por correo
        
        # Palabras opcionales
        total += len(opcionales) * variants_per_word
        
        # Aplicar límite si está activado
        if self.limit_passwords.get() and self.max_passwords.get() > 0:
            total = min(total, self.max_passwords.get())
        
        return total
    
    def start_save_dictionary(self):
        """Inicia el guardado del diccionario en un hilo separado"""
        if self.is_generating:
            return
            
        # Verificar datos
        nombres = self.parse_input(self.nombres.get())
        apellidos = self.parse_input(self.apellidos.get())
        correos = self.parse_input(self.correos.get())
        opcionales = self.parse_input(self.opcionales.get())
        
        if not any([nombres, apellidos, correos, opcionales]):
            messagebox.showwarning("Advertencia", "Debe ingresar al menos un nombre, apellido, correo o palabra opcional.")
            return
        
        # Verificar límite
        if self.limit_passwords.get() and self.max_passwords.get() < 0:
            messagebox.showwarning("Advertencia", "El límite de contraseñas no puede ser negativo.")
            return
        
        # Pedir ubicación para guardar
        filename = self.filename.get().strip()
        if not filename:
            messagebox.showwarning("Advertencia", "Por favor ingrese un nombre de archivo.")
            return
        
        file_path = filedialog.asksaveasfilename(
            initialfile=filename,
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
            title="Guardar diccionario personalizado"
        )
        
        if not file_path:
            return
        
        # Iniciar generación en hilo separado
        self.is_generating = True
        thread = Thread(target=self.save_dictionary_thread, args=(file_path,))
        thread.daemon = True
        thread.start()
    
    def save_dictionary_thread(self, file_path):
        """Hilo para guardar el diccionario con contador en tiempo real"""
        try:
            start_time = time.time()
            
            # Obtener datos
            nombres = self.parse_input(self.nombres.get())
            apellidos = self.parse_input(self.apellidos.get())
            anios_especificos = self.parse_input(self.anios.get())
            correos = self.parse_input(self.correos.get())
            opcionales = self.parse_input(self.opcionales.get())
            
            # Generar años
            if anios_especificos:
                anios = anios_especificos
            else:
                anios = [str(year) for year in range(self.min_anio.get(), self.max_anio.get() + 1)]
            
            # Generar todas las combinaciones
            all_passwords = set()
            password_count = 0
            
            # Función para agregar y contar
            def add_and_count(items):
                nonlocal password_count
                all_passwords.update(items)
                password_count += len(items)
                if password_count % 1000 == 0:  # Actualizar cada 1000 contraseñas
                    self.update_progress(password_count)
            
            # Nombres individuales
            for nombre in nombres:
                variants = self.generate_variants(nombre)
                add_and_count(variants)
            
            # Apellidos individuales
            for apellido in apellidos:
                variants = self.generate_variants(apellido)
                add_and_count(variants)
            
            # Combinaciones nombre + apellido
            for nombre in nombres:
                for apellido in apellidos:
                    # Sin separador
                    combo = f"{nombre}{apellido}"
                    variants = self.generate_variants(combo)
                    add_and_count(variants)
                    
                    # Con punto
                    combo = f"{nombre}.{apellido}"
                    variants = self.generate_variants(combo)
                    add_and_count(variants)
            
            # Combinaciones con años
            for anio in anios:
                for nombre in nombres:
                    combo = f"{nombre}{anio}"
                    variants = self.generate_variants(combo)
                    add_and_count(variants)
                
                for apellido in apellidos:
                    combo = f"{apellido}{anio}"
                    variants = self.generate_variants(combo)
                    add_and_count(variants)
            
            # Correos electrónicos
            for correo in correos:
                email_variants = self.generate_email_variants(correo)
                add_and_count(email_variants)
            
            # Palabras opcionales
            for opcional in opcionales:
                variants = self.generate_variants(opcional)
                add_and_count(variants)
            
            # Aplicar límite si está activado
            if self.limit_passwords.get() and self.max_passwords.get() > 0:
                all_passwords = self.apply_password_limit(all_passwords, self.max_passwords.get())
            
            # Escribir archivo
            with open(file_path, 'w', encoding='utf-8') as f:
                sorted_passwords = sorted(all_passwords)
                for i, password in enumerate(sorted_passwords):
                    f.write(password + '\n')
                    if i % 1000 == 0:  # Actualizar contador durante escritura
                        self.update_progress(i)
            
            end_time = time.time()
            generation_time = end_time - start_time
            
            # Actualizar estadísticas finales
            final_count = len(all_passwords)
            self.passwords_created.set(f"{final_count:,}")
            self.generation_time.set(f"{generation_time:.2f}s")
            self.dictionary_size.set(f"{final_count:,}")
            
            # Mostrar mensaje de éxito
            self.root.after(0, lambda: messagebox.showinfo(
                "Éxito", 
                f"¡Diccionario guardado exitosamente!\n"
                f"Total de contraseñas generadas: {final_count:,}\n"
                f"Tiempo de generación: {generation_time:.2f} segundos\n"
                f"Límite aplicado: {'Sí' if self.limit_passwords.get() and self.max_passwords.get() > 0 else 'No'}\n"
                f"Ubicación: {file_path}"
            ))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error al guardar el diccionario: {str(e)}"))
        finally:
            self.is_generating = False
    
    def clear_all(self):
        """Limpia todos los campos"""
        self.nombres.set("")
        self.apellidos.set("")
        self.anios.set("")
        self.correos.set("")
        self.opcionales.set("")
        self.min_anio.set(1990)
        self.max_anio.set(2024)
        self.dominios.set("gmail.com,yahoo.com,hotmail.com,outlook.com")
        self.include_variantes.set(True)
        self.include_numeros.set(True)
        self.include_especiales.set(False)
        self.filename.set("diccionario_personalizado")
        self.dictionary_size.set("0")
        self.passwords_created.set("0")
        self.generation_time.set("0.0s")
        self.max_passwords.set(0)
        self.limit_passwords.set(False)
        self.selection_method.set("aleatorio")
        self.preview_text.delete('1.0', tk.END)
        self.preview_count.config(text="0 contraseñas")
        self.toggle_password_limit()
        
        messagebox.showinfo("Limpiar", "Todos los campos han sido restablecidos.")

def main():
    root = tk.Tk()
    app = PersonalDictionaryGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()

    