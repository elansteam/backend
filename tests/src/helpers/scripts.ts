import api from "./api";


export const cleanup = async () => {
  await api.test.cleanup().expectJsonLike({ok: true});
}
