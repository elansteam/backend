import {describe, test, expect, beforeEach} from "@jest/globals";
import { cleanup } from "./helpers/scripts";
import api from "./helpers/api";
import { ErrorCodes, SERVICE_TOKEN } from "./helpers/constants";
import RS from "./helpers/responses";
import { makeResponse } from "./helpers/helpers";
import { User } from "./helpers/objects";

describe("Organizations", () => {
  let first_user: User;
  let second_user: User;
  beforeEach(async () => {
    cleanup();

    first_user = await User.signup("first@gmail.com");
    second_user = await User.signup("second@gmail.com");
  });

  test("Create and get organization", () => {
    const org_name = "test_org";
    const org: RS.test.orgs.create = api.test.orgs.create({name: org_name}, first_user.getAccessToken())
      .expectJsonLike({ok: true})
      .returns(makeResponse);

    const orgs: RS.orgs.get = api.orgs.get({id: org.id}, first_user.getAccessToken())
      .expectJsonLike({ok: true})
      .returns(makeResponse);
    expect(orgs).toContainEqual({id: org.id, name: org_name});
  });
});
