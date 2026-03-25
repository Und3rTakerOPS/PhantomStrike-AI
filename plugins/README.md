# Plugin System

The bot now supports a Python plugin system automatically loaded from the `plugins/` directory.

## How it works
- Each `.py` file in `plugins/` is loaded at startup.
- Each plugin must expose a `register(bot)` function.
- Through the `bot` object you can register custom exploits:

```python
def register(bot):
    def my_exploit(target, port=80):
        # custom logic
        return True, "Custom result"
    bot.register_exploit("my_exploit", my_exploit)
```

## Available API
- `bot.register_exploit(name, function)` — Registers an exploit callable from the core.
- `bot.run_exploit(name, *args, **kwargs)` — Runs a registered exploit.

## CLI
- Use `--plugins-dir` to specify an alternative plugin directory.

## Quick example
See `plugins/ftp_weakpass.py` for a basic example.

## Notes
- Plugins are loaded BEFORE the scan execution.
- Plugins can add exploits, scanners, report exporters, etc.
- Plugin loading errors are logged but do not block execution.
