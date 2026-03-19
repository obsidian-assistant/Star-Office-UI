#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "office-agents.json"
STATE_PATH = ROOT / "state.json"
AGENTS_PATH = ROOT / "agents-state.json"

AVATARS = [
    "guest_role_1",
    "guest_role_2",
    "guest_role_3",
    "guest_role_4",
    "guest_role_5",
    "guest_role_6",
]

STATE_TO_AREA = {
    "idle": "breakroom",
    "writing": "writing",
    "researching": "writing",
    "executing": "writing",
    "syncing": "writing",
    "error": "error",
}


def area_for(state: str) -> str:
    return STATE_TO_AREA.get((state or "idle").strip(), "breakroom")


def main():
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    now = datetime.now().isoformat()

    main_cfg = data.get("main", {})
    main_state = {
        "state": main_cfg.get("state", "idle"),
        "detail": main_cfg.get("detail", "Waiting..."),
        "progress": 0,
        "updated_at": now,
        "officeName": "Oficina de Atlas",
    }
    STATE_PATH.write_text(json.dumps(main_state, ensure_ascii=False, indent=2), encoding="utf-8")

    agents = [
        {
            "agentId": main_cfg.get("agentId", "atlas"),
            "name": main_cfg.get("name", "Atlas"),
            "isMain": True,
            "state": main_cfg.get("state", "idle"),
            "detail": main_cfg.get("detail", "En espera"),
            "updated_at": now,
            "area": area_for(main_cfg.get("state", "idle")),
            "source": "local-managed",
            "joinKey": None,
            "authStatus": "approved",
            "authExpiresAt": None,
            "lastPushAt": now,
        }
    ]

    for idx, item in enumerate(data.get("agents", [])):
        state = item.get("state", "idle")
        agents.append({
            "agentId": item["agentId"],
            "name": item.get("name", item["agentId"]),
            "isMain": False,
            "state": state,
            "detail": item.get("detail", "Disponible"),
            "updated_at": now,
            "area": area_for(state),
            "source": "local-managed",
            "joinKey": "managed-local",
            "authStatus": "approved",
            "authApprovedAt": now,
            "authExpiresAt": None,
            "lastPushAt": now,
            "avatar": AVATARS[idx % len(AVATARS)],
        })

    AGENTS_PATH.write_text(json.dumps(agents, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"synced {len(agents)} agents")


if __name__ == "__main__":
    main()
