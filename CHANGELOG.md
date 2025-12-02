# Changelog

All notable changes to OverWatch will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-12-02

### Added
- Initial release of OverWatch
- Real-time system monitoring dashboard
- CPU, memory, disk, network, and process monitoring
- Plugin system for extensibility
- Alert system with email and Telegram notifications
- REST API with FastAPI
- WebSocket support for real-time data streaming
- CLI interface with multiple commands
- Cross-platform support (Linux, macOS, Windows)
- Comprehensive documentation

### Features
- `overwatch start` - Launch terminal dashboard
- `overwatch api` - Start API server
- `overwatch version` - Show version info
- `overwatch info` - Display system information
- `overwatch plugins` - List available plugins
- `overwatch metrics` - Show current metrics

### Core Modules
- CPU monitoring with per-core statistics
- Memory (RAM and Swap) monitoring
- Disk usage and I/O statistics
- Network I/O and connection tracking
- Process management and monitoring
- Temperature sensor support

### API Endpoints
- `/metrics` - All system metrics
- `/metrics/cpu` - CPU metrics
- `/metrics/memory` - Memory metrics
- `/metrics/disk` - Disk metrics
- `/metrics/network` - Network metrics
- `/metrics/processes` - Process list
- `/metrics/sensors` - Sensor data
- `/ws` - WebSocket endpoint

[0.1.0]: https://github.com/sudoyasir/overwatch/releases/tag/v0.1.0
