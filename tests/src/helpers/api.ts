import pactum from "pactum";
import RQ from "./requests";
import { makeRequest } from "./helpers";


pactum.request.setBaseUrl("http://api_test:4242");


const api = {
  auth: {
    signin: (request: RQ.auth.signin) => pactum.spec().post("/api/auth/signin")
        .withBody(makeRequest(request)),
    refresh: (bearerToken: string) => pactum.spec().get("/api/auth/refresh")
        .withBearerToken(bearerToken)
  },
  test: {
    cleanup: () => pactum.spec().post("/api/test/cleanup"),
    signup: (request: RQ.test.signup) => pactum.spec().post("/api/test/signup")
        .withBody(makeRequest(request))
  },
  users: {
    current: (bearerToken: string) => pactum.spec().get("/api/users/current")
      .withBearerToken(bearerToken)
  }
}

export default api;
