import requests
import ipaddress




def checking(target_ip) -> bool:
    response = requests.get(f"http://ip-api.com/json/{target_ip}?fields=status,message,country,regionName,city,zip,lat,lon,timezone,isp,org,as,query")
    data = response.json()

    if data["status"] == "success":
        return True
    
    else: 
        return False

def get_ip(target_ip) -> str:
    response = requests.get(f"http://ip-api.com/json/{target_ip}?fields=status,message,country,regionName,city,zip,lat,lon,timezone,isp,org,as,query")
    data = response.json()

    return f"IP: {data['query']}"

def get_country(target_ip) -> str:
    response = requests.get(f"http://ip-api.com/json/{target_ip}?fields=status,message,country,regionName,city,zip,lat,lon,timezone,isp,org,as,query")
    data = response.json()

    return f"COUNTRY: {data['country']}"


def get_city(target_ip) -> str:
    response = requests.get(f"http://ip-api.com/json/{target_ip}?fields=status,message,country,regionName,city,zip,lat,lon,timezone,isp,org,as,query")
    data = response.json()

    return f"CITY: {data['city']}"

def get_isp(target_ip) -> str:
    response = requests.get(f"http://ip-api.com/json/{target_ip}?fields=status,message,country,regionName,city,zip,lat,lon,timezone,isp,org,as,query")
    data = response.json()

    return f"ISP: {data['isp']}"


def get_org(target_ip) -> str:
    response = requests.get(f"http://ip-api.com/json/{target_ip}?fields=status,message,country,regionName,city,zip,lat,lon,timezone,isp,org,as,query")
    data = response.json()

    if data["org"] != "":
        return f"ORG: {data['org']}"
    
    else:
        return f"ORG: None"


def get_cords(target_ip) -> str:
    response = requests.get(f"http://ip-api.com/json/{target_ip}?fields=status,message,country,regionName,city,zip,lat,lon,timezone,isp,org,as,query")
    data = response.json()

    return f"COORDS: {data['lat']}, {data['lon']}"


def get_ip_type(target_ip):
    ip = ipaddress.ip_address(target_ip)

    if ip.is_private:
        ip_type = "PRIVATE"
    elif ip.is_loopback:
        ip_type = "LOOPBACK"
    elif ip.is_reserved:
        ip_type = "RESERVED"
    elif ip.is_multicast:
        ip_type = "MULTICAST"
    elif ip.is_link_local:
        ip_type = "LINK_LOCAL"
    else:
        ip_type = "PUBLIC"
    
    return f"IP TYPE: {ip_type}"