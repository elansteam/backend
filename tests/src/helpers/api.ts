import pactum from "pactum";
import RQ from "./requests";
import { makeRequest } from "./helpers";


pactum.request.setBaseUrl(process.env.API_ORIGIN || "http://api_test:4242");


const api = {
  auth: {
    refresh: (bearerToken: string) => pactum.spec().get("/api/auth/refresh")
      .withBearerToken(bearerToken),
    signin: (request: RQ.auth.signin) => pactum.spec().post("/api/auth/signin")
      .withBody(makeRequest(request))
  },
  organizations: {
    get: (request: RQ.organizations.get, bearerToken: string) => pactum.spec().get("/api/organizations/get")
      .withBearerToken(bearerToken)
      .withQueryParams(makeRequest(request)),
    get_groups: (request: RQ.organizations.get_groups, bearerToken: string) => pactum.spec().get("/api/organizations/get_groups")
      .withBearerToken(bearerToken)
      .withQueryParams(makeRequest(request))
  },
  test: {
    cleanup: () => pactum.spec().post("/api/test/cleanup"),
    signup: (request: RQ.test.signup) => pactum.spec().post("/api/test/signup")
      .withBody(makeRequest(request)),
    organizations: {
      create: (request: RQ.test.organizations.create, bearerToken: string) => pactum.spec().post("/api/test/organizations/create")
        .withBearerToken(bearerToken)
        .withBody(makeRequest(request)),
      invite: (request: RQ.test.organizations.invite, bearerToken: string) => pactum.spec().post("/api/test/organizations/invite")
        .withBearerToken(bearerToken)
        .withBody(makeRequest(request)),
    },
    groups: {
      create: (request: RQ.test.groups.create, bearerToken: string) => pactum.spec().post("/api/test/groups/create")
        .withBearerToken(bearerToken)
        .withBody(makeRequest(request)),
      invite: (request: RQ.test.groups.invite, bearerToken: string) => pactum.spec().post("/api/test/groups/invite")
        .withBearerToken(bearerToken)
        .withBody(makeRequest(request)),
    },
  },
  users: {
    current: (bearerToken: string) => pactum.spec().get("/api/users/current")
      .withBearerToken(bearerToken),
    get_organizations: (request: RQ.users.get_organizations, bearerToken: string) => pactum.spec().get("/api/users/get_organizations")
      .withBearerToken(bearerToken)
      .withQueryParams(makeRequest(request))
  },
  groups: {
    get: (request: RQ.groups.get, bearerToken: string) => pactum.spec().get("/api/groups/get")
      .withBearerToken(bearerToken)
      .withQueryParams(makeRequest(request)),
  }
};

export default api;
