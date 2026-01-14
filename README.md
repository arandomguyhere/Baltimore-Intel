<p align="center">
    <img alt="Baltimore Intel" src="https://img.shields.io/badge/Baltimore-Intel-0066cc?style=for-the-badge&logo=radar&logoColor=white" height="60">
</p>

<p align="center">
    <strong>Critical Infrastructure Intelligence Platform for the Port of Baltimore</strong>
</p>

<p align="center">
    <a href="https://arandomguyhere.github.io/Baltimore-Intel/">
        <img src="https://img.shields.io/badge/Dashboard-LIVE-success?style=for-the-badge&logo=github&logoColor=white" alt="Dashboard">
    </a>
    <a href="https://github.com/arandomguyhere/Baltimore-Intel/actions/workflows/collect-and-deploy.yml">
        <img src="https://img.shields.io/github/actions/workflow/status/arandomguyhere/Baltimore-Intel/collect-and-deploy.yml?style=for-the-badge&label=Data%20Collection" alt="Data Collection">
    </a>
    <a href="./LICENSE">
        <img src="https://img.shields.io/github/license/arandomguyhere/Baltimore-Intel?style=for-the-badge" alt="License">
    </a>
</p>

---

## Live Dashboard

**https://arandomguyhere.github.io/Baltimore-Intel/**

---

## Features

| Feature | Status | Description |
|---------|--------|-------------|
| **Amtrak Train Tracking** | ✅ Live | Real-time train positions via Amtraker API |
| **Baltimore News Feed** | ✅ Live | Port/shipping/infrastructure news from Google News RSS |
| **Rail Network Overlay** | ✅ Live | OpenRailwayMap tile layer |
| **Infrastructure Status** | ✅ Live | Terminal and chokepoint monitoring |
| **AIS Vessel Tracking** | ✅ Live | Real-time ship positions (enter API key in Settings) |
| **Scanner Feeds** | ✅ Live | Broadcastify links with transcription via ScannerTranscribe |
| **Commodities** | ⚠️ Simulated | Placeholder data (real APIs need keys) |

---

## Quick Start

### 1. View the Dashboard
Visit **https://arandomguyhere.github.io/Baltimore-Intel/** - data updates every 15 minutes.

### 2. Enable AIS Vessel Tracking
1. Get a free API key from [aisstream.io](https://aisstream.io)
2. Click **Settings** in the dashboard header
3. Paste your API key and click **Save & Connect**
4. Toggle **Vessel Tracks** on the map to see ships

### 3. Use Scanner Transcription
1. Click **Listen** to open a Broadcastify feed
2. Click **Transcribe** to open [ScannerTranscribe](https://arandomguyhere.github.io/ScannerTranscribe/)
3. Start capture in ScannerTranscribe to transcribe audio

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│           GitHub Actions (every 15 minutes)                      │
│   collect_data.py → APIs → JSON files → GitHub Pages deploy      │
└─────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│                    docs/data/*.json                              │
│   amtrak │ news │ commodities │ infrastructure │ vessels         │
└─────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│              Dashboard (GitHub Pages)                            │
│   Leaflet Map │ News Panel │ Scanner Feeds │ Commodities         │
│                                                                  │
│   + Live WebSocket connections:                                  │
│     • AISstream (vessels) - API key in Settings                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Sources

| Source | Type | API/URL | Auth Required |
|--------|------|---------|---------------|
| **Amtraker** | Trains | `api-v3.amtraker.com` | No |
| **Google News RSS** | News | `news.google.com/rss` | No |
| **OpenRailwayMap** | Rail tiles | `tiles.openrailwaymap.org` | No |
| **AISstream** | Vessels | `stream.aisstream.io` | Yes (free) |
| **Broadcastify** | Scanners | `broadcastify.com` | No |
| **ScannerTranscribe** | Transcription | Your app | No |

---

## Scanner Feeds (Broadcastify)

| Feed | ID | Coverage |
|------|----|----------|
| Baltimore Rail (CSX/NS/Amtrak) | 14954 | Rail communications |
| Baltimore City/County Fire | 22380 | Fire dispatch |
| Baltimore City Police | 32008 | Police talkgroups |
| Baltimore County Fire/EMS | 16828 | County fire/EMS |

---

## Port Infrastructure

### Terminals
| Terminal | Type | Status |
|----------|------|--------|
| Seagirt Marine Terminal | Container | Operational |
| Dundalk Marine Terminal | RoRo/Breakbulk | Operational |
| CNX Marine Terminal | Coal Export | Operational |
| Fairfield Auto Terminal | Automobiles | Operational |

### Rail
| Location | Operator | Notes |
|----------|----------|-------|
| Howard Street Tunnel | CSX | Capacity bottleneck |
| Penn Station | Amtrak | NEC hub |
| Bayview Yard | Norfolk Southern | Intermodal |

### Chokepoints
| Location | Status | Notes |
|----------|--------|-------|
| Fort McHenry Channel | Operational | Main ship channel |
| Key Bridge Area | Critical | Bridge collapse - restricted navigation |

---

## Project Structure

```
Baltimore-Intel/
├── docs/                          # GitHub Pages dashboard
│   ├── index.html                 # Main dashboard (Leaflet + panels)
│   └── data/                      # JSON data (auto-updated)
│       ├── amtrak.json            # Train positions
│       ├── news.json              # Baltimore news
│       ├── commodities.json       # Port commodities
│       ├── infrastructure.json    # Status monitoring
│       ├── vessels.json           # AIS vessel data
│       └── manifest.json          # Data manifest
├── baltimore_intel/               # Python data collectors
│   └── collect_data.py            # Main collector script
├── .github/workflows/
│   ├── collect-and-deploy.yml     # Scheduled collection + deploy
│   ├── auto-assign.yml            # Issue assignment
│   └── codeql-analysis.yml        # Security scanning
└── README.md
```

---

## Local Development

### Run Data Collector
```bash
cd baltimore_intel
pip install requests websocket-client
python collect_data.py
```

### With AIS (requires API key)
```bash
export AISSTREAM_API_KEY=your_key_here
python collect_data.py
```

---

## GitHub Secrets (Optional)

For automated AIS collection via GitHub Actions:

| Secret | Description |
|--------|-------------|
| `AISSTREAM_API_KEY` | AISstream.io API key for vessel tracking |

Add at: Repository Settings → Secrets → Actions → New secret

---

## Related Projects

| Project | Description |
|---------|-------------|
| [ScannerTranscribe](https://github.com/arandomguyhere/ScannerTranscribe) | Browser-based scanner transcription with Whisper AI |
| [Google-News-Scraper](https://github.com/arandomguyhere/Google-News-Scraper) | News aggregation with entity extraction |
| [AIS_Tracker](https://github.com/arandomguyhere/AIS_Tracker) | Vessel tracking dashboard |

---

## Credits

- **Amtraker** - [amtraker.com](https://amtraker.com/)
- **OpenRailwayMap** - [openrailwaymap.org](https://www.openrailwaymap.org/)
- **AISstream** - [aisstream.io](https://aisstream.io/)
- **Broadcastify** - [broadcastify.com](https://www.broadcastify.com/)

---

## License

AGPL-3.0 - See [LICENSE](./LICENSE)
