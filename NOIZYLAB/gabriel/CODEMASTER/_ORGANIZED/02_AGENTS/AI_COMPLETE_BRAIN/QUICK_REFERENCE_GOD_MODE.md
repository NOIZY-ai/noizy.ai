# QUICK REFERENCE (GOD MODE)
> [!IMPORTANT]
> **SYSADMIN DIRECTIVE:** FAILURE IS NOT AN OPTION. LATENCY IS DEATH.


## CLI Commands
| Command | Description |
|OS|---|
| `npm run start` | Start local dev server |
| `npm run deploy` | Deploy to Cloudflare |
| `npm test` | Run strict unit tests |
| `npm run lint` | Check code style |

## API Endpoints
- `POST /api/chat` - `{ message: string, agent?: string }`
- `POST /api/voice` - `{ audio_base64: string }`
- `GET /api/status` - Returns System Health

## Key Files
- `UNIFIED_AI_WORKER.ts` - Main Entry
- `wrangler.toml` - Config
- `deploy.sh` - Deploy Script

## Emergency
- **Stop All:** `npm run stop`
- **Rollback:** `npm run rollback`
- **Admin Contact:** `admin@noizylab.ai`

**PRINT THIS AND TAPE IT TO THE WALL.**
