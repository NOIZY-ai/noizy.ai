#!/usr/bin/env python3
"""
artifact_signer.py - Sign artifacts with checksums and optional GPG
Usage:
  python artifact_signer.py --dir artifacts
  python artifact_signer.py --dir artifacts --gpg-key ABCD1234
  python artifact_signer.py --dir artifacts --checksums-only
  python artifact_signer.py --verify --dir artifacts
"""
import os
import sys
import json
import hashlib
import subprocess
import argparse
from datetime import datetime, timezone

ARTIFACT_PATTERNS = ["*.json", "*.txt", "*.sh"]


def sha256_file(path: str) -> str:
    """Compute SHA256 of file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def sha512_file(path: str) -> str:
    """Compute SHA512 of file."""
    h = hashlib.sha512()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def gpg_sign(path: str, key_id: str = None) -> bool:
    """Create detached GPG signature."""
    cmd = ["gpg", "--batch", "--yes", "--detach-sign", "--armor"]
    if key_id:
        cmd.extend(["--local-user", key_id])
    cmd.extend(["--output", f"{path}.asc", path])
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except:
        return False


def gpg_verify(path: str) -> bool:
    """Verify GPG signature."""
    sig_path = f"{path}.asc"
    if not os.path.exists(sig_path):
        return False
    
    try:
        subprocess.run(["gpg", "--verify", sig_path, path], check=True, capture_output=True)
        return True
    except:
        return False


def verify_checksum(path: str) -> bool:
    """Verify SHA256 checksum."""
    checksum_path = f"{path}.sha256"
    if not os.path.exists(checksum_path):
        return False
    
    with open(checksum_path) as f:
        expected = f.read().strip().split()[0]
    
    actual = sha256_file(path)
    return actual == expected


def main():
    parser = argparse.ArgumentParser(description="Sign artifacts")
    parser.add_argument("--dir", default="artifacts", help="Directory with artifacts")
    parser.add_argument("--gpg-key", help="GPG key ID for signing")
    parser.add_argument("--checksums-only", action="store_true", help="Skip GPG signing")
    parser.add_argument("--verify", action="store_true", help="Verify existing signatures")
    args = parser.parse_args()

    if not os.path.isdir(args.dir):
        print(f"Directory not found: {args.dir}", file=sys.stderr)
        sys.exit(1)

    # Find artifact files
    files = []
    for f in os.listdir(args.dir):
        if f.endswith((".json", ".txt", ".sh")) and not f.endswith((".sha256", ".sha512", ".asc")):
            files.append(os.path.join(args.dir, f))

    if not files:
        print("No artifacts found")
        sys.exit(0)

    print("═" * 60)
    print(f"{'VERIFY' if args.verify else 'SIGN'} ARTIFACTS")
    print("═" * 60)

    if args.verify:
        # Verification mode
        all_ok = True
        for path in files:
            name = os.path.basename(path)
            checksum_ok = verify_checksum(path)
            gpg_ok = gpg_verify(path)
            
            status = []
            if checksum_ok:
                status.append("✅ SHA256")
            else:
                status.append("❌ SHA256")
                all_ok = False
            
            if os.path.exists(f"{path}.asc"):
                if gpg_ok:
                    status.append("✅ GPG")
                else:
                    status.append("❌ GPG")
                    all_ok = False
            
            print(f"  {name}: {' '.join(status)}")
        
        sys.exit(0 if all_ok else 1)

    # Signing mode
    manifest = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "signed_by": args.gpg_key or "(checksums only)",
        "files": []
    }

    for path in files:
        name = os.path.basename(path)
        size = os.path.getsize(path)
        
        # Checksums
        sha256 = sha256_file(path)
        sha512 = sha512_file(path)
        
        with open(f"{path}.sha256", "w") as f:
            f.write(f"{sha256}  {name}\n")
        
        with open(f"{path}.sha512", "w") as f:
            f.write(f"{sha512}  {name}\n")
        
        print(f"  ✅ {name}")
        print(f"     SHA256: {sha256[:16]}...")
        
        # GPG
        gpg_signed = False
        if not args.checksums_only and args.gpg_key:
            gpg_signed = gpg_sign(path, args.gpg_key)
            if gpg_signed:
                print(f"     GPG: signed")
            else:
                print(f"     GPG: failed")
        
        manifest["files"].append({
            "name": name,
            "size": size,
            "checksums": {"sha256": sha256, "sha512": sha512},
            "gpg_signed": gpg_signed
        })

    # Write manifest
    manifest_path = os.path.join(args.dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    
    # Sign manifest too
    if not args.checksums_only and args.gpg_key:
        gpg_sign(manifest_path, args.gpg_key)

    print(f"\n✅ Manifest: {manifest_path}")
    print("═" * 60)


if __name__ == "__main__":
    main()
