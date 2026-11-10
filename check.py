import os, json, urllib.request, urllib.parse

URL = ("https://www.maquillajetrendyshop.com/api/catalog_system/pub/products/search?ft="
       + urllib.parse.quote("aura"))
req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
data = json.load(urllib.request.urlopen(req, timeout=30))
found = [p for p in data if "adviento" in p.get("productName", "").lower()]
print(len(data), "resultados;", len(found), "con 'aura'")

if found:
    p = found[0]
    topic = os.environ["NTFY_TOPIC"]
    headers = {"Title": "Trendy", "Priority": "urgent"}
    if p.get("link"):
        headers["Click"] = p["link"]
    msg = "Salio: " + p["productName"]
    urllib.request.urlopen(urllib.request.Request(
        "https://ntfy.sh/" + topic, data=msg.encode("utf-8"), headers=headers), timeout=30)
