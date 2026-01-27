def parse_text_bytes(raw: bytes) -> str:
    # This is decoding as UTF-8 and falling back safely.
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("latin-1", errors="ignore")
