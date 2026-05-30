from executor.llm_core import ask
from executor.memory import load


def review_last():
    mem = load()[-10:]

    prompt = f"""
Είσαι ο reviewer agent του ΝΟΥΣ AI OS.

Context συστήματος:
- Ο ΝΟΥΣ τρέχει σε Android / Termux.
- Backend: Python 3.13 και Flask.
- Τα plugins είναι Python αρχεία με def run() μέσα στο executor/plugins/.
- Στόχος σου είναι να κάνεις καθαρό, χρήσιμο έλεγχο των τελευταίων ενεργειών.
- Μην προτείνεις npm, JavaScript, plugin.json ή manifest.
- Μην ξανασχεδιάζεις τον ΝΟΥΣ από την αρχή.
- Μην χρησιμοποιείς περίεργες ή κακές ελληνικές μεταφράσεις.
- Γράψε φυσικά ελληνικά, σαν τεχνικός συνεργάτης.

Πρόσφατα γεγονότα:
{mem}

Απάντησε αυστηρά με αυτή τη μορφή:

Έλεγχος τελευταίων ενεργειών

1. Τι έγινε:
- σύντομη περίληψη

2. Αν πέτυχε:
- ναι / όχι / μερικώς και γιατί

3. Πρόβλημα ή ρίσκο:
- το βασικότερο θέμα που βλέπεις

4. Επόμενο μικρό βήμα:
- μία συγκεκριμένη, ασφαλής ενέργεια
"""

    res = ask(prompt)
    return res.get("response", str(res)) if isinstance(res, dict) else str(res)
