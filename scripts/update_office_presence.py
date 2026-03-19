#!/usr/bin/env python3
import json
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'office-agents.json'
SYNC = ROOT / 'scripts' / 'sync_managed_agents.py'

CHECKS = {
    'mission-control': ('http://127.0.0.1:3002/', 'syncing', 'Mission Control operativo'),
    'health-hub': ('http://127.0.0.1:3114/', 'idle', 'Health Hub disponible'),
    'investment-hub': ('http://127.0.0.1:3012/', 'error', 'Investment Hub caído o no levantado'),
    'inmobiliaria-core': ('http://127.0.0.1:8011/', 'error', 'Inmobiliaria Core caída o no levantada'),
    'web-content-factory': ('http://127.0.0.1:8008/', 'error', 'Web Content Factory caída o no levantada'),
}


def up(url: str) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=2.5) as r:
            return r.status < 500
    except Exception:
        return False


def main():
    data = json.loads(CONFIG.read_text(encoding='utf-8'))
    main = data.get('main', {})
    mc_up = up('http://127.0.0.1:3002/')
    main['state'] = 'syncing' if mc_up else 'error'
    main['detail'] = 'Coordinando Mission Control y la oficina' if mc_up else 'Mission Control no responde'
    data['main'] = main

    for agent in data.get('agents', []):
        key = agent.get('agentId')
        if key not in CHECKS:
            continue
        url, state_up, detail_up = CHECKS[key]
        if up(url):
            agent['state'] = state_up
            agent['detail'] = detail_up
        else:
            agent['state'] = 'error'
            agent['detail'] = CHECKS[key][2] if 'caído' in CHECKS[key][2] else f'{agent.get("name", key)} no responde'

    CONFIG.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print('updated office-agents.json')

    import subprocess
    subprocess.check_call(['/usr/local/bin/python3.12', str(SYNC)])


if __name__ == '__main__':
    main()
