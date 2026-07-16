from pydantic import BaseModel, field_validator


class PublicKeyUpload(BaseModel):
    public_key: str

    @field_validator("public_key")
    @classmethod
    def validate_pgp_format(cls, v: str) -> str:
        PGP_PUBLIC_KEY_BLOCK_HEAD = "-----BEGIN PGP PUBLIC KEY BLOCK-----"
        if not v.strip().startswith(PGP_PUBLIC_KEY_BLOCK_HEAD):
            raise ValueError("Chave pública deve estar no formato PGP ASCII-armored.")
        return v
