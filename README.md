# AURA-NETSTRESS
Erzeugt konstante Dauerlast über offizielle Hetzner-Speedtest-Knoten ohne Festplatten-Verschleiß.
<img width="1917" height="840" alt="image" src="https://github.com/user-attachments/assets/f47157c2-64ab-42bc-a575-203e8de91600" />


# ⚡ AURA // NETSTRESS

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+"/>
  <img src="https://img.shields.io/badge/Platform-Windows%20|%20macOS%20|%20Linux-0078D6?style=for-the-badge" alt="Cross-Platform"/>
  <img src="https://img.shields.io/badge/Disk--I%2FO-0%20Bytes%20(Safe%20for%20SSDs)-00C853?style=for-the-badge" alt="Zero Disk IO"/>
  <img src="https://img.shields.io/badge/Dependencies-Zero%20(Pure%20Stdlib)-A855F7?style=for-the-badge" alt="Zero External Dependencies"/>
  <img src="https://img.shields.io/badge/License-MIT-F59E0B?style=for-the-badge" alt="MIT License"/>
</p>

<p align="center">
  <b>Minimalistisches, SSD-schonendes WLAN- & Netzwerk-Stresstest-Tool mit Cyberpunk / Gen Z Bento-Grid UI.</b><br>
  Erzeugt regulierbare Dauerlast über offizielle Hetzner CDN/Datacenter-Backbones direkt im RAM – ohne Festplatten-Verschleiß und mit minimalster CPU-Last.
</p>

---

## 🎯 Warum AURA // NETSTRESS? (The Problem vs. The Solution)

Wenn du dein WLAN auf Herz und Nieren testen willst (z. B. Mesh-Roaming, Bufferbloat, Wi-Fi 6/7 Durchsatz, AP-Thermal-Throttling), stößt du bei herkömmlichen Methoden schnell auf Probleme:

* ❌ **Browser-Speedtests (Speedtest.net, Fast.com):** Laufen nur 10 bis 15 Sekunden. Völlig ungeeignet für 30-minütige Dauerlast- oder Stabilitätstests.
* ❌ **Große Testdateien per Browser / `wget` herunterladen:** Zerstört mit der Zeit die Schreibzyklen deiner NVMe/SSD, wenn du täglich hunderte Gigabyte Test-Payload auf die Festplatte schreibst.
* ❌ **`iperf3`:** Genial, erfordert aber zwingend einen zweiten dedizierten Rechner/Server im LAN als Gegenstelle.

**Die Lösung:** **AURA // NETSTRESS** streamt 10 GB große Test-Binaries offizieller Hetzner-Backbones direkt in einen fixen 256-KB-RAM-Puffer (`memoryview`) und verwirft die Pakete sofort. 
**Ergebnis:** 100 % Netzwerkauslastung, 0 Bytes SSD-Schreibzugriffe und unter 1 % CPU-Overhead.

---

## ⚡ Key Features

- 🛡️ **Zero Disk I/O & SSD Protection:** Verwendet Python `memoryview` und `readinto` – die Daten werden im flüchtigen RAM überschrieben und niemals auf Massenspeicher abgelegt.
- 🌍 **Globale Hetzner High-Speed Knoten:** Falkenstein, Nürnberg, Helsinki, Ashburn (USA), Hillsboro (USA) und Singapur mit direkter Anbindung an Tier-1 Carrier.
- 🚀 **Multi-Stream Engine (1 bis 8 Threads):** Öffne bis zu 8 parallele TCP-Streams, um das volle Potential von Multi-Gigabit- und High-End-Wi-Fi-Verbindungen auszuschöpfen.
- 🎛️ **Live Speed-Limiter (Token-Bucket):** Drossle die Last stufenlos im laufenden Betrieb (z. B. auf exakt 50 Mbit/s), um dein Heimnetz gezielt zu belasten, ohne andere Teilnehmer komplett abzuschnüren.
- 🎯 **Target Auto-Stop:** Setze ein automatisches Datenvolumen-Ziel (z. B. 25 GB) oder teste endlos.
- 📈 **Real-Time Waveform Graph:** Glatter 60-Sekunden-Durchsatzverlauf inklusive Peak- und Durchschnitts-Messung (`Ø Mbit/s`).
- 💅 **Cyberpunk / Gen Z Aesthetic:** Dark Obsidian Theme (`#09090E`), Neon-Akzente und dynamischer Vibe-Check (*Aura Meter*).
- 📦 **Zero Dependencies:** Benötigt ausschließlich die Python-Standardbibliothek (`tkinter`, `urllib`, `ssl`, `threading`). Kein `pip install` erforderlich!

---

## 🕹️ Use Cases

1. **WLAN Mesh & Roaming-Diagnose:**
   Laufe mit deinem Laptop durch die Wohnung/das Haus, während der Stresstest läuft. Anhand von Einbrüchen in der Live-Waveform erkennst du exakt, wo Access Points wechseln, wo tote Winkel liegen oder wo Roaming fehlschlägt.
2. **Bufferbloat & QoS / SQM Überprüfung:**
   Erzeuge 50, 100 oder 250 Mbit/s Dauerlast und teste parallel die Ping-Stabilität (z. B. zu Cloudflare `1.1.1.1` oder Google `8.8.8.8`), um Bufferbloat deines Routers zu identifizieren.
3. **Wi-Fi Kanal-Interferenz- & Lasttests:**
   Finde heraus, ob dein 5 GHz / 6 GHz Kanal bei 10 Minuten Volllast stabil bleibt oder ob DFS-Warngeräusche, Nachbar-WLANs oder thermisches Drosseln des Routers auftreten.
4. **ISP Peering Check:**
   Wechsle zwischen Falkenstein, USA und Singapur, um das internationale Routing und Peering deines Providers unter Dauerlast zu bewerten.

---

## 📦 Installation & Schnellstart

### 1. Repository klonen oder herunterladen
```bash
git clone [https://github.com/DEIN_USERNAME/aura-netstress.git](https://github.com/DEIN_USERNAME/aura-netstress.git)
cd aura-netstress
