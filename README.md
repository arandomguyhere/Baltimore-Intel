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
    <a href="https://github.com/arandomguyhere/Baltimore-Intel/actions/workflows/collect-data.yml">
        <img src="https://img.shields.io/github/actions/workflow/status/arandomguyhere/Baltimore-Intel/collect-data.yml?style=for-the-badge&label=Data%20Collection" alt="Data Collection">
    </a>
    <a href="./LICENSE">
        <img src="https://img.shields.io/github/license/arandomguyhere/Baltimore-Intel?style=for-the-badge" alt="License">
    </a>
</p>

---

## Status

| Data Source | Status | Update Frequency | Notes |
|-------------|--------|------------------|-------|
| **Amtrak Trains** | ✅ Working | Every 15 min | Via Amtraker API |
| **News Feed** | ✅ Working | Every 15 min | Via Google-News-Scraper |
| **Rail Map Overlay** | ✅ Working | Static | OpenRailwayMap tiles |
| **Infrastructure** | ✅ Working | Every 15 min | Status monitoring |
| **Commodities** | ⚠️ Simulated | Every 15 min | Real APIs need keys |
| **AIS Vessels** | ❌ Pending | - | Requires AISstream API key |
| **Scanner Transcripts** | ❌ Pending | - | Requires backend + ScannerTranscribe |

**Live Dashboard:** https://arandomguyhere.github.io/Baltimore-Intel/

---

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│           GitHub Actions (runs every 15 minutes)                 │
│                                                                  │
│   collect_data.py → Fetches from APIs → Writes JSON files        │
└─────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│                    docs/data/                                    │
│   amtrak.json │ news.json │ commodities.json │ infrastructure   │
└─────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│              GitHub Pages Dashboard                              │
│         Reads JSON files → Displays on map + panels              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Sources

### Working Now

| Source | API | What It Does |
|--------|-----|--------------|
| **Amtraker** | `api-v3.amtraker.com` | Tracks Amtrak trains near Baltimore |
| **Google-News-Scraper** | Your repo | Pulls news with entity extraction |
| **OpenRailwayMap** | Tile server | Shows rail network on map |

### Needs Configuration

| Source | Requirement | To Enable |
|--------|-------------|-----------|
| **AISstream** | API key | Add `AISSTREAM_API_KEY` secret |
| **Commodity APIs** | API keys | Add market data API keys |
| **Scanner Transcription** | Backend | Run ScannerTranscribe + backend |

---

## Quick Start

### View the Dashboard

Just visit: **https://arandomguyhere.github.io/Baltimore-Intel/**

Data updates automatically every 15 minutes via GitHub Actions.

### Run Data Collection Locally

```bash
cd baltimore_intel
pip install requests
python collect_data.py
```

### Run Full Stack (Docker)

```bash
docker-compose -f docker-compose.full.yml up -d
```

---

## Baltimore Port Coverage

### Terminals
| Terminal | Type | Coordinates |
|----------|------|-------------|
| Seagirt | Containers | 39.2558, -76.5528 |
| Dundalk | RoRo, Breakbulk | 39.2467, -76.5256 |
| CNX Marine | Coal Export | 39.2089, -76.5847 |
| Fairfield | Automobiles | 39.2156, -76.5678 |

### Rail
- **CSX** - Howard Street Tunnel (capacity bottleneck)
- **Norfolk Southern** - Bayview Yard
- **Amtrak NEC** - Penn Station

### Scanner Feeds (Broadcastify)
| Feed | ID |
|------|----|
| Baltimore Terminal Railroad | 43356 |
| CSX/NS Regional | 14954 |
| Baltimore Marine | 42710 |
| Coast Guard Sector | 31547 |

---

## Project Structure

```
Baltimore-Intel/
├── docs/                      # GitHub Pages dashboard
│   ├── index.html             # Main dashboard
│   └── data/                  # JSON data files (auto-updated)
│       ├── amtrak.json
│       ├── news.json
│       ├── commodities.json
│       └── infrastructure.json
├── baltimore_intel/           # Python modules
│   ├── collect_data.py        # Data collection script
│   ├── ais_integration.py     # AIS tracking (needs API key)
│   ├── rail_tracking.py       # Rail monitoring
│   ├── scanner_feeds.py       # Scanner config
│   ├── commodities.py         # Commodity tracking
│   └── intelligence_hub.py    # Correlation engine
├── Watcher/                   # Watcher engine (Django)
└── .github/workflows/
    └── collect-data.yml       # Scheduled data collection
```

---

## Related Projects

| Project | Description |
|---------|-------------|
| [Google-News-Scraper](https://github.com/arandomguyhere/Google-News-Scraper) | News aggregation with entity extraction |
| [AIS_Tracker](https://github.com/arandomguyhere/AIS_Tracker) | Vessel tracking dashboard |
| [ScannerTranscribe](https://github.com/arandomguyhere/ScannerTranscribe) | Scanner audio transcription |
| [geopolitical-threat-mapper](https://github.com/arandomguyhere/geopolitical-threat-mapper) | Threat visualization |

---

## Future Roadmap

- [ ] Add AISstream integration (needs API key)
- [ ] Connect ScannerTranscribe for live transcripts
- [ ] Real commodity price APIs
- [ ] TheHive/MISP integration for alerting
- [ ] Historical trend analysis

---

## Credits

- **Watcher Engine** - [Thales Group CERT](https://github.com/thalesgroup-cert/Watcher)
- **Amtraker** - [amtraker.com](https://amtraker.com/)
- **OpenRailwayMap** - [openrailwaymap.org](https://www.openrailwaymap.org/)
