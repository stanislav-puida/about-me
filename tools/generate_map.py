"""Generate a Leaflet HTML map using Python's standard library.

Run: python3 tools/generate_map.py
Edit journey.json to change the locations and popup descriptions.
Coordinates are approximate city centres, not private addresses.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
places = json.loads((ROOT / 'journey.json').read_text(encoding='utf-8'))
template = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>My journey map</title>
<link rel="stylesheet" href="assets/leaflet.css">
<style>html,body{margin:0;height:100%;font:14px Arial,sans-serif;color:#111111}body{display:flex;flex-direction:column}#map{flex:1;min-height:220px;background:#f4f4f4}.controls{padding:12px;display:flex;gap:7px;flex-wrap:wrap;background:white;border-bottom:1px solid #dddddd}button{font:inherit;border:1px solid #cccccc;border-radius:4px;background:white;color:#111111;padding:8px 10px;cursor:pointer}button:hover,button[aria-pressed=true]{background:#111111;color:white}button:focus-visible{outline:3px solid #111111;outline-offset:2px}.leaflet-popup-content{font:14px/1.6 Arial,sans-serif}.leaflet-popup-content strong{font-size:17px}#status{padding:9px 12px;font-size:12px;line-height:1.5;background:#f5f5f5}.leaflet-control-attribution{font-size:11px}.leaflet-tile-pane{filter:grayscale(100%)}.leaflet-control-attribution a{color:#111}.leaflet-container a.leaflet-popup-close-button{color:#111}</style></head>
<body><div class="controls" role="group" aria-label="Journey map locations"><button id="all" aria-pressed="true">Full journey</button></div><div id="map" role="region" aria-label="Journey map"></div><div id="status" aria-live="polite" hidden></div><noscript>Enable JavaScript to explore the map. The full journey is described on the main page.</noscript><script src="assets/leaflet.js"></script><script>
const places = __PLACES__;
const status = document.getElementById('status');
if(typeof L === 'undefined'){status.hidden=false;status.textContent='The map could not load. You can read the full journey on the main page.';}else{
const map = L.map('map',{scrollWheelZoom:false});
const tiles = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',{maxZoom:19,attribution:'Tiles &copy; Esri | Sources: Esri, HERE, Garmin, USGS, Intermap, INCREMENT P, NRCan, Esri Japan, METI, Esri China (Hong Kong), Esri Korea, Esri (Thailand), NGCC, &copy; OpenStreetMap contributors and the GIS User Community'}).addTo(map);
tiles.on('tileerror',()=>{status.hidden=false;status.textContent='Background tiles are unavailable. The city markers and journey descriptions still work.'});
const bounds=L.latLngBounds(places.map(p=>[p.lat,p.lon]));
function fit(){map.fitBounds(bounds,{padding:[35,35]});}
const markers = places.map(p=>{
  const box=document.createElement('div');
  const title=document.createElement('strong');title.textContent=p.city;box.append(title);
  const text=document.createElement('p');text.textContent=p.country+' | '+p.story;box.append(text);
  return L.circleMarker([p.lat,p.lon],{radius:8,color:'#fff',weight:3,fillColor:'#111111',fillOpacity:1}).addTo(map).bindPopup(box);
});
// Kaunas appears twice in the path: before and after the Erasmus semester.
const route=['Luhansk','Kharkiv','Kremenchuk','Poznań','Kaunas','Brno','Kaunas','Berlin'];
const path=route.map(city=>places.find(p=>p.city===city)).map(p=>[p.lat,p.lon]);
L.polyline(path,{color:'#111111',weight:3,dashArray:'6 8',opacity:.75}).addTo(map);
function selected(button){document.querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));}
places.forEach((p,i)=>{const button=document.createElement('button');button.textContent=p.city;button.setAttribute('aria-pressed','false');button.addEventListener('click',()=>{selected(button);map.setView([p.lat,p.lon],6);markers[i].openPopup();});document.querySelector('.controls').append(button);});
document.getElementById('all').addEventListener('click',e=>{selected(e.currentTarget);map.closePopup();fit();status.hidden=true;status.textContent='';});
fit();
}
</script></body></html>'''
output = ROOT.parent / 'map.html'
output.parent.mkdir(exist_ok=True)
output.write_text(template.replace('__PLACES__', json.dumps(places, ensure_ascii=False).replace('<', '\\u003c')), encoding='utf-8')
print(f'Generated {output}')
