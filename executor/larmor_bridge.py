"""
NOUS ↔ Larmor Bridge — read-only access to the Larmor frequency calculator.
No writes, no modifications — observation and analysis only.
"""

import requests
from executor.remote_llm import ask_with_turns

LARMOR_APP_URL = "https://insta-giveaway-bot-1--traianos1985.replit.app"

# ── Material library (γ/2π in Hz/T) ────────────────────────────────────────
MATERIALS = {
    "au-pure":       {"name": "197Au (χρυσός καθαρός)",           "gamma": 0.7379e6},
    "ottoman-5lira": {"name": "Ottoman 5 Lira (91.7% Au)",        "gamma": 1.6155005e6},
    "22k-alloy":     {"name": "Κράμα Χρυσής Λίρας (22K)",        "gamma": 1.619025e6},
    "ag":            {"name": "109Ag (άργυρος)",                   "gamma": 1.98965e6},
    "cu":            {"name": "63Cu (χαλκός)",                     "gamma": 11.3114e6},
    "al":            {"name": "27Al (αλουμίνιο)",                  "gamma": 11.100630e6},
    "fe":            {"name": "57Fe (σίδηρος)",                    "gamma": 1.3818e6},
    "ammo-box":      {"name": "55Mn (κιβώτιο πυρ. British WWII)", "gamma": 10.5707e6},
    "c":             {"name": "13C (διαμάντι)",                    "gamma": 10.707746e6},
    "ba-137":        {"name": "137Ba (χειροβομβίδες/Baratol)",    "gamma": 4.7634601e6},
    "sn-119":        {"name": "119Sn (κασσίτερος/τενεκές)",       "gamma": 15.9449e6},
    "sb-121":        {"name": "121Sb (αντιμόνιο)",                "gamma": 10.2387e6},
    "b-11":          {"name": "11B (βόριο/βόρακας)",              "gamma": 13.6616080e6},
}


def calculate_larmor(material_key: str, b_field_T: float) -> dict:
    """Calculate Larmor frequency fL = γ/2π × B"""
    mat = MATERIALS.get(material_key)
    if not mat:
        return {"error": f"Unknown material: {material_key}"}
    gamma = mat["gamma"]
    f_hz = gamma * b_field_T
    f_khz = f_hz / 1e3
    f_mhz = f_hz / 1e6
    harmonics = [{"n": n, "hz": f_hz * n, "khz": f_khz * n, "mhz": f_mhz * n}
                 for n in range(1, 21)]
    return {
        "material": mat["name"],
        "material_key": material_key,
        "gamma_hz_per_T": gamma,
        "b_field_T": b_field_T,
        "f_larmor_hz": f_hz,
        "f_larmor_khz": f_khz,
        "f_larmor_mhz": f_mhz,
        "harmonics": harmonics,
    }


def skin_depth_m(sigma_S_per_m: float, freq_hz: float) -> float:
    """δ = 1/sqrt(π × f × μ₀ × σ)"""
    import math
    mu0 = 4 * math.pi * 1e-7
    denom = math.pi * freq_hz * mu0 * sigma_S_per_m
    if denom <= 0:
        return 9999.0
    return 1.0 / math.sqrt(denom)


def ping_larmor_app() -> dict:
    """Check if the Larmor app is online."""
    try:
        r = requests.get(LARMOR_APP_URL, timeout=8, verify=False)
        online = r.status_code == 200 and "Larmor" in r.text
        return {"online": online, "status_code": r.status_code, "url": LARMOR_APP_URL}
    except Exception as e:
        return {"online": False, "error": str(e), "url": LARMOR_APP_URL}


def analyze_session(session_data: dict | str, question: str = "") -> str:
    """
    AI analysis of Larmor session data with specialized NMR/geophysics knowledge.
    session_data: either raw JSON from user or dict with calculation results.
    question: optional specific question from user.
    """
    system_prompt = """Είσαι ο ΝΟΥΣ, εξειδικευμένος αναλυτής NMR γεωφυσικής έρευνας.
Έχεις πλήρη γνώση:

— Φυσική NMR / Larmor:
  fL = (γ/2π) × B₀
  Γυρομαγνητικές σταθερές: Au=0.7379 MHz/T, Ottoman 5 Lira=1.6155 MHz/T, 22K Alloy=1.619 MHz/T,
  Ag=1.989 MHz/T, Cu=11.311 MHz/T, Al=11.101 MHz/T, Fe=1.382 MHz/T, Mn(WWII box)=10.571 MHz/T,
  Ba-137=4.763 MHz/T, Sn=15.945 MHz/T, Sb=10.239 MHz/T, B-11=13.662 MHz/T

— BGS WMM2025 (World Magnetic Model 2025-2030):
  Μαγνητικό πεδίο Μεσσηνία ~47,000-49,000 nT (0.047-0.049 T)
  Κλίση ~55°, Απόκλιση ~4°E

— Βάθος διείσδυσης (skin depth):
  δ = 1/√(π × f × μ₀ × σ)
  Τύποι εδάφους: βραχώδες σ≈0.00001, ξηρό σ≈0.001, μέτριο σ≈0.01, υγρό σ≈0.05, κορεσμένο σ≈0.1

— Στρατηγική αρμονικών:
  Υψηλότερες αρμονικές → μικρότερο skin depth → λιγότερο βάθος
  Βέλτιστη αρμονική n: επιλέγεται ώστε δ ≈ 1.5 × ageFactor × βάθος στόχου
  AgeFactor: πρόσφατο=1.0, αντάρτικα 1940-50=1.25, οθωμανικό <1900=1.6

— Γεωγραφικό/ιστορικό πλαίσιο Μεσσηνίας:
  Περιοχή πλούσια σε αρχαιολογικά ευρήματα (Αρχαία Μεσσήνη, Βυζαντινά, Οθωμανικά, WWII).
  Κρυμμένα αντικείμενα: χρυσές λίρες, οθωμανικά νομίσματα, WWII πυρομαχικά/θησαυροί.

— Σφάλματα / Προβλήματα πεδίου:
  Ατμοσφαιρικοί θόρυβοι (Schumann resonances): 7.83, 14.3, 20.8, 27.3 Hz — αποφεύγε τις κοντινές αρμονικές.
  Βιολογικοί θόρυβοι: 50/60 Hz ηλεκτρικό δίκτυο.
  Οριζόντιοι θόρυβοι: 1/f noise, σεισμικός θόρυβος < 1 Hz.

Απαντάς ΜΟΝΟ με ανάλυση, συμπεράσματα και πρακτικές προτάσεις.
Αν υπάρχουν δεδομένα υπολογισμού, τα αναλύεις βήμα-βήμα.
Απαντάς πάντα στα Ελληνικά."""

    data_str = session_data if isinstance(session_data, str) else str(session_data)
    user_content = f"""Δεδομένα από τον Υπολογιστή Larmor:

{data_str}
"""
    if question:
        user_content += f"\nΕρώτηση: {question}"
    else:
        user_content += "\nΑνάλυσε τα δεδομένα και δώσε:\n1. Σύνοψη υπολογισμού\n2. Αξιολόγηση παραμέτρων\n3. Βέλτιστες αρμονικές για το βάθος/υλικό\n4. Πρακτικές προτάσεις για την έρευνα πεδίου"

    turns = [{"role": "user", "content": user_content}]
    try:
        result = ask_with_turns(turns, system=system_prompt)
        return result
    except Exception as e:
        return f"Σφάλμα ανάλυσης: {e}"


def larmor_chat(conversation: list[dict]) -> str:
    """
    Multi-turn chat about Larmor/NMR research.
    conversation: list of {role: user|assistant, content: str}
    """
    system_prompt = """Είσαι ο ΝΟΥΣ, εξειδικευμένος σύμβουλος NMR γεωφυσικής και έρευνας πεδίου.
Γνωρίζεις άριστα:
- Φυσική NMR/Larmor: fL = (γ/2π)B₀, γυρομαγνητικές σταθερές υλικών
- BGS WMM2025 γεωμαγνητικό μοντέλο και εφαρμογές στην Ελλάδα
- Βάθος διείσδυσης (skin depth) συναρτήσει εδάφους και συχνότητας
- Στρατηγική επιλογής αρμονικών για βέλτιστο βάθος
- Ιστορικό/αρχαιολογικό πλαίσιο Μεσσηνίας
- Πρακτικές τεχνικές πεδίου NMR/Larmor
- Ηλεκτρομαγνητικούς θορύβους και αντιμετώπισή τους

Απαντάς με ακρίβεια, επιστημονικά αλλά κατανοητά. Πάντα στα Ελληνικά."""
    try:
        result = ask_with_turns(conversation, system=system_prompt)
        return result
    except Exception as e:
        return f"Σφάλμα: {e}"
