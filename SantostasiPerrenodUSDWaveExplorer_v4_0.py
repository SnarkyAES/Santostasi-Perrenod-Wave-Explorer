# ============================================================
# SANTOSTASI PERRENOD USD WAVE EXPLORER v1.0
# ============================================================
# Based on the original work of Stephen Perrenod (BTC/USD)
# and Giovanni Santostasi (Power Law Theory)
# 
# Formula: ln(P) = α×ln(t) + c + Σ Aᵢ×t^βᵢ × cos(i×ω×ln(t) + φᵢ)
# With physics constraint: ω = 2π/ln(2) = 9.0647 (LOCKED)
# λ = 2.0 → cycles when Bitcoin age doubles
#
# This version uses BTC/USD as in Perrenod's original work
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
import csv
import hashlib
from datetime import datetime
import threading
import requests
from scipy.optimize import differential_evolution
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks
from scipy.interpolate import interp1d
from scipy.stats import norm, skew, kurtosis
import io
from PIL import Image, ImageGrab

# ============================================================
# TRANSLATIONS
# ============================================================

TRANSLATIONS = {
    'en': {
        'title': "Santostasi Perrenod USD Wave Explorer - BTC/USD - ω = 9.0647 LOCKED",
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
        'historical': "Historical BTC/USD",
        'zoom_proj': "Zoom + Projection",
        'long_proj': "Long Projection",
        'residuals': "Residuals (ln scale)",
        'spectral': "Spectral Analysis",
        'spectral_tab': "📊 Spectral",
        'run_spectral': "Run Spectral Analysis",
        'fft_time': "FFT (Time Domain)",
        'fft_logtime': "FFT (Log-Time)",
        'wavelet': "Wavelet Spectrum",
        'wavelet_tab': "🌊 Wavelet",
        'scalogram': "Scalogram (Morlet)",
        'global_wavelet': "Global Wavelet Spectrum",
        'wavelet_stats': "Wavelet Statistics",
        'acf': "Autocorrelation",
        'spectral_stats': "Spectral Statistics",
        'top_periods': "Top Periodic Signals",
        'custom_harm': "Custom Harmonics",
        'stats': "Statistics",
        'years': "years",
        'model': "PERRENOD BTC/USD MODEL",
        'harmonics_selected': "Harmonics",
        'parameters': "Parameters",
        'performance': "PERFORMANCE",
        'projections': "PROJECTIONS vs Power Law",
        'de_params': "DE PARAMETERS",
        'settings_title': "Perrenod USD Wave Explorer Settings",
        'graphs': "Graphs",
        'optimization': "Optimization",
        'colors': "Colors",
        'zoom_years': "Zoom last (years):",
        'short_proj': "Short projection (years):",
        'long_proj_years': "Long projection (years):",
        'show_pl': "Show Power Law BTC/USD",
        'show_grid': "Show grid",
        'de_iterations': "DE Iterations:",
        'de_population': "DE Population:",
        'test_split': "Test split date:",
        'color_btc': "BTC/USD:",
        'color_perrenod': "Perrenod:",
        'color_pl': "Power Law:",
        'save': "Save",
        'cancel': "Cancel",
        'invalid_value': "Invalid value:",
        'loading_data': "Loading BTC and Gold data...",
        'data_loaded': "Data loaded!",
        'credits_title': "Credits & Acknowledgments",
        'credits_text': """
═══════════════════════════════════════════════════════
         PERRENOD GOLD WAVE EXPLORER v1.0
═══════════════════════════════════════════════════════

This software analyzes BTC/USD ratio as in Stephen 
Perrenod's original work.

📊 STEPHEN PERRENOD
   - Log-Periodic Power Law (LPPL) for Bitcoin
   - Original BTC/USD analysis
   - Physics-based cycle analysis (λ = 2.0)
   - ω = 2π/ln(2) constraint derivation
   - Substack: stephenperrenod.substack.com

📊 GIOVANNI SANTOSTASI
   - Bitcoin Power Law Theory
   - Statistical analysis of BTC price dynamics
   - YouTube: @GiovanniSantostasi
   - X/Twitter: @Giovann35084111

Implementation, harmonic optimization, and software 
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
        'title': "Santostasi Perrenod USD Wave Explorer - BTC/USD - ω = 9.0647 LOCKED",
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
        'historical': "Storico BTC/USD",
        'zoom_proj': "Zoom + Proiezione",
        'long_proj': "Proiezione Lunga",
        'residuals': "Residui (scala ln)",
        'spectral': "Analisi Spettrale",
        'spectral_tab': "📊 Spettrale",
        'run_spectral': "Esegui Analisi Spettrale",
        'fft_time': "FFT (Tempo)",
        'fft_logtime': "FFT (Log-Tempo)",
        'wavelet': "Spettro Wavelet",
        'wavelet_tab': "🌊 Wavelet",
        'scalogram': "Scalogramma (Morlet)",
        'global_wavelet': "Spettro Wavelet Globale",
        'wavelet_stats': "Statistiche Wavelet",
        'acf': "Autocorrelazione",
        'spectral_stats': "Statistiche Spettrali",
        'top_periods': "Segnali Periodici",
        'custom_harm': "Armoniche Custom",
        'stats': "Statistiche",
        'years': "anni",
        'model': "MODELLO PERRENOD BTC/GOLD",
        'harmonics_selected': "Armoniche",
        'parameters': "Parametri",
        'performance': "PERFORMANCE",
        'projections': "PROIEZIONI vs Power Law",
        'de_params': "PARAMETRI DE",
        'settings_title': "Impostazioni Perrenod USD Wave Explorer",
        'graphs': "Grafici",
        'optimization': "Ottimizzazione",
        'colors': "Colori",
        'zoom_years': "Zoom ultimi (anni):",
        'short_proj': "Proiezione breve (anni):",
        'long_proj_years': "Proiezione lunga (anni):",
        'show_pl': "Mostra Power Law BTC/USD",
        'show_grid': "Mostra griglia",
        'de_iterations': "DE Iterazioni:",
        'de_population': "DE Popolazione:",
        'test_split': "Data split test:",
        'color_btc': "BTC/USD:",
        'color_perrenod': "Perrenod:",
        'color_pl': "Power Law:",
        'save': "Salva",
        'cancel': "Annulla",
        'invalid_value': "Valore non valido:",
        'loading_data': "Caricamento dati BTC e Oro...",
        'data_loaded': "Dati caricati!",
        'credits_title': "Credits & Ringraziamenti",
        'credits_text': """
═══════════════════════════════════════════════════════
         SANTOSTASI PERRENOD GOLD WAVE EXPLORER v1.0
═══════════════════════════════════════════════════════

Questo software analizza il rapporto BTC/Oro come nel 
lavoro originale di Stephen Perrenod.

📊 STEPHEN PERRENOD
   - Log-Periodic Power Law (LPPL) per Bitcoin
   - Analisi originale BTC/Oro
   - Analisi dei cicli basata sulla fisica (λ = 2.0)
   - Derivazione del vincolo ω = 2π/ln(2)
   - Substack: stephenperrenod.substack.com

📊 GIOVANNI SANTOSTASI
   - Teoria Power Law di Bitcoin
   - Analisi statistica delle dinamiche di prezzo BTC
   - YouTube: @GiovanniSantostasi
   - X/Twitter: @Giovann35084111

Implementazione, ottimizzazione delle armoniche e sviluppo 
software a cura di Snarky.

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
# CONSTANTS - Based on Santostasi Perrenod's BTC/USD analysis
# ============================================================
# For BTC/USD: λ = 2.0 (standard doubling), ω = 9.0647
# Power law from Santostasi: P = a * t^b with b ≈ 5.83

GENESIS_DATE = pd.Timestamp("2009-01-03")

# Lambda options - Standard λ = 2.0 for BTC/USD
LAMBDA_PERRENOD = 2.0   # Standard doubling for BTC/USD
LAMBDA_STANDARD = 2.0   # Standard doubling

# Default to standard value for BTC/USD
LAMBDA = LAMBDA_PERRENOD
OMEGA_LOCKED = 2 * np.pi / np.log(LAMBDA)  # ≈ 9.0647 for λ=2.0

# ============================================================
# DEFAULT SETTINGS - BTC/USD SPECIFIC
# ============================================================
# Power Law parameters from Santostasi for BTC/USD

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
    'colore_btc': '#FFD700',  # Gold/orange color for BTC
    'colore_perrenod': '#4ECDC4',
    'colore_pl': '#FF6B6B',
    # Power Law params for BTC/USD from Santostasi:
    # P = 10^-17 * t^5.83
    'pl_a_log10': -17.0,  # Santostasi BTC/USD
    'pl_b': 5.83,         # Santostasi's value for BTC/USD
    'lambda': 2.0,        # Standard lambda for BTC/USD
    'de_iter': 1000,
    'de_pop': 20,
    'de_tol': 1e-7,
    'test_split_date': '2023-01-01',
}

# Harmonics - Extended list with subharmonics
# Format: (harm_idx, name, description with lambda, days and years)
# The FUNDAMENTAL mode (harm_idx=1) corresponds to ~4 year cycle (halving cycle)
# harm_idx < 1 are SUBharmonics (longer cycles than fundamental)
# harm_idx > 1 are harmonics (shorter cycles than fundamental)
# Period calculation: T = T_fundamental / harm_idx, where T_fundamental ≈ 1460 days (~4 years)
# For λ=2.0: lambda_eff = 2^(1/harm_idx)
ALL_HARMONICS = [
    (0.25, "1/4 sub", "λ=4.00, ~5840d, ~16.00y"),
    (0.333, "1/3 sub", "λ=3.00, ~4380d, ~12.00y"),
    (0.5, "1/2 sub", "λ=2.00, ~2920d, ~8.00y"),
    (0.667, "2/3 sub", "λ=1.68, ~2190d, ~6.00y"),
    (0.75, "3/4 sub", "λ=1.54, ~1947d, ~5.33y"),
    (1, "FUND", "λ=2.00, ~1460d, ~4.00y"),
    (1.5, "3/2 harm", "λ=1.54, ~973d, ~2.67y"),
    (2, "2ª harm", "λ=1.41, ~730d, ~2.00y"),
    (3, "3ª harm", "λ=1.26, ~487d, ~1.33y"),
    (4, "4ª harm", "λ=1.19, ~365d, ~1.00y"),
    (5, "5ª harm", "λ=1.15, ~292d, ~0.80y"),
    (6, "6ª harm", "λ=1.12, ~243d, ~0.67y"),
    (7, "7ª harm", "λ=1.10, ~209d, ~0.57y"),
    (8, "8ª harm", "λ=1.09, ~182d, ~0.50y"),
]

# Presets based on Perrenod's analysis
PRESET_BEST = [1, 2]          # Fundamental + 2nd harmonic (standard)
PRESET_EFFICIENT = [1, 2]     # Fundamental + 2nd harmonic
PRESET_MINIMAL = [1]          # Just fundamental mode

# Best params for [1] harmonic - calibrated for BTC/USD
BEST_1_HARM_PARAMS = {
    'alpha': 5.83,
    'c': -38.0,
    'harmonics': {1: (80.0, -0.55, 1.0)},
    'r2_train': 0.97,
    'r2_test': 0.85,
    'r2_full': 0.97,
}

CACHE_FILE = "perrenod_usd_cache.json"
SETTINGS_FILE = "perrenod_usd_settings.json"
DATA_FILE = "btc_usd_data_full.csv"
LOG_FILE = "perrenod_usd_experiments.csv"

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
                cache = json.load(f)
                # Validate cache entries - remove invalid ones
                valid_cache = {}
                for key, value in cache.items():
                    if isinstance(value, dict) and 'params' in value and 'stats' in value:
                        valid_cache[key] = value
                return valid_cache
        except:
            pass
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=2)

def get_cache_key(harmonics, de_iter, de_pop):
    harm_str = ",".join(str(h) for h in sorted(harmonics))
    key_str = f"perrenod_usd_{harm_str}|{de_iter}|{de_pop}"
    return hashlib.md5(key_str.encode()).hexdigest()[:16]

def fetch_btc_data():
    """Fetch BTC/USD data from CryptoCompare"""
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
        if to_ts < 1279324800:  # July 2010
            break
    df = pd.DataFrame(all_data)
    df['date'] = pd.to_datetime(df['time'], unit='s')
    df = df[['date', 'close']].copy()
    df = df[df['close'] > 0].copy()
    return df

def load_btc_usd_data():
    """Load BTC/USD data"""
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE, parse_dates=['date'])
    else:
        print("Fetching BTC/USD data...")
        df = fetch_btc_data()
        
        # Save for future use
        df.to_csv(DATA_FILE, index=False)
    
    df['days'] = (df['date'] - GENESIS_DATE).dt.days
    df = df[df['days'] > 0].copy()
    return df

def fit_power_law(df):
    """Fit power law to BTC/USD data to get baseline parameters"""
    from scipy.optimize import curve_fit
    
    t = df['days'].values.astype(np.float64)
    y = np.log10(df['close'].values)
    ln_t = np.log10(t)
    
    # Linear regression in log-log space: log10(y) = b * log10(t) + log10(a)
    # => log10(y) = b * log10(t) + a_log10
    try:
        coeffs = np.polyfit(ln_t, y, 1)
        b = coeffs[0]  # slope
        a_log10 = coeffs[1]  # intercept
        return a_log10, b
    except:
        return DEFAULT_SETTINGS['pl_a_log10'], DEFAULT_SETTINGS['pl_b']

# ============================================================
# MODEL FUNCTIONS
# ============================================================

def perrenod_model(x, t, ln_t, harmonics, omega=None):
    """Perrenod LPPL model for BTC/USD
    
    Args:
        x: parameters [alpha, c, A1, beta1, phi1, A2, beta2, phi2, ...]
        t: days since genesis
        ln_t: natural log of t (precomputed for efficiency)
        harmonics: list of harmonic indices [1, 2, 3, ...]
        omega: angular frequency (if None, uses global OMEGA_LOCKED)
    """
    if omega is None:
        omega = OMEGA_LOCKED
    
    alpha = x[0]
    c = x[1]
    result = alpha * ln_t + c
    for i, harm_idx in enumerate(harmonics):
        A = x[2 + i*3]
        beta = x[3 + i*3]
        phi = x[4 + i*3]
        oscillation = A * np.power(t, beta) * np.cos(harm_idx * omega * ln_t + phi)
        result += oscillation
    return result

def make_x0_perrenod(harmonics, alpha_init=5.83, c_init=-38.0):
    """Create initial parameters - calibrated for BTC/USD
    
    Based on Santostasi's Power Law for BTC/USD:
    - alpha ≈ 5.83 (power law exponent)
    - c ≈ -38 (intercept in ln space)
    
    For t=5000 days, P=$100,000:
    ln(100000) = 11.5 = 5.83 * ln(5000) + c
    c = 11.5 - 5.83 * 8.52 = 11.5 - 49.7 ≈ -38
    """
    n_harm = len(harmonics)
    x = np.zeros(2 + n_harm * 3)
    x[0] = alpha_init
    x[1] = c_init
    for i, harm_idx in enumerate(harmonics):
        if harm_idx == 1:
            # Fundamental mode - strongest
            x[2 + i*3] = 80.0     # Amplitude
            x[3 + i*3] = -0.55    # Beta (moderate decay)
            x[4 + i*3] = 1.0      # Phase
        elif harm_idx == 2:
            # First harmonic (half-harmonic) - 2021 bubble
            x[2 + i*3] = 40.0
            x[3 + i*3] = -0.50
            x[4 + i*3] = 2.0
        elif harm_idx < 1:  # Subharmonics
            x[2 + i*3] = 50.0
            x[3 + i*3] = -0.45
            x[4 + i*3] = 0.5
        else:  # Higher harmonics (3, 4, 5, ...)
            x[2 + i*3] = 30.0 / harm_idx
            x[3 + i*3] = -0.50
            x[4 + i*3] = 0.0
    return x

def make_bounds_perrenod(n_harm):
    """Parameter bounds - calibrated for BTC/USD based on Santostasi's work
    
    Key insights:
    - Power law index k ≈ 5.5-6.2 for BTC/USD
    - c intercept around -42 to -34 in ln space
    """
    bounds = [(5.5, 6.2), (-42, -34)]  # alpha, c (adjusted for BTC/USD)
    for _ in range(n_harm):
        bounds.extend([
            (1.0, 200.0),     # A: amplitude
            (-0.75, -0.20),   # beta: decay rate (not too extreme)
            (0, 2*np.pi)      # phi: phase
        ])
    return bounds

def power_law(t, a_log10, b):
    a = 10 ** a_log10
    return a * np.power(t, b)

# ============================================================
# MAIN CLASS
# ============================================================

class PerrenodGoldExplorer:
    def __init__(self, root):
        self.root = root
        self.settings = load_settings()
        self.cache = load_cache()
        self.lang = self.settings.get('language', 'en')
        self.tr = TRANSLATIONS[self.lang]
        
        # Calculate omega from lambda setting
        self.lambda_val = self.settings.get('lambda', LAMBDA_PERRENOD)
        self.omega = 2 * np.pi / np.log(self.lambda_val)
        
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
            self.df = load_btc_usd_data()
            self.today_days = self.df['days'].max()
            self.today_date = self.df['date'].max()
            
            # Fit power law to get baseline parameters for BTC/USD
            pl_a_log10, pl_b = fit_power_law(self.df)
            self.settings['pl_a_log10'] = pl_a_log10
            self.settings['pl_b'] = pl_b
            print(f"Fitted Power Law for BTC/USD: a_log10={pl_a_log10:.4f}, b={pl_b:.4f}")
            
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
        
        omega_label = ttk.Label(toolbar, text=f"λ={self.lambda_val:.2f} ω={self.omega:.4f}", 
                                font=('Arial', 10, 'bold'))
        omega_label.pack(side=tk.LEFT, padx=10)
        
        # BTC/USD indicator
        usd_label = ttk.Label(toolbar, text="💵 BTC/USD", 
                               font=('Arial', 10, 'bold'), foreground='#FFD700')
        usd_label.pack(side=tk.LEFT, padx=10)
        
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
        ttk.Label(info_frame, text="P = BTC/USD", font=('Arial', 8, 'bold'), 
                  foreground='#FFD700').pack(anchor=tk.W, pady=(5,0))
        
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
        
        # Custom harmonics - after fixed harmonics in the scrollable list
        ttk.Separator(harm_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        ttk.Label(harm_frame, text=self.t('custom_harm'), font=('Arial', 8, 'bold')).pack(anchor=tk.W)
        
        # Custom Harmonic 1
        custom1_frame = ttk.Frame(harm_frame)
        custom1_frame.pack(fill=tk.X, pady=2)
        
        self.custom_harm1_enabled = tk.BooleanVar(value=False)
        self.custom_harm1_cb = ttk.Checkbutton(custom1_frame, variable=self.custom_harm1_enabled)
        self.custom_harm1_cb.pack(side=tk.LEFT)
        
        ttk.Label(custom1_frame, text="C1:", font=('Arial', 8)).pack(side=tk.LEFT)
        self.custom_harm1_var = tk.StringVar(value="")
        self.custom_harm1_var.trace('w', lambda *args: self.update_custom_label(1))
        self.custom_harm1_entry = ttk.Entry(custom1_frame, textvariable=self.custom_harm1_var, width=5)
        self.custom_harm1_entry.pack(side=tk.LEFT, padx=2)
        
        self.custom_harm1_label = ttk.Label(custom1_frame, text="", font=('Arial', 7))
        self.custom_harm1_label.pack(side=tk.LEFT, padx=2)
        
        # Custom Harmonic 2
        custom2_frame = ttk.Frame(harm_frame)
        custom2_frame.pack(fill=tk.X, pady=2)
        
        self.custom_harm2_enabled = tk.BooleanVar(value=False)
        self.custom_harm2_cb = ttk.Checkbutton(custom2_frame, variable=self.custom_harm2_enabled)
        self.custom_harm2_cb.pack(side=tk.LEFT)
        
        ttk.Label(custom2_frame, text="C2:", font=('Arial', 8)).pack(side=tk.LEFT)
        self.custom_harm2_var = tk.StringVar(value="")
        self.custom_harm2_var.trace('w', lambda *args: self.update_custom_label(2))
        self.custom_harm2_entry = ttk.Entry(custom2_frame, textvariable=self.custom_harm2_var, width=5)
        self.custom_harm2_entry.pack(side=tk.LEFT, padx=2)
        
        self.custom_harm2_label = ttk.Label(custom2_frame, text="", font=('Arial', 7))
        self.custom_harm2_label.pack(side=tk.LEFT, padx=2)
        
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
        
        # ============ RIGHT PANEL with TABS ============
        right_frame = ttk.Frame(main_container)
        main_container.add(right_frame, weight=1)
        
        # Create notebook for tabs
        self.main_notebook = ttk.Notebook(right_frame)
        self.main_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Main plots
        main_tab = ttk.Frame(self.main_notebook)
        self.main_notebook.add(main_tab, text="📈 Main")
        
        # Create horizontal paned window: plots on left, stats on right
        plot_stats_pane = ttk.PanedWindow(main_tab, orient=tk.HORIZONTAL)
        plot_stats_pane.pack(fill=tk.BOTH, expand=True)
        
        # Left side: plots
        plot_frame = ttk.Frame(plot_stats_pane)
        plot_stats_pane.add(plot_frame, weight=4)
        
        self.fig = Figure(figsize=(10, 8), facecolor='#1a1a2e')
        self.axes = self.fig.subplots(2, 2)
        
        for ax in self.axes.flat:
            ax.set_facecolor('#1a1a2e')
            ax.tick_params(colors='white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.title.set_color('white')
            for spine in ax.spines.values():
                spine.set_color('white')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Right side: statistics panel
        stats_frame = ttk.Frame(plot_stats_pane, width=220)
        plot_stats_pane.add(stats_frame, weight=1)
        
        # Stats text widget with scrollbar
        stats_container = ttk.Frame(stats_frame)
        stats_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        stats_scrollbar = ttk.Scrollbar(stats_container)
        stats_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.stats_text_widget = tk.Text(stats_container, 
                                          wrap=tk.WORD, 
                                          font=('Consolas', 9),
                                          bg='#1a1a2e', 
                                          fg='white',
                                          width=28,
                                          yscrollcommand=stats_scrollbar.set)
        self.stats_text_widget.pack(fill=tk.BOTH, expand=True)
        stats_scrollbar.config(command=self.stats_text_widget.yview)
        
        # Tab 2: Spectral Analysis
        spectral_tab = ttk.Frame(self.main_notebook)
        self.main_notebook.add(spectral_tab, text=self.t('spectral_tab'))
        
        # Spectral tab layout: plots on left, stats on right
        spectral_pane = ttk.PanedWindow(spectral_tab, orient=tk.HORIZONTAL)
        spectral_pane.pack(fill=tk.BOTH, expand=True)
        
        # Left: spectral plots
        spectral_plot_frame = ttk.Frame(spectral_pane)
        spectral_pane.add(spectral_plot_frame, weight=4)
        
        self.fig_spectral = Figure(figsize=(10, 8), facecolor='#1a1a2e')
        self.axes_spectral = self.fig_spectral.subplots(2, 2)
        
        for ax in self.axes_spectral.flat:
            ax.set_facecolor('#1a1a2e')
            ax.tick_params(colors='white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.title.set_color('white')
            for spine in ax.spines.values():
                spine.set_color('white')
        
        self.canvas_spectral = FigureCanvasTkAgg(self.fig_spectral, master=spectral_plot_frame)
        self.canvas_spectral.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Right: spectral stats
        spectral_stats_frame = ttk.Frame(spectral_pane, width=250)
        spectral_pane.add(spectral_stats_frame, weight=1)
        
        spectral_stats_container = ttk.Frame(spectral_stats_frame)
        spectral_stats_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        spectral_scrollbar = ttk.Scrollbar(spectral_stats_container)
        spectral_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.spectral_text_widget = tk.Text(spectral_stats_container,
                                             wrap=tk.WORD,
                                             font=('Consolas', 9),
                                             bg='#1a1a2e',
                                             fg='white',
                                             width=32,
                                             yscrollcommand=spectral_scrollbar.set)
        self.spectral_text_widget.pack(fill=tk.BOTH, expand=True)
        spectral_scrollbar.config(command=self.spectral_text_widget.yview)
        
        # Tab 3: Wavelet Analysis
        wavelet_tab = ttk.Frame(self.main_notebook)
        self.main_notebook.add(wavelet_tab, text="🌊 Wavelet")
        
        # Wavelet tab layout: plots on left, stats on right
        wavelet_pane = ttk.PanedWindow(wavelet_tab, orient=tk.HORIZONTAL)
        wavelet_pane.pack(fill=tk.BOTH, expand=True)
        
        # Left: wavelet plots
        wavelet_plot_frame = ttk.Frame(wavelet_pane)
        wavelet_pane.add(wavelet_plot_frame, weight=4)
        
        self.fig_wavelet = Figure(figsize=(10, 8), facecolor='#1a1a2e')
        self.axes_wavelet = self.fig_wavelet.subplots(2, 2)
        
        for ax in self.axes_wavelet.flat:
            ax.set_facecolor('#1a1a2e')
            ax.tick_params(colors='white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.title.set_color('white')
            for spine in ax.spines.values():
                spine.set_color('white')
        
        self.canvas_wavelet = FigureCanvasTkAgg(self.fig_wavelet, master=wavelet_plot_frame)
        self.canvas_wavelet.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Right: wavelet stats
        wavelet_stats_frame = ttk.Frame(wavelet_pane, width=250)
        wavelet_pane.add(wavelet_stats_frame, weight=1)
        
        wavelet_stats_container = ttk.Frame(wavelet_stats_frame)
        wavelet_stats_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        wavelet_scrollbar = ttk.Scrollbar(wavelet_stats_container)
        wavelet_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.wavelet_text_widget = tk.Text(wavelet_stats_container,
                                            wrap=tk.WORD,
                                            font=('Consolas', 9),
                                            bg='#1a1a2e',
                                            fg='white',
                                            width=32,
                                            yscrollcommand=wavelet_scrollbar.set)
        self.wavelet_text_widget.pack(fill=tk.BOTH, expand=True)
        wavelet_scrollbar.config(command=self.wavelet_text_widget.yview)
        
        self.fig.tight_layout()
        self.fig_spectral.tight_layout()
        self.fig_wavelet.tight_layout()
    
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
        harmonics = [h for h, var in self.harm_vars.items() if var.get()]
        
        # Add custom harmonics if enabled
        try:
            if self.custom_harm1_enabled.get():
                custom1 = self.custom_harm1_var.get().strip()
                if custom1:
                    val = float(custom1)
                    if val > 0 and val not in harmonics:
                        harmonics.append(val)
        except:
            pass
        
        try:
            if self.custom_harm2_enabled.get():
                custom2 = self.custom_harm2_var.get().strip()
                if custom2:
                    val = float(custom2)
                    if val > 0 and val not in harmonics:
                        harmonics.append(val)
        except:
            pass
        
        return sorted(harmonics)
    
    def update_custom_label(self, which):
        """Update the label showing lambda, days and years for custom harmonic"""
        try:
            if which == 1:
                val_str = self.custom_harm1_var.get().strip()
                label = self.custom_harm1_label
            else:
                val_str = self.custom_harm2_var.get().strip()
                label = self.custom_harm2_label
            
            if val_str:
                h = float(val_str)
                if h > 0:
                    # Calculate lambda for this harmonic
                    lam_h = np.exp(2 * np.pi / (h * self.omega))
                    # Period: T = T_fundamental / harm_idx, T_fundamental ≈ 1460 days (~4 years)
                    days = int(1460 / h)
                    years = days / 365.25
                    label.config(text=f"λ={lam_h:.2f}, ~{days}d, ~{years:.2f}y")
                else:
                    label.config(text="")
            else:
                label.config(text="")
        except:
            if which == 1:
                self.custom_harm1_label.config(text="")
            else:
                self.custom_harm2_label.config(text="")
    
    def flash_button(self, button, color='#00ff00'):
        """Flash button to indicate action"""
        original_style = button.cget('style')
        style = ttk.Style()
        style.configure('Flash.TButton', background=color)
        button.configure(style='Flash.TButton')
        self.root.after(200, lambda: button.configure(style=original_style if original_style else 'TButton'))
    
    def copy_results(self):
        """Copy results to clipboard - content depends on active tab"""
        active_tab = self.main_notebook.index(self.main_notebook.select())
        
        if active_tab == 0:
            # Main tab - copy model results
            text = self._get_main_results_text()
        elif active_tab == 1:
            # Spectral tab - copy spectral statistics
            text = self._get_spectral_results_text()
        else:
            # Wavelet tab - copy wavelet statistics
            text = self._get_wavelet_results_text()
        
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()
        
        self.flash_button(self.btn_copy_text)
        self.status_var.set(self.t('copied_text'))
    
    def _get_main_results_text(self):
        """Get text for Main tab results"""
        harmonics = self.get_selected_harmonics()
        de_iter = int(self.de_iter_var.get())
        de_pop = int(self.de_pop_var.get())
        
        text = "=" * 50 + "\n"
        text += "PERRENOD GOLD WAVE EXPLORER - BTC/GOLD RESULTS\n"
        text += "=" * 50 + "\n\n"
        
        text += f"λ = {self.lambda_val:.4f} (Perrenod BTC/USD)\n"
        text += f"ω = {self.omega:.6f}\n"
        text += f"Asset: BTC/USD\n\n"
        
        text += f"Harmonics: {harmonics}\n"
        text += f"N parameters: {2 + len(harmonics)*3}\n\n"
        
        text += f"DE PARAMETERS:\n"
        text += f"  Iterations: {de_iter}\n"
        text += f"  Population: {de_pop}\n\n"
        
        if self.current_stats:
            s = self.current_stats
            text += "PERFORMANCE:\n"
            text += f"  R2 train: {s['r2_train']:.4f}\n"
            text += f"  R2 test (OOS):  {s['r2_test']:.4f}\n"
            if 'r2_test_std' in s:
                text += f"  R2 test (std):  {s['r2_test_std']:.4f}\n"
            text += f"  R2 full:  {s['r2_full']:.4f}\n"
            if 'mae_test' in s:
                text += f"  MAE test: {s['mae_test']:.4f}\n"
            if 'bias_test' in s:
                text += f"  Bias test: {s['bias_test']:.4f}\n"
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
                days = int(1460 / harm_idx)  # T_fundamental = 1460d (~4 years)
                years = days / 365.25
                text += f"  Harm {harm_idx}: A={A:.4f}, β={beta:.4f}, φ={phi:.4f} (λ={lambda_eff:.3f}, ~{days}d, ~{years:.2f}y)\n"
            
            text += f"\nRAW PARAMS: {self.current_params.tolist()}\n"
        
        text += "\n" + "=" * 50
        return text
    
    def _get_spectral_results_text(self):
        """Get text for Spectral tab results"""
        text = "=" * 50 + "\n"
        text += "PERRENOD GOLD WAVE EXPLORER - SPECTRAL ANALYSIS\n"
        text += "=" * 50 + "\n\n"
        
        text += f"λ = {self.lambda_val:.4f}\n"
        text += f"ω = {self.omega:.6f}\n"
        text += f"Harmonics: {self.get_selected_harmonics()}\n\n"
        
        if self.current_params is not None:
            harmonics = self.get_selected_harmonics()
            x = self.current_params
            
            # Calculate residuals
            y_fit = perrenod_model(x, self.t_full, self.ln_t_full, harmonics, self.omega)
            residuals = self.y_full - y_fit
            
            text += "RESIDUALS STATISTICS:\n"
            text += f"  Mean:     {np.mean(residuals):.6f}\n"
            text += f"  Std:      {np.std(residuals):.6f}\n"
            text += f"  Min:      {np.min(residuals):.4f}\n"
            text += f"  Max:      {np.max(residuals):.4f}\n"
            text += f"  Skewness: {skew(residuals):.4f}\n"
            text += f"  Kurtosis: {kurtosis(residuals):.4f}\n\n"
            
            # Durbin-Watson
            diff = np.diff(residuals)
            dw = np.sum(diff**2) / np.sum(residuals**2)
            text += "DIAGNOSTICS:\n"
            text += f"  Durbin-Watson: {dw:.4f}\n"
            text += f"  (2.0 = no autocorrelation)\n\n"
            
            # FFT peaks
            N = len(residuals)
            residuals_detrend = residuals - np.mean(residuals)
            fft_vals = fft(residuals_detrend)
            freqs = fftfreq(N, 1)
            
            pos_mask = freqs > 0
            power = np.abs(fft_vals[pos_mask])**2 / N
            periods = 1 / freqs[pos_mask]
            
            try:
                peaks_idx, _ = find_peaks(power, height=np.percentile(power, 90), distance=10)
                peak_periods = periods[peaks_idx]
                peak_power = power[peaks_idx]
                sort_idx = np.argsort(peak_power)[::-1][:10]
                
                text += "TOP PERIODIC SIGNALS (FFT):\n"
                for i, idx in enumerate(sort_idx):
                    p = peak_periods[idx]
                    pw = peak_power[idx]
                    text += f"  {i+1}. {p:.0f}d ({p/365.25:.2f}y) - Power: {pw:.2e}\n"
            except:
                pass
        
        text += "\n" + "=" * 50
        return text
    
    def _get_wavelet_results_text(self):
        """Get text for Wavelet tab results"""
        text = "=" * 50 + "\n"
        text += "PERRENOD GOLD WAVE EXPLORER - WAVELET ANALYSIS\n"
        text += "=" * 50 + "\n\n"
        
        text += f"λ = {self.lambda_val:.4f}\n"
        text += f"ω = {self.omega:.6f}\n"
        text += f"Harmonics: {self.get_selected_harmonics()}\n\n"
        
        if self.current_params is not None:
            harmonics = self.get_selected_harmonics()
            x = self.current_params
            
            # Calculate residuals
            y_fit = perrenod_model(x, self.t_full, self.ln_t_full, harmonics, self.omega)
            residuals = self.y_full - y_fit
            
            # Bubble analysis
            threshold = np.percentile(residuals, 95)
            bubble_mask = residuals > threshold
            n_bubble_days = bubble_mask.sum()
            
            text += "BUBBLE ANALYSIS:\n"
            text += f"  Threshold (95th percentile): {threshold:.4f}\n"
            text += f"  Bubble days: {n_bubble_days}\n"
            text += f"  Bubble percentage: {100*n_bubble_days/len(residuals):.1f}%\n\n"
            
            # Find bubble periods
            if n_bubble_days > 0:
                dates = self.df['date'].values
                bubble_idx = np.where(bubble_mask)[0]
                
                if len(bubble_idx) > 0:
                    clusters = []
                    start = bubble_idx[0]
                    end = bubble_idx[0]
                    
                    for idx in bubble_idx[1:]:
                        if idx - end <= 30:
                            end = idx
                        else:
                            clusters.append((start, end))
                            start = idx
                            end = idx
                    clusters.append((start, end))
                    
                    text += "BUBBLE PERIODS:\n"
                    for i, (s, e) in enumerate(clusters):
                        d1 = pd.Timestamp(dates[s]).strftime('%Y-%m-%d')
                        d2 = pd.Timestamp(dates[e]).strftime('%Y-%m-%d')
                        duration = e - s + 1
                        text += f"  {i+1}. {d1} to {d2} ({duration} days)\n"
            
            text += f"\nLPPL PARAMETERS:\n"
            text += f"  λ (scale ratio): {self.lambda_val:.4f}\n"
            text += f"  ω (angular freq): {self.omega:.4f}\n"
            text += f"  Cycle period: ~{np.log(self.lambda_val)*365:.0f} days\n"
        
        text += "\n" + "=" * 50
        return text
    
    def copy_graph(self):
        """Copy graph to clipboard - works with active tab"""
        try:
            # Determine which figure to copy based on active tab
            active_tab = self.main_notebook.index(self.main_notebook.select())
            
            if active_tab == 0:
                fig = self.fig
                prefix = "perrenod_usd_graph"
            elif active_tab == 1:
                fig = self.fig_spectral
                prefix = "perrenod_usd_spectral"
            else:
                fig = self.fig_wavelet
                prefix = "perrenod_usd_wavelet"
            
            # Save figure to bytes
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=150, facecolor='#1a1a2e', bbox_inches='tight')
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
            active_tab = self.main_notebook.index(self.main_notebook.select())
            if active_tab == 0:
                fig = self.fig
                prefix = "perrenod_usd_graph"
            elif active_tab == 1:
                fig = self.fig_spectral
                prefix = "perrenod_usd_spectral"
            else:
                fig = self.fig_wavelet
                prefix = "perrenod_usd_wavelet"
                
            filename = f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            fig.savefig(filename, dpi=150, facecolor='#1a1a2e', bbox_inches='tight')
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
        self.status_var.set(f"🏆 Perrenod [1,2] - Fundamental + Half-harmonic")
    
    def select_efficient(self):
        for h, var in self.harm_vars.items():
            var.set(h in PRESET_EFFICIENT)
        self.status_var.set(f"[1] - Fundamental only")
    
    def select_minimal(self):
        for h, var in self.harm_vars.items():
            var.set(h in PRESET_MINIMAL)
        # Load default params for BTC/USD
        p = BEST_1_HARM_PARAMS
        harm_params = p['harmonics'][1]
        self.current_params = np.array([p['alpha'], p['c'], harm_params[0], harm_params[1], harm_params[2]])
        self.current_stats = None  # Will be calculated on draw
        self.status_var.set(f"[1] - Default params for BTC/USD")
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
        
        # Check if cache entry is valid
        if cache_key in self.cache and 'params' in self.cache[cache_key]:
            self.current_params = np.array(self.cache[cache_key]['params'])
            self.current_stats = self.cache[cache_key].get('stats')
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
        
        # Check if cache entry is valid
        if cache_key in self.cache and 'params' in self.cache[cache_key]:
            self.current_params = np.array(self.cache[cache_key]['params'])
            self.current_stats = self.cache[cache_key].get('stats')
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
                    y_pred = perrenod_model(x, self.t_train, self.ln_t_train, harmonics, self.omega)
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
        
        # Train stats
        y_pred_train = perrenod_model(x, self.t_train, self.ln_t_train, harmonics, self.omega)
        ss_res_train = np.sum((self.y_train - y_pred_train)**2)
        r2_train = 1 - ss_res_train / self.ss_tot_train
        bic_train = self.n_train * np.log(ss_res_train / self.n_train) + n_params * np.log(self.n_train)
        
        # Test stats - use train mean as reference for proper out-of-sample R2
        y_pred_test = perrenod_model(x, self.t_test, self.ln_t_test, harmonics, self.omega)
        ss_res_test = np.sum((self.y_test - y_pred_test)**2)
        
        # R2 test standard (vs test mean) - can be negative if test has low variance
        r2_test_std = 1 - ss_res_test / self.ss_tot_test
        
        # R2 test out-of-sample (vs train mean) - more appropriate
        ss_tot_test_oos = np.sum((self.y_test - np.mean(self.y_train))**2)
        r2_test_oos = 1 - ss_res_test / ss_tot_test_oos
        
        # Additional metrics
        mae_test = np.mean(np.abs(self.y_test - y_pred_test))
        bias_test = np.mean(self.y_test - y_pred_test)
        
        # Full stats
        y_pred_full = perrenod_model(x, self.t_full, self.ln_t_full, harmonics, self.omega)
        ss_res_full = np.sum((self.y_full - y_pred_full)**2)
        r2_full = 1 - ss_res_full / self.ss_tot_full
        
        pl_a = 10 ** self.settings['pl_a_log10']
        pl_b = self.settings['pl_b']
        
        ratios = {}
        for years in [10, 25, 50]:
            fd = self.today_days + years * 365.25
            p_perrenod = np.exp(perrenod_model(x, np.array([fd]), np.log(np.array([fd])), harmonics, self.omega))[0]
            p_pl = pl_a * (fd ** pl_b)
            ratios[years] = p_perrenod / p_pl
        
        return {
            'r2_train': float(r2_train), 
            'r2_test': float(r2_test_oos),  # Use out-of-sample R2
            'r2_test_std': float(r2_test_std),  # Keep standard for reference
            'r2_full': float(r2_full),
            'mae_test': float(mae_test),
            'bias_test': float(bias_test),
            'bic': float(bic_train), 'n_params': n_params, 'n_harm': n_harm,
            'ratio_10y': float(ratios[10]), 'ratio_25y': float(ratios[25]), 'ratio_50y': float(ratios[50]),
            'alpha': float(x[0]), 'c': float(x[1]),
        }
    
    def _fit_complete(self):
        self.is_fitting = False
        self.status_var.set(self.t('fit_complete'))
        self.cache_label.config(text=f"{self.t('cache')}: {len(self.cache)}")
        
        # Log the experiment
        self.log_experiment()
        
        self.update_plots()
    
    def log_experiment(self):
        """Log experiment results to CSV file with comprehensive data"""
        if self.current_params is None or self.current_stats is None:
            return
        
        harmonics = self.get_selected_harmonics()
        s = self.current_stats
        x = self.current_params
        
        # Calculate residuals for additional stats
        y_fit = perrenod_model(x, self.t_full, self.ln_t_full, harmonics, self.omega)
        residuals = self.y_full - y_fit
        
        # Durbin-Watson
        diff = np.diff(residuals)
        dw = np.sum(diff**2) / np.sum(residuals**2) if np.sum(residuals**2) > 0 else 0
        
        # Residual statistics
        res_mean = np.mean(residuals)
        res_std = np.std(residuals)
        res_min = np.min(residuals)
        res_max = np.max(residuals)
        res_skew = skew(residuals)
        res_kurt = kurtosis(residuals)
        
        # Calculate projections at specific dates
        def calc_projection(years_ahead):
            fd = self.today_days + years_ahead * 365.25
            return np.exp(perrenod_model(x, np.array([fd]), np.log(np.array([fd])), harmonics, self.omega))[0]
        
        # Current model value
        current_model = np.exp(perrenod_model(x, np.array([self.today_days]), np.log(np.array([self.today_days])), harmonics, self.omega))[0]
        
        # Prepare row data
        row = {
            # Metadata
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'run_id': hashlib.md5(f"{datetime.now().isoformat()}{harmonics}".encode()).hexdigest()[:8],
            
            # Model parameters
            'lambda': self.lambda_val,
            'omega': self.omega,
            'harmonics': str(harmonics).replace(',', ';'),  # Use semicolon to avoid CSV issues
            'n_harmonics': len(harmonics),
            'n_params': s['n_params'],
            
            # Optimization settings
            'de_iter': self.current_de_iter,
            'de_pop': self.current_de_pop,
            'de_tol': self.settings.get('de_tol', 0.01),
            
            # Dataset info
            'n_train': self.n_train,
            'n_test': self.n_test,
            'n_total': len(self.df),
            'train_start': self.df['date'].iloc[0].strftime('%Y-%m-%d'),
            'train_end': self.df['date'].iloc[self.n_train-1].strftime('%Y-%m-%d'),
            'test_start': self.df['date'].iloc[self.n_train].strftime('%Y-%m-%d'),
            'test_end': self.df['date'].iloc[-1].strftime('%Y-%m-%d'),
            
            # Performance metrics
            'r2_train': round(s['r2_train'], 6),
            'r2_test_oos': round(s['r2_test'], 6),
            'r2_test_std': round(s.get('r2_test_std', 0), 6),
            'r2_full': round(s['r2_full'], 6),
            'mae_test': round(s.get('mae_test', 0), 6),
            'bias_test': round(s.get('bias_test', 0), 6),
            'bic': round(s['bic'], 2),
            'aic': round(s['bic'] - s['n_params'] * (np.log(self.n_train) - 2), 2),  # Approximate AIC
            
            # Residual diagnostics
            'durbin_watson': round(dw, 6),
            'res_mean': round(res_mean, 6),
            'res_std': round(res_std, 6),
            'res_min': round(res_min, 4),
            'res_max': round(res_max, 4),
            'res_skewness': round(res_skew, 4),
            'res_kurtosis': round(res_kurt, 4),
            
            # Projections vs Power Law
            'ratio_10y': round(s['ratio_10y'], 4),
            'ratio_25y': round(s['ratio_25y'], 4),
            'ratio_50y': round(s['ratio_50y'], 4),
            
            # Absolute projections (BTC/USD oz)
            'current_model_value': round(current_model, 4),
            'proj_1y': round(calc_projection(1), 4),
            'proj_2y': round(calc_projection(2), 4),
            'proj_5y': round(calc_projection(5), 4),
            'proj_10y': round(calc_projection(10), 4),
            
            # Base parameters
            'alpha': round(s['alpha'], 6),
            'c': round(s['c'], 6),
        }
        
        # Add harmonic parameters
        for i, h in enumerate(harmonics):
            A = x[2 + i*3]
            beta = x[3 + i*3]
            phi = x[4 + i*3]
            omega_eff = h * self.omega
            lambda_eff = np.exp(2 * np.pi / omega_eff)
            days = int(1460 / h)
            years = round(days / 365.25, 2)
            
            row[f'harm_{i+1}_idx'] = h
            row[f'harm_{i+1}_A'] = round(A, 6)
            row[f'harm_{i+1}_beta'] = round(beta, 6)
            row[f'harm_{i+1}_phi'] = round(phi, 6)
            row[f'harm_{i+1}_lambda'] = round(lambda_eff, 4)
            row[f'harm_{i+1}_days'] = days
            row[f'harm_{i+1}_years'] = years
        
        # Add raw params (with semicolons instead of commas)
        raw_str = ';'.join([f"{p:.8f}" for p in x.tolist()])
        row['raw_params'] = raw_str
        
        # Check if file exists to determine if we need header
        file_exists = os.path.exists(LOG_FILE)
        
        # Get all possible columns (for consistent structure)
        base_columns = [
            'timestamp', 'run_id',
            'lambda', 'omega', 'harmonics', 'n_harmonics', 'n_params',
            'de_iter', 'de_pop', 'de_tol',
            'n_train', 'n_test', 'n_total', 'train_start', 'train_end', 'test_start', 'test_end',
            'r2_train', 'r2_test_oos', 'r2_test_std', 'r2_full',
            'mae_test', 'bias_test', 'bic', 'aic',
            'durbin_watson', 'res_mean', 'res_std', 'res_min', 'res_max', 'res_skewness', 'res_kurtosis',
            'ratio_10y', 'ratio_25y', 'ratio_50y',
            'current_model_value', 'proj_1y', 'proj_2y', 'proj_5y', 'proj_10y',
            'alpha', 'c'
        ]
        
        # Add harmonic columns (support up to 10 harmonics)
        harm_columns = []
        for i in range(1, 11):
            harm_columns.extend([
                f'harm_{i}_idx', f'harm_{i}_A', f'harm_{i}_beta', 
                f'harm_{i}_phi', f'harm_{i}_lambda', f'harm_{i}_days', f'harm_{i}_years'
            ])
        
        all_columns = base_columns + harm_columns + ['raw_params']
        
        # Write to CSV with proper quoting
        try:
            with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=all_columns, extrasaction='ignore',
                                       quoting=csv.QUOTE_MINIMAL)
                
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow(row)
            
            self.status_var.set(f"{self.t('fit_complete')} - Logged to {LOG_FILE}")
        except Exception as e:
            print(f"Error logging experiment: {e}")
    
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
        
        # Check if cache entry is valid
        if cache_key in self.cache and 'params' in self.cache[cache_key]:
            self.current_params = np.array(self.cache[cache_key]['params'])
            self.current_stats = self.cache[cache_key].get('stats')
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
        
        # Calculate stats if not present
        if self.current_stats is None:
            self.current_stats = self._calc_stats(self.current_params, harmonics)
        
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
        
        # Plot 1: Historical BTC/USD
        ax1 = self.axes[0, 0]
        ax1.semilogy(self.df['date'], self.df['close'], color=col_btc, alpha=0.6, lw=0.8, label='BTC/USD')
        y_fit = perrenod_model(x, self.t_full, self.ln_t_full, harmonics, self.omega)
        ax1.semilogy(self.df['date'], np.exp(y_fit), color=col_perrenod, lw=2, label='Perrenod')
        if self.settings['mostra_power_law']:
            y_pl = power_law(self.t_full, self.settings['pl_a_log10'], pl_b)
            ax1.semilogy(self.df['date'], y_pl, color=col_pl, lw=1.5, ls='--', label='Power Law')
        ax1.axvline(pd.Timestamp(self.settings['test_split_date']), color='yellow', ls='--', alpha=0.7)
        ax1.set_title(self.t('historical'), color='white', fontweight='bold')
        ax1.set_ylabel('BTC/USD ($)', color='white')
        ax1.legend(loc='upper left', fontsize=8)
        # Add minor grid for better price reading
        ax1.grid(True, which='major', alpha=0.3)
        ax1.grid(True, which='minor', alpha=0.1, linestyle=':')
        ax1.minorticks_on()
        
        # Plot 2: Zoom + projection
        ax2 = self.axes[0, 1]
        zoom_anni = self.settings['zoom_anni']
        proj_breve = self.settings['proiezione_breve']
        start_date = self.today_date - pd.Timedelta(days=zoom_anni*365)
        df_zoom = self.df[self.df['date'] >= start_date]
        ax2.semilogy(df_zoom['date'], df_zoom['close'], color=col_btc, alpha=0.8, lw=1, label='BTC/USD')
        end_days = self.today_days + proj_breve * 365.25
        proj_days = np.linspace(df_zoom['days'].min(), end_days, 500)
        proj_dates = pd.to_datetime(GENESIS_DATE) + pd.to_timedelta(proj_days, unit='D')
        y_proj = perrenod_model(x, proj_days, np.log(proj_days), harmonics, self.omega)
        ax2.semilogy(proj_dates, np.exp(y_proj), color=col_perrenod, lw=2, label='Perrenod')
        if self.settings['mostra_power_law']:
            y_pl = power_law(proj_days, self.settings['pl_a_log10'], pl_b)
            ax2.semilogy(proj_dates, y_pl, color=col_pl, lw=1.5, ls='--', label='Power Law')
        ax2.axvline(self.today_date, color='yellow', ls=':', alpha=0.8)
        ax2.set_title(f"{self.t('zoom_proj')} ({zoom_anni}y + {proj_breve}y)", color='white', fontweight='bold')
        ax2.set_ylabel('BTC/USD ($)', color='white')
        ax2.legend(loc='upper left', fontsize=8)
        # Add minor grid for better price reading
        ax2.grid(True, which='major', alpha=0.3)
        ax2.grid(True, which='minor', alpha=0.1, linestyle=':')
        ax2.minorticks_on()
        
        # Plot 3: Long projection
        ax3 = self.axes[1, 0]
        proj_lunga = self.settings['proiezione_lunga']
        end_days = self.today_days + proj_lunga * 365.25
        proj_days = np.linspace(365, end_days, 1000)
        proj_dates = pd.to_datetime(GENESIS_DATE) + pd.to_timedelta(proj_days, unit='D')
        ax3.semilogy(self.df['date'], self.df['close'], color=col_btc, alpha=0.3, lw=0.5)
        y_proj = perrenod_model(x, proj_days, np.log(proj_days), harmonics, self.omega)
        y_proj_exp = np.exp(y_proj)
        ax3.semilogy(proj_dates, y_proj_exp, color=col_perrenod, lw=2, label='Perrenod')
        if self.settings['mostra_power_law']:
            y_pl = power_law(proj_days, self.settings['pl_a_log10'], pl_b)
            ax3.semilogy(proj_dates, y_pl, color=col_pl, lw=1.5, ls='--', label='Power Law')
        ax3.axvline(self.today_date, color='yellow', ls=':', alpha=0.8)
        ax3.set_title(f"{self.t('long_proj')} ({proj_lunga} {self.t('years')})", color='white', fontweight='bold')
        ax3.set_ylabel('BTC/USD ($)', color='white')
        ax3.legend(loc='upper left', fontsize=8)
        # Dynamic ylim based on projection max
        y_max = max(y_proj_exp.max(), y_pl.max() if self.settings['mostra_power_law'] else y_proj_exp.max())
        y_min = min(self.df['close'].min(), 0.01)
        ax3.set_ylim(y_min, y_max * 2)
        # Add minor grid for better price reading
        ax3.grid(True, which='major', alpha=0.3)
        ax3.grid(True, which='minor', alpha=0.1, linestyle=':')
        ax3.minorticks_on()
        
        # Plot 4: Residuals
        ax4 = self.axes[1, 1]
        
        # Calculate residuals for full dataset
        y_fit_full = perrenod_model(x, self.t_full, self.ln_t_full, harmonics, self.omega)
        residuals = self.y_full - y_fit_full
        
        # Plot residuals
        ax4.axhline(0, color='#FF6B6B', ls='--', lw=1, alpha=0.8)
        ax4.fill_between(self.df['date'], residuals, 0, 
                         where=(residuals >= 0), color='#4ECDC4', alpha=0.4, label='Above model')
        ax4.fill_between(self.df['date'], residuals, 0, 
                         where=(residuals < 0), color='#FF6B6B', alpha=0.4, label='Below model')
        ax4.plot(self.df['date'], residuals, color='white', lw=0.5, alpha=0.7)
        
        # Mark train/test split
        split_date = pd.Timestamp(self.settings['test_split_date'])
        ax4.axvline(split_date, color='yellow', ls=':', alpha=0.8, label='Train/Test')
        
        # Add mean residual lines for train and test
        train_mask = self.df['date'] < split_date
        test_mask = self.df['date'] >= split_date
        
        if train_mask.sum() > 0:
            mean_res_train = residuals[train_mask].mean()
            ax4.axhline(mean_res_train, color='#4ECDC4', ls=':', lw=1, alpha=0.6)
        
        if test_mask.sum() > 0:
            mean_res_test = residuals[test_mask].mean()
            ax4.axhline(mean_res_test, color='orange', ls=':', lw=1.5, 
                       label=f'Test bias: {mean_res_test:.3f}')
        
        ax4.set_title(self.t('residuals'), color='white', fontweight='bold')
        ax4.set_ylabel('ln(Actual) - ln(Model)', color='white')
        ax4.legend(loc='upper left', fontsize=7)
        ax4.grid(True, alpha=0.2)
        
        # Update stats text widget
        self.update_stats_panel(harmonics)
        
        self.fig.tight_layout()
        self.canvas.draw()
    
    def update_stats_panel(self, harmonics):
        """Update the statistics panel on the right"""
        self.stats_text_widget.config(state=tk.NORMAL)
        self.stats_text_widget.delete(1.0, tk.END)
        
        stats_text = f"{self.t('model')}\n{'='*28}\n\n"
        stats_text += f"λ = {self.lambda_val:.2f}\n"
        stats_text += f"ω = {self.omega:.4f}\n\n"
        stats_text += f"Harmonics: {harmonics}\n"
        stats_text += f"N params: {2 + len(harmonics)*3}\n\n"
        
        stats_text += f"DE: {self.current_de_iter} iter,\n"
        stats_text += f"    {self.current_de_pop} pop\n\n"
        
        stats_text += f"Power Law:\n"
        stats_text += f"  a_log10={self.settings['pl_a_log10']:.4f}\n"
        stats_text += f"  b={self.settings['pl_b']:.4f}\n\n"
        
        if self.current_stats:
            s = self.current_stats
            stats_text += f"{self.t('performance')}:\n"
            stats_text += f"  R2 train: {s['r2_train']:.4f}\n"
            stats_text += f"  R2 test:  {s['r2_test']:.4f}\n"
            stats_text += f"  R2 full:  {s['r2_full']:.4f}\n"
            if 'mae_test' in s:
                stats_text += f"  MAE test: {s['mae_test']:.4f}\n"
            if 'bias_test' in s:
                stats_text += f"  Bias: {s['bias_test']:.4f}\n"
            stats_text += f"  BIC: {s['bic']:.1f}\n\n"
            
            stats_text += f"{self.t('projections')}:\n"
            stats_text += f"  +10y: {s['ratio_10y']:.2f}x\n"
            stats_text += f"  +25y: {s['ratio_25y']:.2f}x\n"
            stats_text += f"  +50y: {s['ratio_50y']:.2f}x\n\n"
            
            stats_text += f"{'='*28}\n"
            stats_text += f"alpha = {s['alpha']:.4f}\n"
            stats_text += f"c = {s['c']:.4f}\n\n"
        
        # Add harmonics details
        if self.current_params is not None and len(harmonics) > 0:
            stats_text += f"{'='*28}\n"
            stats_text += f"HARMONICS:\n"
            for i, h in enumerate(harmonics):
                A = self.current_params[2 + i*3]
                beta = self.current_params[3 + i*3]
                phi = self.current_params[4 + i*3]
                lam_h = np.exp(2*np.pi / (h * self.omega))
                stats_text += f"\nHarm {h}:\n"
                stats_text += f"  A={A:.2f}\n"
                stats_text += f"  β={beta:.4f}\n"
                stats_text += f"  φ={phi:.4f}\n"
                stats_text += f"  λ={lam_h:.3f}\n"
        
        self.stats_text_widget.insert(tk.END, stats_text)
        self.stats_text_widget.config(state=tk.DISABLED)
        
        # Also update spectral analysis if tab is visible
        self.update_spectral_analysis()
    
    def update_spectral_analysis(self):
        """Run spectral analysis on residuals and update the Spectral tab"""
        if self.current_params is None:
            return
        
        harmonics = self.get_selected_harmonics()
        if not harmonics:
            return
        
        x = self.current_params
        
        # Calculate residuals
        y_fit = perrenod_model(x, self.t_full, self.ln_t_full, harmonics, self.omega)
        residuals = self.y_full - y_fit
        
        # Clear spectral plots
        for ax in self.axes_spectral.flat:
            ax.clear()
            ax.set_facecolor('#1a1a2e')
            ax.tick_params(colors='white')
            for spine in ax.spines.values():
                spine.set_color('white')
        
        # ============ Plot 1: FFT Time Domain ============
        ax1 = self.axes_spectral[0, 0]
        
        N = len(residuals)
        residuals_detrend = residuals - np.mean(residuals)
        fft_vals = fft(residuals_detrend)
        freqs = fftfreq(N, 1)  # 1 day sampling
        
        pos_mask = freqs > 0
        freqs_pos = freqs[pos_mask]
        power = np.abs(fft_vals[pos_mask])**2 / N
        periods = 1 / freqs_pos
        
        # Plot only interesting range (30 days to 5 years)
        mask = (periods > 30) & (periods < 2000)
        ax1.loglog(periods[mask], power[mask], color='#4ECDC4', lw=0.8)
        
        # Mark important periods
        for p, label, color in [(365, '1y', 'yellow'), (365*4, '4y', 'red'), (180, '6m', 'orange')]:
            if 30 < p < 2000:
                ax1.axvline(p, color=color, ls='--', alpha=0.5, lw=1)
        
        ax1.set_title(self.t('fft_time'), color='white', fontsize=10)
        ax1.set_xlabel('Period (days)', color='white', fontsize=8)
        ax1.set_ylabel('Power', color='white', fontsize=8)
        ax1.grid(True, alpha=0.2)
        
        # Find top peaks for stats
        try:
            peaks_idx, _ = find_peaks(power, height=np.percentile(power, 90), distance=10)
            peak_periods = periods[peaks_idx]
            peak_power = power[peaks_idx]
            sort_idx = np.argsort(peak_power)[::-1][:10]
            top_periods = [(peak_periods[i], peak_power[i]) for i in sort_idx]
        except:
            top_periods = []
        
        # ============ Plot 2: FFT Log-Time (LPPL specific) ============
        ax2 = self.axes_spectral[0, 1]
        
        # Resample residuals on uniform ln(t) grid
        ln_t = self.ln_t_full
        ln_t_min, ln_t_max = ln_t.min(), ln_t.max()
        n_points = 1024
        ln_t_uniform = np.linspace(ln_t_min, ln_t_max, n_points)
        d_ln_t = (ln_t_max - ln_t_min) / n_points
        
        interp_func = interp1d(ln_t, residuals, kind='linear', fill_value='extrapolate')
        residuals_ln = interp_func(ln_t_uniform)
        residuals_ln = residuals_ln - residuals_ln.mean()
        
        fft_ln = fft(residuals_ln)
        freqs_ln = fftfreq(n_points, d_ln_t)
        
        pos_mask_ln = freqs_ln > 0
        freqs_ln_pos = freqs_ln[pos_mask_ln]
        power_ln = np.abs(fft_ln[pos_mask_ln])**2 / n_points
        omega_spectrum = 2 * np.pi * freqs_ln_pos
        
        # Plot
        mask_omega = (omega_spectrum > 2) & (omega_spectrum < 50)
        ax2.semilogy(omega_spectrum[mask_omega], power_ln[mask_omega], color='#4ECDC4', lw=0.8)
        
        # Mark expected omega and harmonics
        for n in [1, 2, 3]:
            ax2.axvline(n * self.omega, color='red', ls='--', alpha=0.7, lw=1)
        
        ax2.set_title(f"{self.t('fft_logtime')} (ω={self.omega:.2f})", color='white', fontsize=10)
        ax2.set_xlabel('ω (angular freq in ln(t))', color='white', fontsize=8)
        ax2.set_ylabel('Power', color='white', fontsize=8)
        ax2.grid(True, alpha=0.2)
        
        # ============ Plot 3: ACF ============
        ax3 = self.axes_spectral[1, 0]
        
        # Calculate ACF manually
        n_lags = min(200, len(residuals) // 4)
        acf_values = np.zeros(n_lags)
        var_res = np.var(residuals)
        mean_res = np.mean(residuals)
        
        for lag in range(n_lags):
            if var_res > 0:
                acf_values[lag] = np.mean((residuals[:-lag-1] - mean_res) * (residuals[lag+1:] - mean_res)) / var_res if lag > 0 else 1.0
        
        lags = np.arange(n_lags)
        ax3.bar(lags, acf_values, color='#4ECDC4', alpha=0.7, width=1)
        ax3.axhline(0, color='white', lw=0.5)
        
        # Confidence bounds (95%)
        conf = 1.96 / np.sqrt(len(residuals))
        ax3.axhline(conf, color='red', ls='--', lw=1, alpha=0.7)
        ax3.axhline(-conf, color='red', ls='--', lw=1, alpha=0.7)
        ax3.fill_between(lags, -conf, conf, color='red', alpha=0.1)
        
        ax3.set_title(self.t('acf'), color='white', fontsize=10)
        ax3.set_xlabel('Lag (days)', color='white', fontsize=8)
        ax3.set_ylabel('ACF', color='white', fontsize=8)
        ax3.set_xlim(0, n_lags)
        ax3.grid(True, alpha=0.2)
        
        # ============ Plot 4: Residuals Distribution ============
        ax4 = self.axes_spectral[1, 1]
        
        ax4.hist(residuals, bins=50, density=True, color='#4ECDC4', alpha=0.7, edgecolor='white', linewidth=0.5)
        
        # Overlay normal distribution
        x_norm = np.linspace(residuals.min(), residuals.max(), 100)
        ax4.plot(x_norm, norm.pdf(x_norm, np.mean(residuals), np.std(residuals)), 
                 color='#FF6B6B', lw=2, label='Normal')
        
        ax4.set_title('Residuals Distribution', color='white', fontsize=10)
        ax4.set_xlabel('Residual value', color='white', fontsize=8)
        ax4.set_ylabel('Density', color='white', fontsize=8)
        ax4.legend(fontsize=7)
        ax4.grid(True, alpha=0.2)
        
        self.fig_spectral.tight_layout()
        self.canvas_spectral.draw()
        
        # Update spectral stats panel
        self.update_spectral_stats(residuals, top_periods)
    
    def update_spectral_stats(self, residuals, top_periods):
        """Update the spectral statistics panel"""
        self.spectral_text_widget.config(state=tk.NORMAL)
        self.spectral_text_widget.delete(1.0, tk.END)
        
        stats_text = f"{self.t('spectral_stats')}\n{'='*30}\n\n"
        
        # Basic residual stats
        stats_text += "RESIDUALS:\n"
        stats_text += f"  Mean: {np.mean(residuals):.4f}\n"
        stats_text += f"  Std:  {np.std(residuals):.4f}\n"
        stats_text += f"  Min:  {np.min(residuals):.4f}\n"
        stats_text += f"  Max:  {np.max(residuals):.4f}\n\n"
        
        # Skewness and Kurtosis
        stats_text += f"  Skewness: {skew(residuals):.4f}\n"
        stats_text += f"  Kurtosis: {kurtosis(residuals):.4f}\n\n"
        
        # Top periodic signals
        stats_text += f"{'='*30}\n"
        stats_text += f"{self.t('top_periods')}:\n\n"
        
        for i, (period, power) in enumerate(top_periods[:8]):
            years = period / 365.25
            stats_text += f"  {i+1}. {period:.0f}d ({years:.2f}y)\n"
            stats_text += f"     Power: {power:.2e}\n"
        
        # Durbin-Watson
        stats_text += f"\n{'='*30}\n"
        stats_text += "DIAGNOSTICS:\n\n"
        
        diff = np.diff(residuals)
        dw = np.sum(diff**2) / np.sum(residuals**2)
        stats_text += f"  Durbin-Watson: {dw:.4f}\n"
        stats_text += f"  (2.0 = no autocorr)\n\n"
        
        # Interpretation
        if dw < 1.5:
            stats_text += "  ⚠️ Positive autocorr.\n"
        elif dw > 2.5:
            stats_text += "  ⚠️ Negative autocorr.\n"
        else:
            stats_text += "  ✅ Low autocorr.\n"
        
        self.spectral_text_widget.insert(tk.END, stats_text)
        self.spectral_text_widget.config(state=tk.DISABLED)
        
        # Also update wavelet analysis
        self.update_wavelet_analysis(residuals)
    
    def update_wavelet_analysis(self, residuals):
        """Run wavelet analysis on residuals and update the Wavelet tab"""
        if residuals is None or len(residuals) < 100:
            return
        
        # Clear wavelet plots
        for ax in self.axes_wavelet.flat:
            ax.clear()
            ax.set_facecolor('#1a1a2e')
            ax.tick_params(colors='white')
            for spine in ax.spines.values():
                spine.set_color('white')
        
        # ============ Plot 1: Scalogram (CWT) ============
        ax1 = self.axes_wavelet[0, 0]
        
        # Widths correspond to periods (in days) - extended to ~10^4
        widths = np.arange(20, 5000, 30)
        
        # Normalize residuals
        residuals_norm = (residuals - np.mean(residuals)) / np.std(residuals)
        
        # Simple CWT implementation using Morlet-like wavelet
        try:
            def morlet_wavelet(M, w=5.0, s=1.0):
                """Simple Morlet wavelet"""
                x = np.linspace(-4, 4, M)
                wavelet = np.exp(1j * w * x) * np.exp(-x**2 / (2 * s**2))
                return wavelet / np.sqrt(np.sum(np.abs(wavelet)**2))
            
            cwt_matrix = np.zeros((len(widths), len(residuals_norm)))
            for i, width in enumerate(widths):
                # Create wavelet at this scale
                M = min(len(residuals_norm), int(width * 2))
                if M < 4:
                    M = 4
                wavelet = morlet_wavelet(M, w=5.0, s=1.0)
                
                # Convolve with signal
                conv = np.convolve(residuals_norm, wavelet, mode='same')
                cwt_matrix[i] = np.abs(conv)**2
            
            # Plot scalogram
            dates_idx = np.arange(len(residuals))
            im = ax1.pcolormesh(dates_idx, widths, cwt_matrix, shading='auto', cmap='jet')
            ax1.set_yscale('log')
            ax1.set_ylim(10, 10000)  # Force Y axis to 10^1 - 10^4
            
            # Mark important periods
            for p, label in [(180, '6m'), (365, '1y'), (365*4, '4y'), (365*8, '8y')]:
                if p >= 10 and p <= 10000:
                    ax1.axhline(p, color='white', ls='--', alpha=0.5, lw=0.5)
            
            ax1.set_title(self.t('scalogram'), color='white', fontsize=10)
            ax1.set_xlabel('Days', color='white', fontsize=8)
            ax1.set_ylabel('Period (days)', color='white', fontsize=8)
            
        except Exception as e:
            ax1.text(0.5, 0.5, f'CWT error: {str(e)[:30]}', transform=ax1.transAxes, 
                    color='white', ha='center')
            cwt_matrix = None
        
        # ============ Plot 2: Global Wavelet Spectrum ============
        ax2 = self.axes_wavelet[0, 1]
        
        peak_periods_wavelet = []
        try:
            if cwt_matrix is not None:
                # Global wavelet spectrum (mean power at each period)
                global_ws = np.mean(cwt_matrix, axis=1)
                
                ax2.semilogx(widths, global_ws, color='#4ECDC4', lw=1.5)
                ax2.set_xlim(10, 10000)  # Match scalogram range
                
                # Mark important periods
                for p, label, color in [(180, '6m', 'orange'), (365, '1y', 'yellow'), 
                                        (365*4, '4y', 'red'), (365*8, '8y', 'magenta')]:
                    ax2.axvline(p, color=color, ls='--', alpha=0.6, lw=1)
                    ax2.text(p*1.1, ax2.get_ylim()[1]*0.9 if ax2.get_ylim()[1] > 0 else 1, 
                            label, color=color, fontsize=8)
                
                ax2.set_title(self.t('global_wavelet'), color='white', fontsize=10)
                ax2.set_xlabel('Period (days)', color='white', fontsize=8)
                ax2.set_ylabel('Global Power', color='white', fontsize=8)
                ax2.grid(True, alpha=0.2)
                
                # Find peak periods
                try:
                    peaks_idx, _ = find_peaks(global_ws, height=np.percentile(global_ws, 70), distance=5)
                    peak_periods_wavelet = [(widths[i], global_ws[i]) for i in peaks_idx]
                    peak_periods_wavelet.sort(key=lambda x: x[1], reverse=True)
                except:
                    peak_periods_wavelet = []
                
        except Exception as e:
            ax2.text(0.5, 0.5, f'GWS error: {str(e)[:30]}', transform=ax2.transAxes,
                    color='white', ha='center')
            peak_periods_wavelet = []
        
        # ============ Plot 3: Residuals vs Time with Bubbles ============
        ax3 = self.axes_wavelet[1, 0]
        
        # Plot residuals with color based on magnitude
        dates = self.df['date'].values
        colors = np.where(residuals >= 0, '#4ECDC4', '#FF6B6B')
        
        ax3.scatter(dates, residuals, c=colors, s=1, alpha=0.5)
        ax3.axhline(0, color='white', ls='--', lw=0.5)
        
        # Mark bubble peaks (where residuals are highest)
        threshold = np.percentile(residuals, 95)
        bubble_mask = residuals > threshold
        if bubble_mask.sum() > 0:
            ax3.scatter(dates[bubble_mask], residuals[bubble_mask], 
                       c='yellow', s=10, alpha=0.8, label='Bubble peaks')
        
        ax3.set_title('Residuals with Bubble Peaks', color='white', fontsize=10)
        ax3.set_xlabel('Date', color='white', fontsize=8)
        ax3.set_ylabel('Residual', color='white', fontsize=8)
        ax3.legend(fontsize=7, loc='upper left')
        ax3.grid(True, alpha=0.2)
        
        # ============ Plot 4: Power vs Lambda ============
        ax4 = self.axes_wavelet[1, 1]
        
        # Calculate lambda from periods
        # Using relation: period ≈ ln(lambda) * T_base
        # For LPPL: lambda^n gives period ratio
        try:
            ln_t = self.ln_t_full
            ln_t_min, ln_t_max = ln_t.min(), ln_t.max()
            n_points = 1024
            ln_t_uniform = np.linspace(ln_t_min, ln_t_max, n_points)
            d_ln_t = (ln_t_max - ln_t_min) / n_points
            
            interp_func = interp1d(ln_t, residuals, kind='linear', fill_value='extrapolate')
            residuals_ln = interp_func(ln_t_uniform) - np.mean(residuals)
            
            fft_ln = fft(residuals_ln)
            freqs_ln = fftfreq(n_points, d_ln_t)
            
            pos_mask_ln = freqs_ln > 0
            freqs_ln_pos = freqs_ln[pos_mask_ln]
            power_ln = np.abs(fft_ln[pos_mask_ln])**2 / n_points
            omega_spectrum = 2 * np.pi * freqs_ln_pos
            
            # Convert omega to lambda
            # lambda = exp(2*pi / omega)
            valid_mask = omega_spectrum > 0.5
            lambda_spectrum = np.exp(2 * np.pi / omega_spectrum[valid_mask])
            power_lambda = power_ln[valid_mask]
            
            # Filter to reasonable lambda range
            lambda_mask = (lambda_spectrum > 1.1) & (lambda_spectrum < 5)
            
            ax4.semilogy(lambda_spectrum[lambda_mask], power_lambda[lambda_mask], 
                        color='#4ECDC4', lw=0.8)
            
            # Mark expected lambda
            ax4.axvline(self.lambda_val, color='red', ls='--', lw=1.5, 
                       label=f'λ={self.lambda_val:.2f}')
            ax4.axvline(np.sqrt(self.lambda_val), color='orange', ls=':', lw=1,
                       label=f'√λ={np.sqrt(self.lambda_val):.2f}')
            
            ax4.set_title('Power vs λ (log-time FFT)', color='white', fontsize=10)
            ax4.set_xlabel('λ (scale ratio)', color='white', fontsize=8)
            ax4.set_ylabel('Power', color='white', fontsize=8)
            ax4.legend(fontsize=7)
            ax4.grid(True, alpha=0.2)
            
        except Exception as e:
            ax4.text(0.5, 0.5, f'Lambda error: {str(e)[:30]}', transform=ax4.transAxes,
                    color='white', ha='center')
        
        self.fig_wavelet.tight_layout()
        self.canvas_wavelet.draw()
        
        # Update wavelet stats
        self.update_wavelet_stats(residuals, peak_periods_wavelet)
    
    def update_wavelet_stats(self, residuals, peak_periods):
        """Update the wavelet statistics panel"""
        self.wavelet_text_widget.config(state=tk.NORMAL)
        self.wavelet_text_widget.delete(1.0, tk.END)
        
        stats_text = f"{self.t('wavelet_stats')}\n{'='*30}\n\n"
        
        # Wavelet peaks
        stats_text += "DOMINANT PERIODS:\n"
        stats_text += "(from Global Wavelet)\n\n"
        
        for i, (period, power) in enumerate(peak_periods[:6]):
            years = period / 365.25
            stats_text += f"  {i+1}. {period:.0f}d ({years:.2f}y)\n"
            stats_text += f"     Power: {power:.2e}\n"
        
        # Bubble analysis
        stats_text += f"\n{'='*30}\n"
        stats_text += "BUBBLE ANALYSIS:\n\n"
        
        threshold = np.percentile(residuals, 95)
        bubble_mask = residuals > threshold
        n_bubble_days = bubble_mask.sum()
        
        stats_text += f"  Bubble threshold: {threshold:.3f}\n"
        stats_text += f"  Bubble days: {n_bubble_days}\n"
        stats_text += f"  Bubble %: {100*n_bubble_days/len(residuals):.1f}%\n\n"
        
        # Find bubble periods
        if n_bubble_days > 0:
            dates = self.df['date'].values
            bubble_dates = dates[bubble_mask]
            
            # Group consecutive bubble days
            stats_text += "  Bubble periods:\n"
            
            # Simple approach: find start/end of bubble clusters
            bubble_idx = np.where(bubble_mask)[0]
            if len(bubble_idx) > 0:
                clusters = []
                start = bubble_idx[0]
                end = bubble_idx[0]
                
                for idx in bubble_idx[1:]:
                    if idx - end <= 30:  # Within 30 days = same cluster
                        end = idx
                    else:
                        clusters.append((start, end))
                        start = idx
                        end = idx
                clusters.append((start, end))
                
                for i, (s, e) in enumerate(clusters[-5:]):  # Last 5 bubbles
                    d1 = pd.Timestamp(dates[s]).strftime('%Y-%m')
                    d2 = pd.Timestamp(dates[e]).strftime('%Y-%m')
                    stats_text += f"    {d1} - {d2}\n"
        
        # Lambda interpretation
        stats_text += f"\n{'='*30}\n"
        stats_text += "LPPL INTERPRETATION:\n\n"
        stats_text += f"  λ = {self.lambda_val:.3f}\n"
        stats_text += f"  ω = {self.omega:.3f}\n\n"
        stats_text += f"  Scale ratio: {self.lambda_val:.2f}x\n"
        stats_text += f"  Per cycle: ~{np.log(self.lambda_val)*365:.0f}d\n"
        
        self.wavelet_text_widget.insert(tk.END, stats_text)
        self.wavelet_text_widget.config(state=tk.DISABLED)
    
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
        
        # Recalculate omega if lambda changed
        self.lambda_val = self.settings.get('lambda', LAMBDA_PERRENOD)
        self.omega = 2 * np.pi / np.log(self.lambda_val)
        
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
        self.window.geometry("450x500")
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
        
        # Power Law Parameters tab
        tab_pl = ttk.Frame(notebook)
        notebook.add(tab_pl, text="Power Law")
        
        row = 0
        ttk.Label(tab_pl, text="a_log10 (BTC/USD):").grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        self.pl_a_var = tk.StringVar(value=str(self.settings['pl_a_log10']))
        ttk.Entry(tab_pl, textvariable=self.pl_a_var, width=15).grid(row=row, column=1, padx=10, pady=5)
        
        row += 1
        ttk.Label(tab_pl, text="b (exponent):").grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        self.pl_b_var = tk.StringVar(value=str(self.settings['pl_b']))
        ttk.Entry(tab_pl, textvariable=self.pl_b_var, width=15).grid(row=row, column=1, padx=10, pady=5)
        
        row += 1
        ttk.Label(tab_pl, text="λ (lambda):").grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        self.lambda_var = tk.StringVar(value=str(self.settings.get('lambda', 2.07)))
        ttk.Entry(tab_pl, textvariable=self.lambda_var, width=15).grid(row=row, column=1, padx=10, pady=5)
        ttk.Label(tab_pl, text="Perrenod: 2.07, Standard: 2.0").grid(row=row, column=2, sticky=tk.W, padx=5)
        
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
            self.settings['pl_a_log10'] = float(self.pl_a_var.get())
            self.settings['pl_b'] = float(self.pl_b_var.get())
            self.settings['lambda'] = float(self.lambda_var.get())
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
    app = PerrenodGoldExplorer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
