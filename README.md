# SigDeck

**Offline Ed25519 signing toolkit** - sign files, verify signatures, exchange
keys via QR. Fully air-gapped: a pure-Python RFC 8032 implementation, scrypt
passphrases, and ASCII armor.

## Layout

```
sigdeck/    the Python engine (pure stdlib)
app/        minimal Android demo: scan QR keys, sign, verify
docs/       guides
examples/   recipes
```

## Quick start

```
pip install -e .
sd keygen --out alice.key
sd sign release.tar.gz --key alice.key
sd verify release.tar.gz --sig release.tar.gz.sig --pub alice.pub
```
