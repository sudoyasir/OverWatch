# OverWatch 🔭

**Advanced System Monitoring CLI Tool**

OverWatch is a powerful, terminal-based system monitor built with Python. It provides real-time monitoring of CPU, memory, disk, network, and processes with a beautiful Rich/Textual UI, plugin support, configurable alerts, and a RESTful API.

![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

---

## 🌟 Features

- **📊 Real-time Dashboard**: Beautiful terminal UI powered by Rich
- **🔌 Plugin System**: Extensible architecture for custom monitoring modules
- **🚨 Smart Alerts**: Threshold-based notifications via Email and Telegram
- **🌐 REST API**: FastAPI server with WebSocket support for real-time data
- **🖥️ Cross-Platform**: Works on Linux, macOS, and Windows
- **⚡ Performance Monitoring**:
  - CPU usage (overall & per-core)
  - Memory (RAM & Swap)
  - Disk usage & I/O
  - Network statistics
  - Process details
  - Temperature sensors (when available)

---

## 📦 Installation

### Quick Install with Virtual Environment (Recommended)

```bash
git clone https://github.com/sudoyasir/overwatch.git
cd overwatch
./quick_setup.sh
source venv/bin/activate
```

### Manual Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install
pip install -e .
```

### Requirements

- Python 3.10 or higher
- pip package manager

### Dependencies

All dependencies are automatically installed:
- `psutil` - System and process utilities
- `rich` - Terminal UI
- `click` - CLI framework
- `fastapi` - API server
- `uvicorn` - ASGI server
- `requests` - HTTP client
- `websockets` - WebSocket support

---

## 🚀 Quick Start

**Note**: Always activate the virtual environment first:
```bash
source venv/bin/activate
```

### Launch Terminal Dashboard

```bash
overwatch start
```

Options:
- `--refresh` or `-r`: Set refresh rate in seconds (default: 1.0)

Example:
```bash
overwatch start --refresh 0.5
```

### Start API Server

```bash
overwatch api
```

Options:
- `--host` or `-h`: Host address (default: 0.0.0.0)
- `--port` or `-p`: Port number (default: 8000)

Example:
```bash
overwatch api --host 127.0.0.1 --port 9000
```

Access the API documentation at: `http://localhost:8000/docs`

### Other Commands

```bash
# Show version information
overwatch version

# Display system information
overwatch info

# List available plugins
overwatch plugins

# Show current metrics
overwatch metrics --format json
```

---

## 📡 API Endpoints

### REST API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API root |
| `/health` | GET | Health check |
| `/metrics` | GET | All system metrics |
| `/metrics/cpu` | GET | CPU metrics |
| `/metrics/memory` | GET | Memory metrics |
| `/metrics/disk` | GET | Disk metrics |
| `/metrics/network` | GET | Network metrics |
| `/metrics/processes` | GET | Process list |
| `/metrics/sensors` | GET | Sensor data |
| `/process/{pid}` | GET | Specific process details |

### WebSocket

Connect to `/ws` for real-time metrics streaming (updates every second).

Example using JavaScript:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
ws.onmessage = (event) => {
    const metrics = JSON.parse(event.data);
    console.log(metrics);
};
```

---

## 🔌 Plugin Development

Create custom plugins to extend OverWatch functionality.

### Plugin Structure

1. Create a new Python file in `overwatch/plugins/`
2. Implement a `run()` function that returns a dict

### Example Plugin

```python
# overwatch/plugins/my_plugin.py

from typing import Dict, Any

def run() -> Dict[str, Any]:
    """
    Your plugin logic here.
    
    Returns:
        Dict with plugin name and data
    """
    return {
        "name": "My Custom Plugin",
        "data": {
            "status": "active",
            "value": 42
        },
        "status": "success",
    }

# Optional: Plugin metadata
PLUGIN_INFO = {
    "name": "My Plugin",
    "version": "1.0.0",
    "description": "Does something awesome",
    "author": "Your Name",
}
```

### Loading Plugins

Plugins are automatically discovered and loaded from the `overwatch/plugins/` directory. Use `overwatch plugins` to list all available plugins.

---

## 🚨 Alert Configuration

### Configure Thresholds

Edit `overwatch/alerts/thresholds.json`:

```json
{
  "cpu": {
    "threshold": 90,
    "enabled": true
  },
  "memory": {
    "threshold": 80,
    "enabled": true
  },
  "disk": {
    "threshold": 85,
    "enabled": true
  },
  "temperature": {
    "threshold": 80,
    "enabled": false
  }
}
```

### Email Notifications

Set environment variables:

```bash
export EMAIL_SMTP_SERVER="smtp.gmail.com"
export EMAIL_SMTP_PORT="587"
export EMAIL_SMTP_USERNAME="your-email@gmail.com"
export EMAIL_SMTP_PASSWORD="your-app-password"
export EMAIL_FROM="your-email@gmail.com"
export EMAIL_TO="recipient@example.com"
```

### Telegram Notifications

Set environment variables:

```bash
export TELEGRAM_BOT_TOKEN="your-bot-token"
export TELEGRAM_CHAT_ID="your-chat-id"
```

To create a Telegram bot:
1. Message [@BotFather](https://t.me/botfather)
2. Create a new bot with `/newbot`
3. Get your chat ID from [@userinfobot](https://t.me/userinfobot)

---

## 🏗️ Project Structure

```
overwatch/
├── core/                  # Monitoring modules
│   ├── cpu.py
│   ├── memory.py
│   ├── disk.py
│   ├── network.py
│   ├── processes.py
│   └── sensors.py
├── ui/                    # Dashboard UI
│   ├── dashboard.py
│   └── components/
│       ├── cpu_panel.py
│       ├── memory_panel.py
│       ├── disk_panel.py
│       ├── network_panel.py
│       └── process_panel.py
├── plugins/               # Plugin system
│   ├── __init__.py
│   └── example_plugin.py
├── alerts/                # Alert system
│   ├── manager.py
│   ├── telegram.py
│   ├── email.py
│   └── thresholds.json
├── api/                   # REST API
│   ├── server.py
│   └── websocket.py
├── cli/                   # CLI interface
│   ├── main.py
│   └── commands.py
├── utils/                 # Utilities
│   ├── loader.py
│   └── system_info.py
└── overwatch.py          # Main entry point
```

---

## 🖼️ Screenshots

![Dashboard Screenshot](./gh-assets/dashboard.png)

---

## 🧪 Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/sudoyasir/overwatch.git
cd overwatch

# Install in development mode
pip install -e .

# Run tests (if available)
pytest
```

### Run from Source

```bash
python -m overwatch.cli.main start
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Built with [psutil](https://github.com/giampaolo/psutil) for system monitoring
- UI powered by [Rich](https://github.com/Textualize/rich)
- API built with [FastAPI](https://fastapi.tiangolo.com/)

---

## 📧 Contact

For questions, issues, or suggestions:
- GitHub Issues: https://github.com/sudoyasir/overwatch/issues
- Email: info@overwatch.dev

---

**Made with ❤️ by the OverWatch Team**
