"""CLI-level smoke tests (argparse wiring, real files)."""

from sigdeck.cli import main


def test_keygen_writes_pair(tmp_path):
    key = tmp_path / "k.key"
    rc = main(["keygen", "--out", str(key)])
    assert rc == 0
    assert key.exists()
    assert key.with_suffix(".pub").exists()


def test_sign_then_verify(tmp_path):
    key = tmp_path / "k.key"
    pub = tmp_path / "k.pub"
    assert main(["keygen", "--out", str(key)]) == 0
    assert main(["pub", "--key", str(key), "--output", str(pub)]) == 0
    target = tmp_path / "a.bin"
    target.write_bytes(b"payload" * 50)
    sig = tmp_path / "a.bin.sig"
    assert main(["sign", str(target), "--key", str(key), "--output", str(sig)]) == 0
    assert main(["verify", str(target), "--sig", str(sig), "--pub", str(pub)]) == 0


def test_verify_fails_on_tamper(tmp_path):
    key = tmp_path / "k.key"
    pub = tmp_path / "k.pub"
    main(["keygen", "--out", str(key)])
    main(["pub", "--key", str(key), "--output", str(pub)])
    target = tmp_path / "a.bin"
    target.write_bytes(b"payload" * 50)
    sig = tmp_path / "a.bin.sig"
    main(["sign", str(target), "--key", str(key), "--output", str(sig)])
    target.write_bytes(b"tampered" * 50)
    assert main(["verify", str(target), "--sig", str(sig), "--pub", str(pub)]) == 1
