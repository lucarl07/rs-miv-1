import * as openpgp from 'openpgp';
import uploadPublicKey from '@/api/uploadPublicKey';

const PRIVATE_KEY_STORAGE_KEY = 'pgp_private_key';

export function usePgpIdentity() {
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

  function removeKeyPair() {
    sessionStorage.removeItem(PRIVATE_KEY_STORAGE_KEY)
  }

  async function ensureKeyPair(token: string | null) {
    const existing = getStoredPrivateKey();
    if (existing) return;

    await generateAndRegisterKeyPair(token);
  }

  return {
    generateAndRegisterKeyPair,
    getStoredPrivateKey,
    ensureKeyPair,
    removeKeyPair,
  };
}
