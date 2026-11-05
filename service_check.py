import requests
import time

services = {
    "discord": "https://discord.com/",
    "youtube": "https://www.youtube.com/",
    "github": "https://github.com/",
    "telegram": "https://web.telegram.org/",
    "claude": "https://claude.ai"
}
def serviceget():
    resu = {}
    for name, url in services.items():
        try:
            start = time.time()

            response = requests.get(
                url,
                timeout=10,
                allow_redirects=True
            )
            elapsed = round(time.time() - start, 2)
            resu[name] = {"status": response.status_code, "time": elapsed, "error": None}
        except requests.exceptions.RequestException as e:
            resu[name] = {"status": "connection error", "time": None, "error": str(e)}
    return resu
