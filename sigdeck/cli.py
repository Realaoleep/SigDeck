"""sd - the SigDeck command line interface."""

import argparse
import sys
from pathlib import Path

from .keys import armor_secret, generate_seed, load_secret, save_armored
from . import ed25519


def main(argv=None):
    ap = argparse.ArgumentParser(prog="sd")
    sub = ap.add_subparsers(dest="cmd", required=True)

    pk = sub.add_parser("keygen", help="create a new key pair")
    pk.add_argument("--out", default="signing.key")

    ps = sub.add_parser("sign", help="sign a file")
    ps.add_argument("file")
    ps.add_argument("--key", default="signing.key")

    args = ap.parse_args(argv)

    if args.cmd == "keygen":
        seed = generate_seed()
        save_armored(args.out, armor_secret(seed))
        print(f"wrote {args.out}")
        return 0

    if args.cmd == "sign":
        seed = load_secret(args.key)
        data = Path(args.file).read_bytes()
        sig = ed25519.sign(data, seed)
        Path(args.file + ".sig").write_bytes(sig)
        print(f"wrote {args.file}.sig")
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
