import time
import re
import requests
import socket
from ipaddress import ip_address, ip_network
from utils import log_event
from utils import PORT_SERVICE_MAP, MAX_HTTP_BODY_SIZE, HTTP_TIMEOUT, HTTP_RATE_LIMIT
from exploits import check_ssl_certificate, calculate_ai_score

_grab_http_info_cache = {}

def _rate_limit():
	"""Pause between HTTP requests to avoid triggering WAF/IDS."""
	time.sleep(HTTP_RATE_LIMIT)

def grab_http_info(target, port=80, use_ssl=False):
	log_event("grab_http_info_start", target=target, port=port, use_ssl=use_ssl)
	global _grab_http_info_cache
	cache_key = (target, port, use_ssl)
	if cache_key in _grab_http_info_cache:
		log_event("grab_http_info_cache_hit", target=target, port=port, use_ssl=use_ssl)
		return _grab_http_info_cache[cache_key]
	scheme = "https" if use_ssl else "http"
	info = {"server": "", "headers": {}, "title": "", "technologies": []}
	try:
		_rate_limit()
		r = requests.get(
			f"{scheme}://{target}:{port}",
			timeout=HTTP_TIMEOUT,
			verify=False,
			allow_redirects=True
		)
		info["headers"] = dict(r.headers)
		info["server"] = r.headers.get("Server", "Unknown")
		body = r.text
		if len(body) > MAX_HTTP_BODY_SIZE:
			body = body[:MAX_HTTP_BODY_SIZE]
		title_match = re.search(r"<title>(.*?)</title>", body, re.IGNORECASE)
		if title_match:
			info["title"] = title_match.group(1)[:100]
		tech_headers = {
			"X-Powered-By": "framework",
			"X-AspNet-Version": ".NET",
			"X-Generator": "generator",
		}
		for header, label in tech_headers.items():
			if header in r.headers:
				info["technologies"].append(f"{label}: {r.headers[header]}")
		missing = []
		for sec_header in ("X-Frame-Options", "X-XSS-Protection", "Strict-Transport-Security", "Content-Security-Policy"):
			if sec_header not in r.headers:
				missing.append(sec_header)
		if missing:
			info["technologies"].append(f"Header sicurezza mancanti: {', '.join(missing)}")
		_grab_http_info_cache[cache_key] = info
		log_event("grab_http_info_success", target=target, port=port, use_ssl=use_ssl, headers=list(info["headers"].keys()))
	except requests.RequestException as e:
		log_event("grab_http_info_error", target=target, port=port, use_ssl=use_ssl, error=str(e))
	return info

def analyze_ports(target, open_ports):
	"""In-depth analysis of vulnerabilities for each open port."""
	vulns = []
	for port_info in open_ports:
		port = port_info["port"]
		banner = port_info["banner"]
		service = PORT_SERVICE_MAP.get(port, f"unknown-{port}")
		# ... (copy the logic of analyze_ports from the original file here)
	return vulns

def check_ip_scope(target):
	"""Detects if the target is a private or public IP and logs a warning."""
	try:
		addr = ip_address(target)
		private_ranges = [
			ip_network("10.0.0.0/8"),
			ip_network("172.16.0.0/12"),
			ip_network("192.168.0.0/16"),
			ip_network("127.0.0.0/8"),
		]
		is_private = any(addr in net for net in private_ranges)
		return is_private
	except ValueError:
		try:
			resolved = socket.gethostbyname(target)
			return check_ip_scope(resolved)
		except socket.gaierror:
			return None

def prioritize(vulns):
	"""Sort vulnerabilities by descending AI score."""
	for v in vulns:
		v["ai_score"] = calculate_ai_score(v)
	return sorted(vulns, key=lambda x: x["ai_score"], reverse=True)
# analyzer.py
"""Vulnerability analysis, scoring, HTTP info."""

# Qui andranno: analyze_ports, grab_http_info, check_ip_scope, prioritize, _rate_limit
