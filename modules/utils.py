"""
Utility functions and constants for AI Red Team Bot.
"""

import logging

class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREY = "\033[90m"
    @staticmethod
    def severity(sev):
        return {
            "CRITICAL": C.RED + C.BOLD,
            "HIGH": C.RED,
            "MEDIUM": C.YELLOW,
            "LOW": C.BLUE,
        }.get(sev, C.GREY)

MAX_BANNER_SIZE = 1024
MAX_HTTP_BODY_SIZE = 65536
MAX_CONCURRENT_SCANS = 100
DEFAULT_MAX_BANNER_SIZE = 1024
DEFAULT_MAX_HTTP_BODY_SIZE = 65536
DEFAULT_MAX_CONCURRENT_SCANS = 100
DEFAULT_TARGET_PORTS = [21, 22, 23, 25, 80, 443, 445, 3306, 5432, 6379, 27017, 3389, 5900, 8080, 8443]
DEFAULT_PORT_SERVICE_MAP = {
    21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp", 80: "http", 443: "https", 445: "smb",
    3306: "mysql", 5432: "postgresql", 6379: "redis", 27017: "mongodb", 3389: "rdp", 5900: "vnc",
    8080: "http-alt", 8443: "https-alt"
}
DEFAULT_COMMON_PATHS = ["/admin", "/login", "/.git", "/config", "/backup", "/test"]

logger = logging.getLogger("PhantomStrike AI")
SCAN_TIMEOUT = 3.0
HTTP_TIMEOUT = 5.0

def log_event(event, **kwargs):
    logger.info(f"[EVENT] {event} | {kwargs}")
