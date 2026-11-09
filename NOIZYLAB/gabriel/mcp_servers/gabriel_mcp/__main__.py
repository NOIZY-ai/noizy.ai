#!/usr/bin/env python3
"""
GABRIEL MCP v2 — Direct Execution Entry Point
===============================================
Run with: python -m gabriel_mcp

Modes:
  python -m gabriel_mcp          # Start MCP server (stdio)
  python -m gabriel_mcp test     # Run test suite
  python -m gabriel_mcp status   # Show server status
  python -m gabriel_mcp demo     # Run demo session
"""

import asyncio
import sys
from pathlib import Path

# Ensure package is importable
sys.path.insert(0, str(Path(__file__).parent.parent))


def run_server():
    """Run the MCP server."""
    from gabriel_mcp.server import main
    asyncio.run(main())


def run_tests():
    """Run the test suite."""
    import subprocess
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-v", str(Path(__file__).parent / "tests")],
        cwd=str(Path(__file__).parent.parent),
    )
    sys.exit(result.returncode)


def show_status():
    """Show server configuration and status."""
    from gabriel_mcp.config import (
        NOIZYLAB_ROOT, GABRIEL_ROOT, MCP_ROOT,
        DATA_DIR, STATE_DIR, CHARACTERS_DIR,
        SERVER_NAME, SERVER_VERSION,
    )
    from gabriel_mcp.pipeline.processor import AudioProcessor

    print(f"""
GABRIEL MCP v{SERVER_VERSION}
{'=' * 40}

Paths:
  NOIZYLAB_ROOT:  {NOIZYLAB_ROOT}
  GABRIEL_ROOT:   {GABRIEL_ROOT}
  MCP_ROOT:       {MCP_ROOT}
  DATA_DIR:       {DATA_DIR}
  STATE_DIR:      {STATE_DIR}
  CHARACTERS_DIR: {CHARACTERS_DIR}

Characters Available:
""")

    # List characters
    if CHARACTERS_DIR.exists():
        for f in sorted(CHARACTERS_DIR.glob("*.json")):
            print(f"  - {f.stem}")
    else:
        print("  (none)")

    # Pipeline status
    processor = AudioProcessor()
    status = processor.status
    print(f"""
Pipeline Status:
  State:           {status['state']}
  Cocoro Engine:   {'Available' if status['cocoro_available'] else 'Stub mode'}
  Fish Engine:     {'Available' if status['fish_available'] else 'Stub mode'}
  Active Jobs:     {status['active_jobs']}
""")


async def run_demo():
    """Run a demo chamber session."""
    from gabriel_mcp.orchestrator.chamber import ChamberOrchestrator
    from gabriel_mcp.pipeline.processor import AudioProcessor

    print("GABRIEL MCP v2 — Demo Session")
    print("=" * 40)

    # Initialize
    chamber = ChamberOrchestrator()
    processor = AudioProcessor()

    # Start session
    print("\n[1] Starting chamber session...")
    session = chamber.start_session(
        characters=["morrison", "poet"],
        metadata={"demo": True},
    )
    print(f"    Session ID: {session['session_id']}")
    print(f"    Characters: {session['characters_loaded']}")

    # Activate
    print("\n[2] Activating chamber...")
    chamber.activate_chamber()
    print("    Chamber active")

    # Queue work
    print("\n[3] Queuing audio jobs...")
    j1 = chamber.queue_audio("morrison", "process_cocoro", {"text": "Break on through to the other side"})
    j2 = chamber.queue_audio("poet", "process_cocoro", {"text": "The space between words"})
    print(f"    Queued: {j1['job_id']}")
    print(f"    Queued: {j2['job_id']}")

    # Process
    print("\n[4] Processing scene...")
    scene = await processor.process_scene([
        {"character": "morrison", "text": "This is the end, beautiful friend"},
        {"character": "poet", "text": "Of our elaborate plans, the end"},
    ])
    print(f"    Processed {len(scene['lines'])} lines")

    # Status
    print("\n[5] Final status...")
    status = chamber.status()
    print(f"    Session: {status['session']['session_id']}")
    print(f"    Audio queue: {status['audio']['queue_depth']} jobs")

    # Close
    print("\n[6] Closing session...")
    chamber.close_session()
    print("    Session closed")

    print("\n" + "=" * 40)
    print("Demo complete.")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        run_server()
    elif sys.argv[1] == "test":
        run_tests()
    elif sys.argv[1] == "status":
        show_status()
    elif sys.argv[1] == "demo":
        asyncio.run(run_demo())
    else:
        print(f"Unknown command: {sys.argv[1]}")
        print("Usage: python -m gabriel_mcp [test|status|demo]")
        sys.exit(1)


if __name__ == "__main__":
    main()
