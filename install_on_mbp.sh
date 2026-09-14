# Trên MBP, merge vào ~/.nanobot/config.json (đã có provider vilao):
python3 -c "
import json, pathlib
p = pathlib.Path.home()/'.nanobot/config.json'
cfg = json.loads(p.read_text())
mcp = cfg.setdefault('mcp_servers', {})
mcp['hermes-brain-bridge'] = {
  'url': 'https://crawbot-master-9.taild7e69a.ts.net:9111/mcp',
  'transport': 'streamableHttp',
  'auth': {'type':'bearer','token':'4b283c2fb22f77aaa7b3290aed8abf4cea74974cf65f2ce7799a318896545b6b'},
  'description': 'Hermes Brain Bridge — 18 tools'
}
p.write_text(json.dumps(cfg, indent=2))
print('mcp_servers updated:', list(mcp.keys()))
"
# restart gateway để nạp:
nanobot gateway restart --config ~/.nanobot/config.json --workspace ~/nanobot/ws
# verify:
curl -s -H 'Authorization: Bearer 4b283c2fb22f77aaa7b3290aed8abf4cea74974cf65f2ce7799a318896545b6b' \
  https://crawbot-master-9.taild7e69a.ts.net:9111/health
