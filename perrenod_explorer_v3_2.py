# ============================================================
# PERRENOD EXPLORER v2.0
# ============================================================
# Based on the work of Giovanni Santostasi and Stephen Perrenod
# 
# Formula: ln(P) = α×ln(t) + c + Σ Aᵢ×t^βᵢ × cos(i×ω×ln(t) + φᵢ)
# With physics constraint: ω = 2π/ln(2) = 9.0647 (LOCKED)
# λ = 2.0 → cycles when Bitcoin age doubles
#
# Authors: Snarky (snarkyaes@proton.me)
# ============================================================
#
# LICENSE
# ============================================================
# Copyright (c) 2025 Snarky (snarkyaes@proton.me)
# Based on the work of Giovanni Santostasi and Stephen Perrenod
#
# Permission is hereby granted, free of charge, to any person 
# obtaining a copy of this software for personal, educational, 
# or research purposes, to use, copy, modify, and distribute, 
# subject to the following conditions:
#
# 1. The above copyright notice and this permission notice shall 
#    be included in all copies or substantial portions of the 
#    Software.
#
# 2. Attribution to the original authors must be maintained.
#
# 3. COMMERCIAL USE IS NOT PERMITTED without prior written 
#    consent from the copyright holder. For commercial licensing 
#    inquiries, contact: snarkyaes@proton.me
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR
# ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import json
import os
import hashlib
from datetime import datetime
import threading
import requests
from scipy.optimize import differential_evolution
import io
from PIL import Image, ImageGrab

# ============================================================
# TRANSLATIONS
# ============================================================

TRANSLATIONS = {
    'en': {
        'title': "Perrenod Explorer - ω = 9.0647 LOCKED",
        'draw': "📊 Draw",
        'calc_r2': "📈 Calc R²",
        'optimize': "🔄 Optimize",
        'copy_text': "📋 Copy Text",
        'copy_graph': "🖼 Copy Graph",
        'settings': "⚙ Settings",
        'credits': "ℹ Credits",
        'harmonics': "Perrenod Harmonics",
        'formula': "Formula:",
        'ready': "Ready",
        'cache': "Cache",
        'optimizing': "Optimizing...",
        'fit_complete': "Fit complete!",
        'copied_text': "📋 Text copied!",
        'copied_graph': "🖼 Graph copied!",
        'loaded_cache': "Loaded from cache",
        'default_params': "Default params (not optimized)",
        'select_harmonic': "Select at least one harmonic!",
        'already_optimizing': "Optimization already in progress!",
        'error': "Error",
        'optimization_failed': "Optimization failed:",
        'best': "🏆 Best",
        'efficient': "Efficient",
        'minimal': "Minimal",
        'all': "All",
        'none': "None",
        'subharmonics': "Subharmonics (long cycles)",
        'fundamental': "Fundamental & Harmonics",
        'historical': "Historical",
        'zoom_proj': "Zoom + Projection",
        'long_proj': "Long Projection",
        'stats': "Statistics",
        'years': "years",
        'model': "PERRENOD MODEL",
        'harmonics_selected': "Harmonics",
        'parameters': "Parameters",
        'performance': "PERFORMANCE",
        'projections': "PROJECTIONS vs Power Law",
        'de_params': "DE PARAMETERS",
        'settings_title': "Perrenod Explorer Settings",
        'graphs': "Graphs",
        'optimization': "Optimization",
        'colors': "Colors",
        'zoom_years': "Zoom last (years):",
        'short_proj': "Short projection (years):",
        'long_proj_years': "Long projection (years):",
        'show_pl': "Show Power Law Santostasi",
        'show_grid': "Show grid",
        'de_iterations': "DE Iterations:",
        'de_population': "DE Population:",
        'test_split': "Test split date:",
        'color_btc': "BTC:",
        'color_perrenod': "Perrenod:",
        'color_pl': "Power Law:",
        'save': "Save",
        'cancel': "Cancel",
        'invalid_value': "Invalid value:",
        'credits_title': "Credits & Acknowledgments",
        'credits_text': """
═══════════════════════════════════════════════════════
              PERRENOD EXPLORER v2.0
═══════════════════════════════════════════════════════

This software is a simulator inspired by and based on the 
theoretical work of:

📊 GIOVANNI SANTOSTASI
   - Bitcoin Power Law Theory
   - Statistical analysis of BTC price dynamics
   - YouTube: @GiovanniSantostasi
   - X/Twitter: @Giovann35084111

📊 STEPHEN PERRENOD
   - Log-Periodic Power Law (LPPL) for Bitcoin
   - Physics-based cycle analysis (λ = 2.0)
   - ω = 2π/ln(2) constraint derivation
   - Substack: stephenperrenod.substack.com

The implementation, harmonic optimization, and software 
development by Snarky.

═══════════════════════════════════════════════════════

This tool is for educational and research purposes only.
It does NOT constitute financial advice.

═══════════════════════════════════════════════════════

SOFTWARE AUTHOR:
   👤 Snarky (snarkyaes@proton.me)

═══════════════════════════════════════════════════════

MIT License with Non-Commercial Restriction

Copyright (c) 2025 Snarky (snarkyaes@proton.me)
Based on the work of Giovanni Santostasi and Stephen Perrenod

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software for personal, educational, or research purposes, to use, 
copy, modify, and distribute, subject to the following conditions:

1. The above copyright notice and this permission notice shall be included 
   in all copies or substantial portions of the Software.

2. Attribution to the original authors must be maintained.

3. COMMERCIAL USE IS NOT PERMITTED without prior written consent from the 
   copyright holder. For commercial licensing inquiries, contact:
   snarkyaes@proton.me

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.

""",
    },
    'it': {
        'title': "Perrenod Explorer - ω = 9.0647 LOCKED",
        'draw': "📊 Disegna",
        'calc_r2': "📈 Calcola R²",
        'optimize': "🔄 Ottimizza",
        'copy_text': "📋 Copia Testo",
        'copy_graph': "🖼 Copia Grafico",
        'settings': "⚙ Impostazioni",
        'credits': "ℹ Credits",
        'harmonics': "Armoniche Perrenod",
        'formula': "Formula:",
        'ready': "Pronto",
        'cache': "Cache",
        'optimizing': "Ottimizzazione in corso...",
        'fit_complete': "Fit completato!",
        'copied_text': "📋 Testo copiato!",
        'copied_graph': "🖼 Grafico copiato!",
        'loaded_cache': "Caricato da cache",
        'default_params': "Parametri default (non ottimizzati)",
        'select_harmonic': "Seleziona almeno un'armonica!",
        'already_optimizing': "Ottimizzazione già in corso!",
        'error': "Errore",
        'optimization_failed': "Ottimizzazione fallita:",
        'best': "🏆 Best",
        'efficient': "Efficiente",
        'minimal': "Minimo",
        'all': "Tutte",
        'none': "Nessuna",
        'subharmonics': "Subarmoniche (cicli lunghi)",
        'fundamental': "Fondamentale & Armoniche",
        'historical': "Storico",
        'zoom_proj': "Zoom + Proiezione",
        'long_proj': "Proiezione Lunga",
        'stats': "Statistiche",
        'years': "anni",
        'model': "MODELLO PERRENOD",
        'harmonics_selected': "Armoniche",
        'parameters': "Parametri",
        'performance': "PERFORMANCE",
        'projections': "PROIEZIONI vs Power Law",
        'de_params': "PARAMETRI DE",
        'settings_title': "Impostazioni Perrenod Explorer",
        'graphs': "Grafici",
        'optimization': "Ottimizzazione",
        'colors': "Colori",
        'zoom_years': "Zoom ultimi (anni):",
        'short_proj': "Proiezione breve (anni):",
        'long_proj_years': "Proiezione lunga (anni):",
        'show_pl': "Mostra Power Law Santostasi",
        'show_grid': "Mostra griglia",
        'de_iterations': "DE Iterazioni:",
        'de_population': "DE Popolazione:",
        'test_split': "Data split test:",
        'color_btc': "BTC:",
        'color_perrenod': "Perrenod:",
        'color_pl': "Power Law:",
        'save': "Salva",
        'cancel': "Annulla",
        'invalid_value': "Valore non valido:",
        'credits_title': "Credits & Ringraziamenti",
        'credits_text': """
═══════════════════════════════════════════════════════
              PERRENOD EXPLORER v2.0
═══════════════════════════════════════════════════════

Questo software è un simulatore ispirato e basato sul 
lavoro teorico di:

📊 GIOVANNI SANTOSTASI
   - Teoria Power Law di Bitcoin
   - Analisi statistica delle dinamiche di prezzo BTC
   - YouTube: @GiovanniSantostasi
   - X/Twitter: @Giovann35084111

📊 STEPHEN PERRENOD
   - Log-Periodic Power Law (LPPL) per Bitcoin
   - Analisi dei cicli basata sulla fisica (λ = 2.0)
   - Derivazione del vincolo ω = 2π/ln(2)
   - Substack: stephenperrenod.substack.com

Implementazione, ottimizzazione delle armoniche e sviluppo 
software a cura di SnarkyAES

═══════════════════════════════════════════════════════

Questo strumento è solo per scopi educativi e di ricerca.
NON costituisce consulenza finanziaria.

═══════════════════════════════════════════════════════

AUTORE SOFTWARE:
      👤 Snarky (snarkyaes@proton.me)

═══════════════════════════════════════════════════════

MIT License with Non-Commercial Restriction

Copyright (c) 2025 Snarky (snarkyaes@proton.me)
Based on the work of Giovanni Santostasi and Stephen Perrenod

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software for personal, educational, or research purposes, to use, 
copy, modify, and distribute, subject to the following conditions:

1. The above copyright notice and this permission notice shall be included 
   in all copies or substantial portions of the Software.

2. Attribution to the original authors must be maintained.

3. COMMERCIAL USE IS NOT PERMITTED without prior written consent from the 
   copyright holder. For commercial licensing inquiries, contact:
   snarkyaes@proton.me

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.

""",
    }
}

# ============================================================
# CONSTANTS
# ============================================================

GENESIS_DATE = pd.Timestamp("2009-01-03")
OMEGA_LOCKED = 2 * np.pi / np.log(2)  # = 9.064720
LAMBDA = 2.0

# ============================================================
# DEFAULT SETTINGS
# ============================================================

DEFAULT_SETTINGS = {
    'language': 'en',
    'storico_anni': 0,
    'zoom_anni': 2,
    'proiezione_breve': 5,
    'proiezione_lunga': 50,
    'mostra_power_law': True,
    'mostra_griglia': True,
    'scala_log': True,
    'tema': 'scuro',
    'colore_btc': '#FFFFFF',
    'colore_perrenod': '#4ECDC4',
    'colore_pl': '#FF6B6B',
    'pl_a_log10': -17.01,
    'pl_b': 5.82,
    'de_iter': 1000,
    'de_pop': 20,
    'de_tol': 1e-7,
    'test_split_date': '2023-01-01',
}

# Harmonics
ALL_HARMONICS = [
    (0.25, "1/4", "λ=16.0, ~16y"),
    (0.333, "1/3", "λ=8.0, ~12y"),
    (0.5, "1/2", "λ=4.0, ~8y"),
    (0.75, "3/4", "λ=2.83, ~5.3y"),
    (1, "1ª", "λ=2.0, ~4y"),
    (2, "2ª", "λ=1.41, ~2y"),
    (3, "3ª", "λ=1.26, ~1.3y"),
    (4, "4ª", "λ=1.19, ~1y"),
    (5, "5ª", "λ=1.15, ~0.8y"),
    (6, "6ª", "λ=1.12, ~0.7y"),
    (7, "7ª", "λ=1.10, ~0.6y"),
    (8, "8ª", "λ=1.08, ~0.5y"),
    (9, "9ª", "λ=1.07, ~0.4y"),
    (10, "10ª", "λ=1.06, ~0.4y"),
    (11, "11ª", "λ=1.06, ~0.36y"),
    (12, "12ª", "λ=1.05, ~0.33y"),
]

PRESET_BEST = [1, 3, 6]       # R² test = 0.8741
PRESET_EFFICIENT = [1, 3]     # R² test = 0.8685
PRESET_MINIMAL = [1]          # R² test = 0.8533

# Best params for [1] harmonic
BEST_1_HARM_PARAMS = {
    'alpha': 5.726122,
    'c': -38.224161,
    'harmonics': {1: (99.999947, -0.650437, 1.030313)},
    'r2_train': 0.9736,
    'r2_test': 0.8533,
    'r2_full': 0.9796,
}

CACHE_FILE = "perrenod_cache.json"
SETTINGS_FILE = "perrenod_settings.json"
DATA_FILE = "btc_data_full.csv"

# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                saved = json.load(f)
                settings = DEFAULT_SETTINGS.copy()
                settings.update(saved)
                return settings
        except:
            pass
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=2)

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=2)

def get_cache_key(harmonics, de_iter, de_pop):
    harm_str = ",".join(str(h) for h in sorted(harmonics))
    key_str = f"perrenod_{harm_str}|{de_iter}|{de_pop}"
    return hashlib.md5(key_str.encode()).hexdigest()[:16]

def fetch_btc_data():
    url = "https://min-api.cryptocompare.com/data/v2/histoday"
    all_data = []
    to_ts = None
    while True:
        params = {'fsym': 'BTC', 'tsym': 'USD', 'limit': 2000}
        if to_ts:
            params['toTs'] = to_ts
        response = requests.get(url, params=params, timeout=30)
        data = response.json()
        if data['Response'] != 'Success':
            break
        rows = data['Data']['Data']
        if not rows or rows[0]['time'] == 0:
            break
        all_data = rows + all_data
        to_ts = rows[0]['time'] - 1
        if to_ts < 1279324800:
            break
    df = pd.DataFrame(all_data)
    df['date'] = pd.to_datetime(df['time'], unit='s')
    df = df[['date', 'close']].copy()
    df = df[df['close'] > 0].copy()
    return df

def load_btc_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE, parse_dates=['date'])
    else:
        df = fetch_btc_data()
        df.to_csv(DATA_FILE, index=False)
    df['days'] = (df['date'] - GENESIS_DATE).dt.days
    df = df[df['days'] > 0].copy()
    return df

# ============================================================
# MODEL FUNCTIONS
# ============================================================

def perrenod_model(x, t, ln_t, harmonics):
    alpha = x[0]
    c = x[1]
    result = alpha * ln_t + c
    for i, harm_idx in enumerate(harmonics):
        A = x[2 + i*3]
        beta = x[3 + i*3]
        phi = x[4 + i*3]
        oscillation = A * np.power(t, beta) * np.cos(harm_idx * OMEGA_LOCKED * ln_t + phi)
        result += oscillation
    return result

def make_x0_perrenod(harmonics):
    n_harm = len(harmonics)
    x = np.zeros(2 + n_harm * 3)
    x[0] = 5.72
    x[1] = -38.2
    for i, harm_idx in enumerate(harmonics):
        if harm_idx == 1:
            x[2 + i*3] = 100.0
            x[3 + i*3] = -0.65
            x[4 + i*3] = 1.03
        else:
            x[2 + i*3] = 10.0 / harm_idx
            x[3 + i*3] = -0.5
            x[4 + i*3] = 0.0
    return x

def make_bounds_perrenod(n_harm):
    bounds = [(5.2, 6.4), (-45, -30)]
    for _ in range(n_harm):
        bounds.extend([(0.001, 200), (-1.0, -0.01), (0, 2*np.pi)])
    return bounds

def power_law(t, a_log10, b):
    a = 10 ** a_log10
    return a * np.power(t, b)

# ============================================================
# MAIN CLASS
# ============================================================

class PerrenodExplorer:
    def __init__(self, root):
        self.root = root
        self.settings = load_settings()
        self.cache = load_cache()
        self.lang = self.settings.get('language', 'en')
        self.tr = TRANSLATIONS[self.lang]
        
        self.root.title(self.tr['title'])
        self.root.geometry("1450x950")
        
        self.load_data()
        
        self.harm_vars = {}
        self.current_params = None
        self.current_stats = None
        self.is_fitting = False
        self.current_de_iter = self.settings['de_iter']
        self.current_de_pop = self.settings['de_pop']
        
        self.create_widgets()
        self.apply_theme()
        
        self.root.after(100, self.select_best)
    
    def t(self, key):
        """Get translation"""
        return self.tr.get(key, key)
    
    def switch_language(self, lang):
        """Switch language"""
        self.lang = lang
        self.settings['language'] = lang
        save_settings(self.settings)
        self.tr = TRANSLATIONS[lang]
        self.update_ui_texts()
    
    def update_ui_texts(self):
        """Update all UI texts after language change"""
        self.root.title(self.t('title'))
        self.btn_draw.config(text=self.t('draw'))
        self.btn_calc.config(text=self.t('calc_r2'))
        self.btn_opt.config(text=self.t('optimize'))
        self.btn_copy_text.config(text=self.t('copy_text'))
        self.btn_copy_graph.config(text=self.t('copy_graph'))
        self.btn_settings.config(text=self.t('settings'))
        self.btn_credits.config(text=self.t('credits'))
        self.harm_label.config(text=self.t('harmonics'))
        self.cache_label.config(text=f"{self.t('cache')}: {len(self.cache)}")
        self.status_var.set(self.t('ready'))
        self.update_plots()
    
    def load_data(self):
        try:
            self.df = load_btc_data()
            self.today_days = self.df['days'].max()
            self.today_date = self.df['date'].max()
            
            split_date = pd.Timestamp(self.settings['test_split_date'])
            self.df_train = self.df[self.df['date'] < split_date].copy()
            self.df_test = self.df[self.df['date'] >= split_date].copy()
            
            self.t_train = self.df_train['days'].values.astype(np.float64)
            self.y_train = np.log(self.df_train['close'].values)
            self.ln_t_train = np.log(self.t_train)
            self.n_train = len(self.t_train)
            self.ss_tot_train = np.sum((self.y_train - np.mean(self.y_train))**2)
            
            self.t_test = self.df_test['days'].values.astype(np.float64)
            self.y_test = np.log(self.df_test['close'].values)
            self.ln_t_test = np.log(self.t_test)
            self.n_test = len(self.t_test)
            self.ss_tot_test = np.sum((self.y_test - np.mean(self.y_test))**2)
            
            self.t_full = self.df['days'].values.astype(np.float64)
            self.y_full = np.log(self.df['close'].values)
            self.ln_t_full = np.log(self.t_full)
            self.n_full = len(self.t_full)
            self.ss_tot_full = np.sum((self.y_full - np.mean(self.y_full))**2)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot load data:\n{e}")
    
    def create_widgets(self):
        # ============ TOOLBAR ============
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        self.btn_draw = ttk.Button(toolbar, text=self.t('draw'), command=self.draw_only)
        self.btn_draw.pack(side=tk.LEFT, padx=2)
        
        self.btn_calc = ttk.Button(toolbar, text=self.t('calc_r2'), command=self.calc_r2_only)
        self.btn_calc.pack(side=tk.LEFT, padx=2)
        
        self.btn_opt = ttk.Button(toolbar, text=self.t('optimize'), command=self.run_fit)
        self.btn_opt.pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5, fill=tk.Y)
        
        self.btn_copy_text = ttk.Button(toolbar, text=self.t('copy_text'), command=self.copy_results)
        self.btn_copy_text.pack(side=tk.LEFT, padx=2)
        
        self.btn_copy_graph = ttk.Button(toolbar, text=self.t('copy_graph'), command=self.copy_graph)
        self.btn_copy_graph.pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5, fill=tk.Y)
        
        self.btn_settings = ttk.Button(toolbar, text=self.t('settings'), command=self.open_settings)
        self.btn_settings.pack(side=tk.LEFT, padx=2)
        
        self.btn_credits = ttk.Button(toolbar, text=self.t('credits'), command=self.show_credits)
        self.btn_credits.pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5, fill=tk.Y)
        
        # Language buttons
        lang_frame = ttk.Frame(toolbar)
        lang_frame.pack(side=tk.LEFT, padx=5)
        
        self.btn_en = ttk.Button(lang_frame, text="EN", width=3, 
                                  command=lambda: self.switch_language('en'))
        self.btn_en.pack(side=tk.LEFT, padx=1)
        
        self.btn_it = ttk.Button(lang_frame, text="IT", width=3,
                                  command=lambda: self.switch_language('it'))
        self.btn_it.pack(side=tk.LEFT, padx=1)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5, fill=tk.Y)
        
        # DE params
        ttk.Label(toolbar, text="DE Iter:").pack(side=tk.LEFT, padx=2)
        self.de_iter_var = tk.StringVar(value=str(self.settings['de_iter']))
        ttk.Entry(toolbar, textvariable=self.de_iter_var, width=6).pack(side=tk.LEFT, padx=2)
        
        ttk.Label(toolbar, text="Pop:").pack(side=tk.LEFT, padx=2)
        self.de_pop_var = tk.StringVar(value=str(self.settings['de_pop']))
        ttk.Entry(toolbar, textvariable=self.de_pop_var, width=4).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5, fill=tk.Y)
        
        omega_label = ttk.Label(toolbar, text=f"ω = {OMEGA_LOCKED:.4f} (LOCKED)", 
                                font=('Arial', 10, 'bold'))
        omega_label.pack(side=tk.LEFT, padx=10)
        
        self.status_var = tk.StringVar(value=self.t('ready'))
        self.status_label = ttk.Label(toolbar, textvariable=self.status_var)
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        self.cache_label = ttk.Label(toolbar, text=f"{self.t('cache')}: {len(self.cache)}")
        self.cache_label.pack(side=tk.RIGHT, padx=10)
        
        # ============ MAIN CONTAINER ============
        main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # ============ LEFT PANEL ============
        left_frame = ttk.LabelFrame(main_container, text=self.t('harmonics'), width=250)
        main_container.add(left_frame, weight=0)
        self.harm_label = left_frame
        
        # Info
        info_frame = ttk.Frame(left_frame)
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(info_frame, text=self.t('formula'), font=('Arial', 9, 'bold')).pack(anchor=tk.W)
        ttk.Label(info_frame, text="ln(P) = α·ln(t) + c +", font=('Courier', 8)).pack(anchor=tk.W)
        ttk.Label(info_frame, text="  Σ Aᵢ·t^βᵢ·cos(i·ω·ln(t)+φᵢ)", font=('Courier', 8)).pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"ω = 2π/ln(2) = {OMEGA_LOCKED:.4f}", font=('Arial', 8)).pack(anchor=tk.W, pady=(5,0))
        ttk.Label(info_frame, text=f"λ = 2.0", font=('Arial', 8)).pack(anchor=tk.W)
        
        ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=5, pady=5)
        
        # Harmonics with scrollbar
        harm_container = ttk.Frame(left_frame)
        harm_container.pack(fill=tk.BOTH, expand=True, padx=5)
        
        harm_canvas = tk.Canvas(harm_container, bg='#2d2d2d', highlightthickness=0, height=350)
        harm_scrollbar = ttk.Scrollbar(harm_container, orient=tk.VERTICAL, command=harm_canvas.yview)
        harm_frame = ttk.Frame(harm_canvas)
        
        harm_canvas.configure(yscrollcommand=harm_scrollbar.set)
        harm_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        harm_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        harm_window = harm_canvas.create_window((0, 0), window=harm_frame, anchor=tk.NW)
        
        for harm_idx, name, desc in ALL_HARMONICS:
            var = tk.BooleanVar(value=harm_idx in PRESET_BEST)
            self.harm_vars[harm_idx] = var
            label = f"{name} ({desc})"
            cb = ttk.Checkbutton(harm_frame, text=label, variable=var)
            cb.pack(anchor=tk.W, pady=1)
        
        def on_frame_configure(event):
            harm_canvas.configure(scrollregion=harm_canvas.bbox("all"))
        
        def on_canvas_configure(event):
            harm_canvas.itemconfig(harm_window, width=event.width)
        
        harm_frame.bind("<Configure>", on_frame_configure)
        harm_canvas.bind("<Configure>", on_canvas_configure)
        
        def on_mousewheel(event):
            harm_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        harm_canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=5, pady=5)
        
        # Preset buttons
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(btn_frame, text=self.t('best'), command=self.select_best, width=8).pack(side=tk.LEFT, padx=1)
        ttk.Button(btn_frame, text=self.t('efficient'), command=self.select_efficient, width=8).pack(side=tk.LEFT, padx=1)
        
        btn_frame2 = ttk.Frame(left_frame)
        btn_frame2.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(btn_frame2, text=self.t('minimal'), command=self.select_minimal, width=8).pack(side=tk.LEFT, padx=1)
        ttk.Button(btn_frame2, text=self.t('none'), command=self.select_none, width=8).pack(side=tk.LEFT, padx=1)
        
        # ============ RIGHT PANEL ============
        right_frame = ttk.Frame(main_container)
        main_container.add(right_frame, weight=1)
        
        self.fig = Figure(figsize=(12, 8), facecolor='#1a1a2e')
        self.axes = self.fig.subplots(2, 2)
        
        for ax in self.axes.flat:
            ax.set_facecolor('#1a1a2e')
            ax.tick_params(colors='white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.title.set_color('white')
            for spine in ax.spines.values():
                spine.set_color('white')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.fig.tight_layout()
    
    def apply_theme(self):
        if self.settings['tema'] == 'scuro':
            self.root.configure(bg='#2d2d2d')
            style = ttk.Style()
            style.theme_use('clam')
            style.configure('.', background='#2d2d2d', foreground='white')
            style.configure('TFrame', background='#2d2d2d')
            style.configure('TLabel', background='#2d2d2d', foreground='white')
            style.configure('TLabelframe', background='#2d2d2d', foreground='white')
            style.configure('TLabelframe.Label', background='#2d2d2d', foreground='white')
            style.configure('TButton', background='#3d3d3d', foreground='white')
            style.configure('TCheckbutton', background='#2d2d2d', foreground='white')
            style.configure('TEntry', fieldbackground='white', foreground='black')
            style.map('TEntry', fieldbackground=[('readonly', 'white')], foreground=[('readonly', 'black')])
    
    def get_selected_harmonics(self):
        return sorted([h for h, var in self.harm_vars.items() if var.get()])
    
    def flash_button(self, button, color='#00ff00'):
        """Flash button to indicate action"""
        original_style = button.cget('style')
        style = ttk.Style()
        style.configure('Flash.TButton', background=color)
        button.configure(style='Flash.TButton')
        self.root.after(200, lambda: button.configure(style=original_style if original_style else 'TButton'))
    
    def copy_results(self):
        """Copy results to clipboard"""
        harmonics = self.get_selected_harmonics()
        de_iter = int(self.de_iter_var.get())
        de_pop = int(self.de_pop_var.get())
        
        text = "=" * 50 + "\n"
        text += "PERRENOD EXPLORER - RESULTS\n"
        text += "=" * 50 + "\n\n"
        
        text += f"ω = {OMEGA_LOCKED:.6f} (LOCKED)\n"
        text += f"λ = {LAMBDA}\n\n"
        
        text += f"Harmonics: {harmonics}\n"
        text += f"N parameters: {2 + len(harmonics)*3}\n\n"
        
        text += f"DE PARAMETERS:\n"
        text += f"  Iterations: {de_iter}\n"
        text += f"  Population: {de_pop}\n\n"
        
        if self.current_stats:
            s = self.current_stats
            text += "PERFORMANCE:\n"
            text += f"  R² train: {s['r2_train']:.4f}\n"
            text += f"  R² test:  {s['r2_test']:.4f}\n"
            text += f"  R² full:  {s['r2_full']:.4f}\n"
            text += f"  BIC:      {s['bic']:.1f}\n\n"
            
            text += "PROJECTIONS vs Power Law:\n"
            text += f"  Ratio +10y: {s['ratio_10y']:.2f}x\n"
            text += f"  Ratio +25y: {s['ratio_25y']:.2f}x\n"
            text += f"  Ratio +50y: {s['ratio_50y']:.2f}x\n\n"
        
        if self.current_params is not None:
            x = self.current_params
            text += "PARAMETERS:\n"
            text += f"  α (slope)     = {x[0]:.6f}\n"
            text += f"  c (intercept) = {x[1]:.6f}\n\n"
            
            text += "HARMONICS:\n"
            for i, harm_idx in enumerate(harmonics):
                A = x[2 + i*3]
                beta = x[3 + i*3]
                phi = x[4 + i*3]
                omega_eff = harm_idx * OMEGA_LOCKED
                lambda_eff = np.exp(2 * np.pi / omega_eff)
                text += f"  Harm {harm_idx}: A={A:.4f}, β={beta:.4f}, φ={phi:.4f} (λ={lambda_eff:.3f})\n"
            
            text += f"\nRAW PARAMS: {self.current_params.tolist()}\n"
        
        text += "\n" + "=" * 50
        
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()
        
        self.flash_button(self.btn_copy_text)
        self.status_var.set(self.t('copied_text'))
    
    def copy_graph(self):
        """Copy graph to clipboard"""
        try:
            # Save figure to bytes
            buf = io.BytesIO()
            self.fig.savefig(buf, format='png', dpi=150, facecolor='#1a1a2e', bbox_inches='tight')
            buf.seek(0)
            
            # Load as PIL image
            img = Image.open(buf)
            
            # Copy to clipboard (Windows)
            output = io.BytesIO()
            img.convert('RGB').save(output, 'BMP')
            data = output.getvalue()[14:]  # Remove BMP header
            output.close()
            
            import win32clipboard
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()
            
            self.flash_button(self.btn_copy_graph)
            self.status_var.set(self.t('copied_graph'))
            
        except ImportError:
            # Fallback: save to file
            filename = f"perrenod_graph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            self.fig.savefig(filename, dpi=150, facecolor='#1a1a2e', bbox_inches='tight')
            self.status_var.set(f"Saved: {filename}")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)[:30]}")
    
    def show_credits(self):
        """Show credits window"""
        credits_win = tk.Toplevel(self.root)
        credits_win.title(self.t('credits_title'))
        credits_win.geometry("600x550")
        credits_win.transient(self.root)
        credits_win.grab_set()
        
        if self.settings['tema'] == 'scuro':
            credits_win.configure(bg='#2d2d2d')
        
        text_widget = tk.Text(credits_win, wrap=tk.WORD, font=('Consolas', 10),
                             bg='#1a1a2e', fg='white', padx=20, pady=20)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert('1.0', self.t('credits_text'))
        text_widget.config(state=tk.DISABLED)
        
        ttk.Button(credits_win, text="OK", command=credits_win.destroy).pack(pady=10)
    
    def select_best(self):
        for h, var in self.harm_vars.items():
            var.set(h in PRESET_BEST)
        self.status_var.set(f"🏆 Best [1,3,6] - R² test ≈ 0.874")
    
    def select_efficient(self):
        for h, var in self.harm_vars.items():
            var.set(h in PRESET_EFFICIENT)
        self.status_var.set(f"[1,3] - R² test ≈ 0.869")
    
    def select_minimal(self):
        for h, var in self.harm_vars.items():
            var.set(h in PRESET_MINIMAL)
        # Load optimized params
        p = BEST_1_HARM_PARAMS
        harm_params = p['harmonics'][1]
        self.current_params = np.array([p['alpha'], p['c'], harm_params[0], harm_params[1], harm_params[2]])
        self.current_stats = {
            'r2_train': p['r2_train'], 'r2_test': p['r2_test'], 'r2_full': p['r2_full'],
            'bic': -5800, 'n_params': 5, 'n_harm': 1,
            'ratio_10y': 0.86, 'ratio_25y': 1.23, 'ratio_50y': 0.99,
            'alpha': p['alpha'], 'c': p['c'],
        }
        self.status_var.set(f"[1] - R² test = 0.8533")
        self.update_plots()
    
    def select_none(self):
        for var in self.harm_vars.values():
            var.set(False)
        self.status_var.set(self.t('ready'))
    
    def calc_r2_only(self):
        harmonics = self.get_selected_harmonics()
        if not harmonics:
            self.status_var.set(self.t('select_harmonic'))
            return
        
        de_iter = int(self.de_iter_var.get())
        de_pop = int(self.de_pop_var.get())
        cache_key = get_cache_key(harmonics, de_iter, de_pop)
        
        if cache_key in self.cache:
            self.current_params = np.array(self.cache[cache_key]['params'])
            self.current_stats = self.cache[cache_key]['stats']
            self.status_var.set(self.t('loaded_cache'))
        else:
            self.current_params = make_x0_perrenod(harmonics)
            self.current_stats = self._calc_stats(self.current_params, harmonics)
            self.status_var.set(self.t('default_params'))
        
        self.current_de_iter = de_iter
        self.current_de_pop = de_pop
        self.update_plots()
    
    def run_fit(self):
        if self.is_fitting:
            self.status_var.set(self.t('already_optimizing'))
            return
        
        harmonics = self.get_selected_harmonics()
        if not harmonics:
            self.status_var.set(self.t('select_harmonic'))
            return
        
        de_iter = int(self.de_iter_var.get())
        de_pop = int(self.de_pop_var.get())
        cache_key = get_cache_key(harmonics, de_iter, de_pop)
        
        if cache_key in self.cache:
            self.current_params = np.array(self.cache[cache_key]['params'])
            self.current_stats = self.cache[cache_key]['stats']
            self.current_de_iter = de_iter
            self.current_de_pop = de_pop
            self.status_var.set(self.t('loaded_cache'))
            self.update_plots()
            return
        
        self.is_fitting = True
        self.status_var.set(self.t('optimizing'))
        
        thread = threading.Thread(target=self._fit_thread, args=(harmonics, de_iter, de_pop, cache_key))
        thread.start()
    
    def _fit_thread(self, harmonics, de_iter, de_pop, cache_key):
        try:
            x0 = make_x0_perrenod(harmonics)
            bounds = make_bounds_perrenod(len(harmonics))
            
            for i in range(len(x0)):
                x0[i] = np.clip(x0[i], bounds[i][0], bounds[i][1])
            
            def objective(x):
                try:
                    y_pred = perrenod_model(x, self.t_train, self.ln_t_train, harmonics)
                    ss = np.sum((self.y_train - y_pred)**2)
                    return ss if not (np.isnan(ss) or np.isinf(ss)) else 1e30
                except:
                    return 1e30
            
            result = differential_evolution(objective, bounds, x0=x0, maxiter=de_iter, popsize=de_pop,
                                           workers=1, updating='immediate', polish=True,
                                           tol=float(self.settings['de_tol']), seed=42)
            
            x_opt = result.x
            stats = self._calc_stats(x_opt, harmonics)
            
            self.cache[cache_key] = {
                'harmonics': harmonics, 'params': x_opt.tolist(),
                'stats': stats, 'timestamp': datetime.now().isoformat()
            }
            save_cache(self.cache)
            
            self.current_params = x_opt
            self.current_stats = stats
            self.current_de_iter = de_iter
            self.current_de_pop = de_pop
            
            self.root.after(0, self._fit_complete)
        except Exception as e:
            self.root.after(0, lambda: self._fit_error(str(e)))
    
    def _calc_stats(self, x, harmonics):
        n_harm = len(harmonics)
        n_params = 2 + n_harm * 3
        
        y_pred_train = perrenod_model(x, self.t_train, self.ln_t_train, harmonics)
        ss_res_train = np.sum((self.y_train - y_pred_train)**2)
        r2_train = 1 - ss_res_train / self.ss_tot_train
        bic_train = self.n_train * np.log(ss_res_train / self.n_train) + n_params * np.log(self.n_train)
        
        y_pred_test = perrenod_model(x, self.t_test, self.ln_t_test, harmonics)
        ss_res_test = np.sum((self.y_test - y_pred_test)**2)
        r2_test = 1 - ss_res_test / self.ss_tot_test
        
        y_pred_full = perrenod_model(x, self.t_full, self.ln_t_full, harmonics)
        ss_res_full = np.sum((self.y_full - y_pred_full)**2)
        r2_full = 1 - ss_res_full / self.ss_tot_full
        
        pl_a = 10 ** self.settings['pl_a_log10']
        pl_b = self.settings['pl_b']
        
        ratios = {}
        for years in [10, 25, 50]:
            fd = self.today_days + years * 365.25
            p_perrenod = np.exp(perrenod_model(x, np.array([fd]), np.log(np.array([fd])), harmonics))[0]
            p_pl = pl_a * (fd ** pl_b)
            ratios[years] = p_perrenod / p_pl
        
        return {
            'r2_train': float(r2_train), 'r2_test': float(r2_test), 'r2_full': float(r2_full),
            'bic': float(bic_train), 'n_params': n_params, 'n_harm': n_harm,
            'ratio_10y': float(ratios[10]), 'ratio_25y': float(ratios[25]), 'ratio_50y': float(ratios[50]),
            'alpha': float(x[0]), 'c': float(x[1]),
        }
    
    def _fit_complete(self):
        self.is_fitting = False
        self.status_var.set(self.t('fit_complete'))
        self.cache_label.config(text=f"{self.t('cache')}: {len(self.cache)}")
        self.update_plots()
    
    def _fit_error(self, error):
        self.is_fitting = False
        self.status_var.set(f"{self.t('error')}!")
        messagebox.showerror(self.t('error'), f"{self.t('optimization_failed')}\n{error}")
    
    def draw_only(self):
        harmonics = self.get_selected_harmonics()
        if not harmonics:
            self.clear_plots()
            return
        
        de_iter = int(self.de_iter_var.get())
        de_pop = int(self.de_pop_var.get())
        cache_key = get_cache_key(harmonics, de_iter, de_pop)
        
        if cache_key in self.cache:
            self.current_params = np.array(self.cache[cache_key]['params'])
            self.current_stats = self.cache[cache_key]['stats']
            self.status_var.set(self.t('loaded_cache'))
        else:
            self.current_params = make_x0_perrenod(harmonics)
            self.current_stats = None
            self.status_var.set(self.t('default_params'))
        
        self.current_de_iter = de_iter
        self.current_de_pop = de_pop
        self.update_plots()
    
    def update_plots(self):
        harmonics = self.get_selected_harmonics()
        if not harmonics or self.current_params is None:
            self.clear_plots()
            return
        
        x = self.current_params
        col_btc = self.settings['colore_btc']
        col_perrenod = self.settings['colore_perrenod']
        col_pl = self.settings['colore_pl']
        pl_a = 10 ** self.settings['pl_a_log10']
        pl_b = self.settings['pl_b']
        
        for ax in self.axes.flat:
            ax.clear()
            ax.set_facecolor('#1a1a2e')
            ax.tick_params(colors='white')
            ax.grid(self.settings['mostra_griglia'], alpha=0.3)
        
        # Plot 1: Historical
        ax1 = self.axes[0, 0]
        ax1.semilogy(self.df['date'], self.df['close'], color=col_btc, alpha=0.6, lw=0.8, label='BTC')
        y_fit = perrenod_model(x, self.t_full, self.ln_t_full, harmonics)
        ax1.semilogy(self.df['date'], np.exp(y_fit), color=col_perrenod, lw=2, label='Perrenod')
        if self.settings['mostra_power_law']:
            y_pl = power_law(self.t_full, self.settings['pl_a_log10'], pl_b)
            ax1.semilogy(self.df['date'], y_pl, color=col_pl, lw=1.5, ls='--', label='Power Law')
        ax1.axvline(pd.Timestamp(self.settings['test_split_date']), color='yellow', ls='--', alpha=0.7)
        ax1.set_title(self.t('historical'), color='white', fontweight='bold')
        ax1.legend(loc='upper left', fontsize=8)
        
        # Plot 2: Zoom + projection
        ax2 = self.axes[0, 1]
        zoom_anni = self.settings['zoom_anni']
        proj_breve = self.settings['proiezione_breve']
        start_date = self.today_date - pd.Timedelta(days=zoom_anni*365)
        df_zoom = self.df[self.df['date'] >= start_date]
        ax2.semilogy(df_zoom['date'], df_zoom['close'], color=col_btc, alpha=0.8, lw=1, label='BTC')
        end_days = self.today_days + proj_breve * 365.25
        proj_days = np.linspace(df_zoom['days'].min(), end_days, 500)
        proj_dates = pd.to_datetime(GENESIS_DATE) + pd.to_timedelta(proj_days, unit='D')
        y_proj = perrenod_model(x, proj_days, np.log(proj_days), harmonics)
        ax2.semilogy(proj_dates, np.exp(y_proj), color=col_perrenod, lw=2, label='Perrenod')
        if self.settings['mostra_power_law']:
            y_pl = power_law(proj_days, self.settings['pl_a_log10'], pl_b)
            ax2.semilogy(proj_dates, y_pl, color=col_pl, lw=1.5, ls='--', label='Power Law')
        ax2.axvline(self.today_date, color='yellow', ls=':', alpha=0.8)
        ax2.set_title(f"{self.t('zoom_proj')} ({zoom_anni}y + {proj_breve}y)", color='white', fontweight='bold')
        ax2.legend(loc='upper left', fontsize=8)
        
        # Plot 3: Long projection
        ax3 = self.axes[1, 0]
        proj_lunga = self.settings['proiezione_lunga']
        end_days = self.today_days + proj_lunga * 365.25
        proj_days = np.linspace(365, end_days, 1000)
        proj_dates = pd.to_datetime(GENESIS_DATE) + pd.to_timedelta(proj_days, unit='D')
        ax3.semilogy(self.df['date'], self.df['close'], color=col_btc, alpha=0.3, lw=0.5)
        y_proj = perrenod_model(x, proj_days, np.log(proj_days), harmonics)
        ax3.semilogy(proj_dates, np.exp(y_proj), color=col_perrenod, lw=2, label='Perrenod')
        if self.settings['mostra_power_law']:
            y_pl = power_law(proj_days, self.settings['pl_a_log10'], pl_b)
            ax3.semilogy(proj_dates, y_pl, color=col_pl, lw=1.5, ls='--', label='Power Law')
        ax3.axvline(self.today_date, color='yellow', ls=':', alpha=0.8)
        ax3.set_title(f"{self.t('long_proj')} ({proj_lunga} {self.t('years')})", color='white', fontweight='bold')
        ax3.legend(loc='upper left', fontsize=8)
        ax3.set_ylim(1, 1e12)
        
        # Plot 4: Stats
        ax4 = self.axes[1, 1]
        ax4.axis('off')
        
        stats_text = f"{self.t('model')}\n{'='*35}\n\n"
        stats_text += f"ω = {OMEGA_LOCKED:.4f} (LOCKED)\n"
        stats_text += f"λ = {LAMBDA}\n\n"
        stats_text += f"{self.t('harmonics_selected')}: {harmonics}\n"
        stats_text += f"{self.t('parameters')}: {2 + len(harmonics)*3}\n\n"
        
        stats_text += f"{self.t('de_params')}:\n"
        stats_text += f"  Iter: {self.current_de_iter}, Pop: {self.current_de_pop}\n\n"
        
        if self.current_stats:
            s = self.current_stats
            stats_text += f"{self.t('performance')}:\n"
            stats_text += f"  R² train: {s['r2_train']:.4f}\n"
            stats_text += f"  R² test:  {s['r2_test']:.4f}\n"
            stats_text += f"  R² full:  {s['r2_full']:.4f}\n"
            stats_text += f"  BIC:      {s['bic']:.1f}\n\n"
            stats_text += f"{self.t('projections')}:\n"
            stats_text += f"  +10y: {s['ratio_10y']:.2f}x\n"
            stats_text += f"  +25y: {s['ratio_25y']:.2f}x\n"
            stats_text += f"  +50y: {s['ratio_50y']:.2f}x\n\n"
            stats_text += f"α = {s['alpha']:.4f}\n"
            stats_text += f"c = {s['c']:.4f}\n"
        
        ax4.text(0.1, 0.95, stats_text, transform=ax4.transAxes, fontsize=10,
                verticalalignment='top', fontfamily='monospace', color='white',
                bbox=dict(boxstyle='round', facecolor='#2a2a4e', alpha=0.8))
        
        self.fig.tight_layout()
        self.canvas.draw()
    
    def clear_plots(self):
        for ax in self.axes.flat:
            ax.clear()
            ax.set_facecolor('#1a1a2e')
        self.canvas.draw()
    
    def open_settings(self):
        SettingsWindow(self.root, self.settings, self.on_settings_save, self.t)
    
    def on_settings_save(self, new_settings):
        self.settings = new_settings
        save_settings(self.settings)
        self.apply_theme()
        self.update_plots()


# ============================================================
# SETTINGS WINDOW
# ============================================================

class SettingsWindow:
    def __init__(self, parent, settings, callback, t_func):
        self.settings = settings.copy()
        self.callback = callback
        self.t = t_func
        
        self.window = tk.Toplevel(parent)
        self.window.title(self.t('settings_title'))
        self.window.geometry("450x450")
        self.window.transient(parent)
        self.window.grab_set()
        
        if settings['tema'] == 'scuro':
            self.window.configure(bg='#2d2d2d')
        
        self.create_widgets()
    
    def create_widgets(self):
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Graphs tab
        tab_graphs = ttk.Frame(notebook)
        notebook.add(tab_graphs, text=self.t('graphs'))
        
        row = 0
        ttk.Label(tab_graphs, text=self.t('zoom_years')).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        self.zoom_var = tk.StringVar(value=str(self.settings['zoom_anni']))
        ttk.Entry(tab_graphs, textvariable=self.zoom_var, width=10).grid(row=row, column=1, padx=10, pady=5)
        
        row += 1
        ttk.Label(tab_graphs, text=self.t('short_proj')).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        self.proj_short_var = tk.StringVar(value=str(self.settings['proiezione_breve']))
        ttk.Entry(tab_graphs, textvariable=self.proj_short_var, width=10).grid(row=row, column=1, padx=10, pady=5)
        
        row += 1
        ttk.Label(tab_graphs, text=self.t('long_proj_years')).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        self.proj_long_var = tk.StringVar(value=str(self.settings['proiezione_lunga']))
        ttk.Entry(tab_graphs, textvariable=self.proj_long_var, width=10).grid(row=row, column=1, padx=10, pady=5)
        
        row += 1
        self.show_pl_var = tk.BooleanVar(value=self.settings['mostra_power_law'])
        ttk.Checkbutton(tab_graphs, text=self.t('show_pl'), variable=self.show_pl_var).grid(row=row, column=0, columnspan=2, sticky=tk.W, padx=10, pady=5)
        
        row += 1
        self.show_grid_var = tk.BooleanVar(value=self.settings['mostra_griglia'])
        ttk.Checkbutton(tab_graphs, text=self.t('show_grid'), variable=self.show_grid_var).grid(row=row, column=0, columnspan=2, sticky=tk.W, padx=10, pady=5)
        
        # Optimization tab
        tab_opt = ttk.Frame(notebook)
        notebook.add(tab_opt, text=self.t('optimization'))
        
        row = 0
        ttk.Label(tab_opt, text=self.t('de_iterations')).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        self.de_iter_var = tk.StringVar(value=str(self.settings['de_iter']))
        ttk.Entry(tab_opt, textvariable=self.de_iter_var, width=10).grid(row=row, column=1, padx=10, pady=5)
        
        row += 1
        ttk.Label(tab_opt, text=self.t('de_population')).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        self.de_pop_var = tk.StringVar(value=str(self.settings['de_pop']))
        ttk.Entry(tab_opt, textvariable=self.de_pop_var, width=10).grid(row=row, column=1, padx=10, pady=5)
        
        row += 1
        ttk.Label(tab_opt, text=self.t('test_split')).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        self.split_var = tk.StringVar(value=self.settings['test_split_date'])
        ttk.Entry(tab_opt, textvariable=self.split_var, width=15).grid(row=row, column=1, padx=10, pady=5)
        
        # Colors tab
        tab_colors = ttk.Frame(notebook)
        notebook.add(tab_colors, text=self.t('colors'))
        
        row = 0
        ttk.Label(tab_colors, text=self.t('color_btc')).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        self.col_btc_var = tk.StringVar(value=self.settings['colore_btc'])
        ttk.Entry(tab_colors, textvariable=self.col_btc_var, width=15).grid(row=row, column=1, padx=10, pady=5)
        
        row += 1
        ttk.Label(tab_colors, text=self.t('color_perrenod')).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        self.col_perrenod_var = tk.StringVar(value=self.settings['colore_perrenod'])
        ttk.Entry(tab_colors, textvariable=self.col_perrenod_var, width=15).grid(row=row, column=1, padx=10, pady=5)
        
        row += 1
        ttk.Label(tab_colors, text=self.t('color_pl')).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        self.col_pl_var = tk.StringVar(value=self.settings['colore_pl'])
        ttk.Entry(tab_colors, textvariable=self.col_pl_var, width=15).grid(row=row, column=1, padx=10, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(self.window)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(btn_frame, text=self.t('save'), command=self.save).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text=self.t('cancel'), command=self.window.destroy).pack(side=tk.RIGHT, padx=5)
    
    def save(self):
        try:
            self.settings['zoom_anni'] = int(self.zoom_var.get())
            self.settings['proiezione_breve'] = int(self.proj_short_var.get())
            self.settings['proiezione_lunga'] = int(self.proj_long_var.get())
            self.settings['mostra_power_law'] = self.show_pl_var.get()
            self.settings['mostra_griglia'] = self.show_grid_var.get()
            self.settings['de_iter'] = int(self.de_iter_var.get())
            self.settings['de_pop'] = int(self.de_pop_var.get())
            self.settings['test_split_date'] = self.split_var.get()
            self.settings['colore_btc'] = self.col_btc_var.get()
            self.settings['colore_perrenod'] = self.col_perrenod_var.get()
            self.settings['colore_pl'] = self.col_pl_var.get()
            
            self.callback(self.settings)
            self.window.destroy()
        except ValueError as e:
            messagebox.showerror(self.t('error'), f"{self.t('invalid_value')}\n{e}")


# ============================================================
# MAIN
# ============================================================

def main():
    root = tk.Tk()
    app = PerrenodExplorer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
