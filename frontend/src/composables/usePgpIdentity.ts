import * as openpgp from 'openpgp';
import uploadPublicKey from '@/api/uploadPublicKey';

const PRIVATE_KEY_STORAGE_KEY = 'pgp_private_key';

export default function usePgpIdentity() {
  async function generateAndRegisterKeyPair(token: string | null) {
    const { privateKey, publicKey } = await openpgp.generateKey({
      type: 'curve25519',
      userIDs: [{ name: 'RS-MIV-1 user' }],
      format: 'armored',
    });

    sessionStorage.setItem(PRIVATE_KEY_STORAGE_KEY, privateKey);
    await uploadPublicKey(token, publicKey);

    return { privateKey, publicKey };
  }

  function getStoredPrivateKey(): string | null {
    return sessionStorage.getItem(PRIVATE_KEY_STORAGE_KEY);
  }

  async function ensureKeyPair(token: string | null) {
    const existing = getStoredPrivateKey();
    if (existing) return;

    await generateAndRegisterKeyPair(token);
  }

  function removeKeyPair() {
    sessionStorage.removeItem(PRIVATE_KEY_STORAGE_KEY)
  }

  async function decryptSessionKey(
    armoredEnvelope: string
  ): Promise<Uint8Array> {

    const armoredPrivateKey = getStoredPrivateKey();
    if (!armoredPrivateKey) {
      throw new Error('Nenhuma chave privada PGP encontrada no sessionStorage');
    }

    const privateKey = await openpgp.readPrivateKey({ armoredKey: armoredPrivateKey })
    const message = await openpgp.readMessage({ armoredMessage: armoredEnvelope })

    const { data } = await openpgp.decrypt({
      message,
      decryptionKeys: privateKey,
      format: 'binary' // Evita a conversão para string que o padrão faria
    })

    return data as Uint8Array
  }

  return {
    generateAndRegisterKeyPair,
    getStoredPrivateKey,
    ensureKeyPair,
    removeKeyPair,
    decryptSessionKey
  };
}
