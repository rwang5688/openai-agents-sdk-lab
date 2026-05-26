def configure_ssl_trust_store() -> None:
    try:
        import truststore
    except ImportError:
        return

    truststore.inject_into_ssl()
