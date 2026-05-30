from executor.llm_core import ask
from executor.memory import load


BAD_GREEK_MARKERS = [
    "Έλεγχοςτελευταίων",
    "Έλεγχος τελευταίωνενεργειών",
    "τελευταίωνενεργειών",
    "τοModified",
    "Καταγράψτε",
    "Προσθέστε",
    "εκecute",
    "εκτελείτε",
    "εκπιπτόμενο",
    "aim to",
    "\u202f",
]


def clean_review(text):
    text = str(text).replace("\u202f", " ")
    text = text.replace("Έλεγχοςτελευταίων", "Έλεγχος τελευταίων")
    text = text.replace("τοModified", "το τροποποιημένο")
    text = text.replace("Καταγράψτε", "Κατέγραψε")
    text = text.replace("Προσθέστε", "Πρόσθεσε")
    text = text.replace("Έλεγχος τελευταίωνενεργειών", "Έλεγχος τελευταίων ενεργειών")
    text = text.replace("τελευταίωνενεργειών", "τελευταίων ενεργειών")
    text = text.replace("εκecute", "εκτέλεση")
    return text.strip()


def fallback_review(mem):
    return (
        "Έλεγχος τελευταίων ενεργειών\n\n"
        "1. Τι έγινε:\n"
        "- Ελέγχθηκαν οι τελευταίες ενέργειες του ΝΟΥΣ.\n\n"
        "2. Αν πέτυχε:\n"
        "- Μερικώς. Το σύστημα απάντησε, αλλά η ποιότητα ελληνικών του review χρειάζεται βελτίωση.\n\n"
        "3. Πρόβλημα ή ρίσκο:\n"
        "- Το review μπορεί να εμφανίσει κολλημένες λέξεις ή άσχημες μεταφράσεις.\n\n"
        "4. Επόμενο μικρό βήμα:\n"
        "- Συνέχισε με μικρά patches και έλεγχο compile πριν από κάθε commit."
    )


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
- Γράψε φυσικά ελληνικά, σαν τεχνικός συνεργάτης.
- Απόφυγε κολλημένες λέξεις και άσχημες μεταφράσεις.
- Μην χρησιμοποιείς προστακτική πληθυντικού όπως "Καταγράψτε". Μίλα στον χρήστη φιλικά στον ενικό.

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
    text = res.get("response", str(res)) if isinstance(res, dict) else str(res)
    text = clean_review(text)

    if any(marker in text for marker in BAD_GREEK_MARKERS):
        return fallback_review(mem)

    return text
