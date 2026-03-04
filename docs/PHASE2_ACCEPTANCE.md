# Phase 2 验收单（安全加固：可开关、非破坏）

本阶段目标：
- 不删功能
- 默认行为不变
- 新增“可开关”的写接口 Bearer 鉴权

## 已交付
1. 后端新增可选安全开关：
- `STAR_OFFICE_WRITE_API_BEARER_ENABLED`（默认 false）
- `STAR_OFFICE_WRITE_API_TOKENS`（逗号分隔 token）

2. 受保护写接口（开关开启后生效）：
- `POST /set_state`
- `POST /join-agent`
- `POST /leave-agent`
- `POST /agent-push`
- `POST /agent-approve`
- `POST /agent-reject`

3. 文档与安全检查增强：
- `.env.example` 增加配置说明
- `scripts/security_check.py` 增加对应检查提示

## 你可在公网直接验收（推荐）
### A. 默认兼容（不开启）
- 现网不改环境变量时，功能应与之前一致。

### B. 安全开关测试（你确认后再开）
1) 设置环境变量并重启服务：
```bash
STAR_OFFICE_WRITE_API_BEARER_ENABLED=true
STAR_OFFICE_WRITE_API_TOKENS=your-long-random-token
```
2) 验证：
- 不带 `Authorization: Bearer ...` 调用上述 POST，应返回 401
- 带正确 Bearer，应正常
- 页面浏览（GET）不受影响

## 回滚方式
- 立即回滚：把 `STAR_OFFICE_WRITE_API_BEARER_ENABLED` 改回 false 并重启
- 代码回滚：`git revert <phase2_commit>`
