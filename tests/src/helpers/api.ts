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
  orgs: {
    get: (request: RQ.orgs.get, bearerToken: string) => pactum.spec().get("/api/orgs/get")
      .withBearerToken(bearerToken)
      .withQueryParams(makeRequest(request))
  },
  test: {
    cleanup: () => pactum.spec().post("/api/test/cleanup"),
    signup: (request: RQ.test.signup) => pactum.spec().post("/api/test/signup")
        .withBody(makeRequest(request)),
    orgs: {
      create: (request: RQ.test.orgs.create, bearerToken: string) => pactum.spec().post("/api/test/orgs/create")
        .withBearerToken(bearerToken)
        .withBody(makeRequest(request)),
      invite: (request: RQ.test.orgs.invite, bearerToken: string) => pactum.spec().post("/api/test/orgs/invite")
        .withBearerToken(bearerToken)
        .withBody(makeRequest(request))
    }
  },
  users: {
    current: (bearerToken: string) => pactum.spec().get("/api/users/current")
      .withBearerToken(bearerToken),
    get_orgs: (request: RQ.users.get_orgs, bearerToken: string) => pactum.spec().get("/api/users/get_orgs")
      .withBearerToken(bearerToken)
      .withQueryParams(makeRequest(request))
  }
}

export default api;
