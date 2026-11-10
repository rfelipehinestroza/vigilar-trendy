import os, json, urllib.request, urllib.parse

# --- Lo único que cambias ---
BUSQUEDA = "gloss"
PALABRAS = ("gloss")
# ----------------------------

URL = ("https://www.maquillajetrendyshop.com/api/catalog_system/pub/products/search?ft="
       + urllib.parse.quote(BUSQUEDA))
req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
data = json.load(urllib.request.urlopen(req, timeout=30))
found = [p for p in data
         if any(w in p.get("productName", "").lower() for w in PALABRAS)]
print(len(data), "resultados;", len(found), "coinciden")

if found:
    p = found[0]
    topic = os.environ["NTFY_TOPIC"]
    headers = {"Title": "Trendy", "Priority": "urgent"}
    if p.get("link"):
        headers["Click"] = p["link"]
    msg = "Salio: " + p["productName"]
    urllib.request.urlopen(urllib.request.Request(
        "https://ntfy.sh/" + topic, data=msg.encode("utf-8"), headers=headers), timeout=30)
