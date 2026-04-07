import phonenumbers
from phonenumbers import geocoder, carrier, timezone, PhoneNumberFormat, format_number

type_map = {
    0: "FIXED_LINE",
    1: "MOBILE",
    2: "FIXED_OR_MOBILE",
    3: "TOLL_FREE",
    4: "PREMIUM_RATE",
    5: "SHARED_COST",
    6: "VOIP"
}


def is_valid(phone_number) -> bool:
    raw = phone_number
    raw = raw.replace("＋", "+")
    raw = raw.replace("\u200e", "").replace("\u200f", "").replace("\u00a0", "")
    clean = "".join(c for c in raw if c.isdigit() or c == "+")

    while clean.startswith("++"):
        clean = clean[1:]

    if clean.startswith("+8"):
        clean = "+7" + clean[2:]

    if clean.startswith("8") and len(clean) == 11:
        clean = "+7" + clean[1:]

    if not clean.startswith("+"):
        clean = "+7" + clean

    return len(clean) >= 8


def parse_check(phone_number) -> bool:
    raw = phone_number
    raw = raw.replace("＋", "+")
    raw = raw.replace("\u200e", "").replace("\u200f", "").replace("\u00a0", "")
    clean = "".join(c for c in raw if c.isdigit() or c == "+")

    while clean.startswith("++"):
        clean = clean[1:]

    if clean.startswith("+8"):
        clean = "+7" + clean[2:]

    if clean.startswith("8") and len(clean) == 11:
        clean = "+7" + clean[1:]

    if not clean.startswith("+"):
        clean = "+7" + clean

    try:
        phonenumbers.parse(clean, None)
    except Exception:
        return False

    return True


def get_data(parsed) -> dict:
    data = {}

    if isinstance(parsed, str):
        try:
            parsed = phonenumbers.parse(parsed, None)
        except Exception:
            return {
                "country": "Unknown",
                "region": "Unknown",
                "operator": "Unknown",
                "country_code": "Unknown",
                "national_number": "Unknown",
                "intl": "Unknown",
                "local": "Unknown",
                "e164": "Unknown",
                "is_possible": "NO",
                "is_valid": "NO",
                "line_type": "UNKNOWN",
                "tz": "MOBILE_RANGE",
                "tz_list": "Unknown"
            }

    tz_list = timezone.time_zones_for_number(parsed)
    n_type = phonenumbers.number_type(parsed)

    data["country"] = geocoder.country_name_for_number(parsed, "en") or "Unknown"
    data["region"] = geocoder.description_for_number(parsed, "en") or "Unknown"
    data["operator"] = carrier.name_for_number(parsed, "en") or "Unknown"

    data["country_code"] = parsed.country_code
    data["national_number"] = parsed.national_number

    data["intl"] = format_number(parsed, PhoneNumberFormat.INTERNATIONAL)
    data["local"] = format_number(parsed, PhoneNumberFormat.NATIONAL)
    data["e164"] = format_number(parsed, PhoneNumberFormat.E164)

    data["is_possible"] = "YES" if phonenumbers.is_possible_number(parsed) else "NO"
    data["is_valid"] = "YES" if phonenumbers.is_valid_number(parsed) else "NO"

    data["line_type"] = type_map.get(n_type, "UNKNOWN")

    data["tz"] = tz_list[0] if tz_list else "MOBILE_RANGE"
    data["tz_list"] = ", ".join(tz_list) if tz_list else "Unknown"

    return data
