# Home Assistant Diagnostics Helper

This add-on helps identify and troubleshoot issues in your Home Assistant installation by monitoring system health, analyzing logs, and checking configurations.

## Features

- System health monitoring (CPU, memory, disk usage)
- Log analysis for errors and warnings
- Configuration file validation
- Real-time diagnostics
- Periodic health checks

## Installation

1. Add this repository to your Home Assistant Add-on Store
2. Install the "HA Diagnostics Helper" add-on
3. Configure the add-on (see configuration options below)
4. Start the add-on

## Configuration

```yaml
log_level: info
scan_interval: 300
```

### Option: `log_level`

The `log_level` option controls the level of log output by the add-on:

- `trace`: Show every detail
- `debug`: Shows detailed debug information
- `info`: Normal information
- `warning`: Only warnings and errors
- `error`: Only errors
- `critical`: Only critical errors

### Option: `scan_interval`

The `scan_interval` option controls how often (in seconds) the add-on performs diagnostics checks. Default is 300 seconds (5 minutes).

## Support

For issues and feature requests, please open an issue on GitHub.