# Phase 5 验收单（抗滥用加固：上传限制 + 写接口限流）

本阶段目标（仍然非破坏）：
- 降低超大上传或高频写请求导致的服务不稳定风险

## 已做内容
1) 上传大小限制（默认 20MB）
- 新增环境变量：`STAR_OFFICE_MAX_UPLOAD_MB=20`
- 超限返回 `413 PAYLOAD_TOO_LARGE`

2) 写接口限流（默认 60 次/60 秒，按 IP+路径）
- 新增环境变量：`STAR_OFFICE_WRITE_RATE_LIMIT=60,60`
- 触发限流返回 `429 RATE_LIMITED`，带 `Retry-After`

3) 配置与检查同步
- `.env.example` 增加上述配置
- `scripts/security_check.py` 增加格式与阈值检查

## 验收方式（线上可见）
- 正常使用无变化（状态切换、join/push、资产操作仍正常）
- 异常行为才会被拦截（超大上传 / 恶意高频请求）

## 回滚
- 临时回滚：提高限制值（或恢复默认）
- 代码回滚：`git revert <phase5_commit>`
