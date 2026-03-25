# =========================
# RECON (ASYNC PORT SCAN + BANNER GRABBING)
# =========================
import asyncio
from utils import log_event

MAX_BANNER_SIZE = 4096
MAX_CONCURRENT_SCANS = 10
TARGET_PORTS = [21, 22, 23, 80, 443, 445, 3389, 8080]

_scan_port_cache = {}

async def scan_port(target, port, timeout=3.0):
	"""Scans a single port and attempts banner grabbing."""
	log_event("scan_port_start", target=target, port=port)
	cache_key = (target, port)
	if cache_key in _scan_port_cache:
		log_event("scan_port_cache_hit", target=target, port=port)
		return _scan_port_cache[cache_key]
	try:
		reader, writer = await asyncio.wait_for(
			asyncio.open_connection(target, port),
			timeout=timeout
		)
		banner = ""
		try:
			writer.write(b"\r\n")
			await writer.drain()
			data = await asyncio.wait_for(reader.read(MAX_BANNER_SIZE), timeout=2)
			banner = data.decode("utf-8", errors="ignore").strip()
			if len(banner) > MAX_BANNER_SIZE:
				banner = banner[:MAX_BANNER_SIZE]
		except (asyncio.TimeoutError, ConnectionError):
			pass

		writer.close()
		try:
			await writer.wait_closed()
		except (ConnectionError, OSError):
			pass

		result = {"port": port, "open": True, "banner": banner}
		_scan_port_cache[cache_key] = result
		log_event("scan_port_success", target=target, port=port, open=True, banner=banner)
		return result
	except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
		result = {"port": port, "open": False, "banner": ""}
		_scan_port_cache[cache_key] = result
		log_event("scan_port_closed", target=target, port=port, open=False)
		return result

async def scan_target(target):
	"""Scans all configured ports in parallel."""
	semaphore = asyncio.Semaphore(MAX_CONCURRENT_SCANS)
	async def sem_scan_port(port):
		async with semaphore:
			return await scan_port(target, port)
	tasks = [sem_scan_port(p) for p in TARGET_PORTS]
	results = await asyncio.gather(*tasks)
	open_ports = [r for r in results if r["open"]]
	return open_ports
# scanner.py
"""Modules for port scanning and banner grabbing."""

import asyncio

# Qui andranno: scan_port, scan_target, _scan_port_cache, costanti correlate
