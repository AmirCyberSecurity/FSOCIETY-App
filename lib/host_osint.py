import socket
import requests

def site_exists(domain) -> bool:
    try:
        socket.getaddrinfo(domain, None)
        return True
    except socket.gaierror:
        return False

def safe_get_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return None


def detect_protection(h):
    result = []
    try:
        r = requests.get(
            f"http://{h}",               
            timeout=0.5,                
            headers={"User-Agent": "Mozilla/5.0"},
            allow_redirects=False        
        )

        headers = {k.lower(): v.lower() for k, v in r.headers.items()}
        cookies = r.cookies.get_dict()

        server = headers.get("server", "")
        via = headers.get("via", "")

        if "cloudflare" in server or "cf-ray" in headers:
            result.append("Cloudflare")

        if "akamai" in server or "akamai" in via:
            result.append("Akamai")

        if "fastly" in server:
            result.append("Fastly")

        if "sucuri" in server or "x-sucuri-id" in headers:
            result.append("Sucuri WAF")

        if "imperva" in server or "incapsula" in server:
            result.append("Imperva / Incapsula")

        if "varnish" in via:
            result.append("Varnish Cache")

        if any(k.startswith("__cf") for k in cookies):
            result.append("Cloudflare (cookies)")

        if any("incap" in k for k in cookies):
            result.append("Imperva (cookies)")

        if any("ak_bmsc" in k for k in cookies):
            result.append("Akamai (cookies)")

        if r.status_code in (403, 429):
            result.append("WAF detected (behavioral)")

    except:
        return "UNKNOWN_ERROR"

    if not result:
        return "No obvious protection"

    return ", ".join(sorted(set(result)))


def get_ip_host_data(ip) -> dict:
    result = {
        "country": "Unknown",
        "city": "Unknown",
        "org": "Unknown",
        "isp": "Unknown"
    }

    try:
        r = requests.get(
            f"http://ip-api.com/json/{ip}?fields=status,country,city,isp,org",
            timeout=0.5
        )

        data = r.json()

        if data.get("status") != "success":
            return result

        result["country"] = data.get("country", "Unknown")
        result["city"] = data.get("city", "Unknown")
        result["org"] = data.get("org", "Unknown")
        result["isp"] = data.get("isp", "Unknown")

        return result

    except:
        return result
