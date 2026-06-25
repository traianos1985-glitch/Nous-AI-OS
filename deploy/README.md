# NOUS AI OS — Deployment Guide

## Επιλογές Hosting

### Επιλογή Α: VPS (Συνιστάται — ~€4-6/μήνα)

**Καλύτερα providers για NOUS:**
- **Hetzner Cloud** (Φινλανδία/Γερμανία) — CX22: 2 CPU, 4GB RAM = **€3.79/μήνα**
- **DigitalOcean** — Basic Droplet 1GB = **$6/μήνα**
- **Vultr** — Cloud Compute 1GB = **$5/μήνα**

**Βήματα:**
1. Φτιάξε λογαριασμό στο Hetzner (π.χ.)
2. Δημιούργησε server: Ubuntu 22.04, CX22
3. Αντέγραψε τον φάκελο NOUS στον server
4. Τρέξε: `bash deploy/setup_vps.sh`
5. Άνοιξε `http://YOUR_SERVER_IP` στον browser

**Μεταφορά αρχείων από Replit στον VPS:**
```bash
# Κατέβασε το project ως ZIP από Replit
# Μεταφόρτωσε στον VPS:
scp nous-ai-os.zip root@YOUR_VPS_IP:/opt/
ssh root@YOUR_VPS_IP "cd /opt && unzip nous-ai-os.zip && bash nous-ai-os/deploy/setup_vps.sh"
```

---

### Επιλογή Β: Docker (σε οποιοδήποτε Linux)

```bash
# Αντέγραψε .env αρχείο
cp .env.example .env
# Βάλε το OPENROUTER_API_KEY στο .env

# Ξεκίνα
docker-compose up -d

# Δες logs
docker-compose logs -f
```

---

### Επιλογή Γ: Raspberry Pi (δωρεάν, τρέχει στο σπίτι)

Αν έχεις Raspberry Pi 3/4:
```bash
# Στο Pi (Raspberry Pi OS):
git clone <your-repo> nous
cd nous
bash deploy/setup_vps.sh
```
Κόστος: **€0/μήνα** (μόνο ρεύμα ~2-3€)

---

## Χρήσιμες Εντολές (μετά την εγκατάσταση)

```bash
# Δες κατάσταση
systemctl status nous

# Δες live logs
journalctl -u nous -f

# Κάνε restart
systemctl restart nous

# Ενημέρωσε τον κώδικα
bash deploy/update.sh
```

---

## Environment Variables

Αποθήκευσε στο αρχείο `/opt/nous/.env`:

```
OPENROUTER_API_KEY=sk-or-v1-...
```

---

## Backup Data

```bash
# Από τον τοπικό σου υπολογιστή:
bash deploy/backup_data.sh root@YOUR_VPS_IP
```

Αποθηκεύει όλη τη μνήμη, τα goals, τις συνομιλίες.
