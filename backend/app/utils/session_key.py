import os
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes


def derive_session_key() -> bytes:
    seed = os.environ["SESSION_KEY_SEED"].encode("utf-8")

    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b"Escutem Wintersun!", # É uma boa ideia, ao invés de olhar source code alheio...
                                    # (Valor de salt arbitrário e não-secreto; seed já é forte o bastante)
        info=b"rs-miv-1:session-key:v1",
    )
    return hkdf.derive(seed)

