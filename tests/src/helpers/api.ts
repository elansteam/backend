import pactum from "pactum";
import Spec from "pactum/src/models/Spec";


pactum.request.setBaseUrl("http://api_test:4242");


const api = {
  auth: {
    signin: () => pactum.spec().post("/api/auth/signin"),
    signup: () => pactum.spec().post("/api/auth/signup"),
    current: () => pactum.spec().get("/api/auth/current"),
    refresh: () => pactum.spec().get("/api/auth/refresh")
  },
  test: {
    cleanup: () => pactum.spec().post("/api/test/cleanup")
  }
}

export default api;
