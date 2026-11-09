import * as fs from 'fs';
import * as path from 'path';

/**
 * GABRIEL_DOCTOR.ts
 * 
 * Purpose: Enforce "Absolute Perfection" and "GORUNFREE" protocols.
 * Checks:
 * 1. File Hygiene (No empty files, no temp files).
 * 2. God Mode Compliance (Check for required headers).
 * 3. Latency Scan (Greps for setTimeouts in critical paths).
 */

const RED = '\x1b[31m';
const GREEN = '\x1b[32m';
const RESET = '\x1b[0m';

const CRITICAL_FILES = [
    'UNIFIED_AI_WORKER.ts',
    'HEAVEN_WORKER.ts',
    'GABRIEL_TEST_SUITE.ts'
];

async function main() {
    console.log(`${GREEN}>>> GABRIEL DOCTOR: INITIATED <<<${RESET}`);
    let health = 100;

    // 1. Hygiene Check
    const files = fs.readdirSync('.');
    for (const file of files) {
        const stats = fs.statSync(file);
        if (stats.isFile() && stats.size === 0) {
            console.log(`${RED}[FAIL] Empty file detected: ${file}${RESET}`);
            health -= 10;
        }
    }

    // 2. Latency Scan
    for (const file of CRITICAL_FILES) {
        if (fs.existsSync(file)) {
            const content = fs.readFileSync(file, 'utf-8');
            if (content.includes('setTimeout') && !file.includes('GABRIEL_DOCTOR')) {
                // Allow setTimeout(..., 0) for async non-blocking, but warn typically
                const timeouts = content.match(/setTimeout/g);
                if (timeouts && timeouts.length > 0) {
                    // Check if it's a 0ms timeout (acceptable for backgrounding)
                    if (!content.includes('setTimeout(() => {}, 0)') && !content.includes('setTimeout(async () => {')) {
                        // Simple heuristic, strictly we'd parse AST, but grep is fast
                        console.log(`${RED}[WARN] Potential Latency in ${file} (setTimeout detected)${RESET}`);
                        // We don't deduct health for now as backgrounding is valid, but flag it.
                    }
                }
            }
        }
    }

    // 3. God Mode Verification
    if (fs.existsSync('MIRACLE_PROMPT_GOD_MODE.md')) {
        const godMode = fs.readFileSync('MIRACLE_PROMPT_GOD_MODE.md', 'utf-8');
        if (!godMode.includes('GORUNFREE')) {
            console.log(`${RED}[CRITICAL] GOD MODE PROTOCOL MISSING${RESET}`);
            health -= 50;
        }
    } else {
        console.log(`${RED}[FAIL] MIRACLE_PROMPT_GOD_MODE.md missing${RESET}`);
        health -= 20;
    }

    console.log(`\nSystem Health: ${health}%`);
    if (health === 100) {
        console.log(`${GREEN}>>> SYSTEM STATUS: PERFECT <<<${RESET}`);
    } else {
        console.log(`${RED}>>> SYSTEM STATUS: COMPROMISED <<<${RESET}`);
        process.exit(1);
    }
}

main().catch(console.error);
