import {describe, test, expect, beforeEach} from "@jest/globals";
import { cleanup } from "./helpers/scripts";
import api from "./helpers/api";
import { ErrorCodes, SERVICE_TOKEN } from "./helpers/constants";
import RS from "./helpers/responses";
import { makeResponse } from "./helpers/helpers";
import { User } from "./helpers/objects";


describe("Organizations", () => {
  let firstUser: User;
  let secondUser: User;
  beforeEach(async () => {
    await cleanup();
    firstUser = await User.signup("first@gmail.com");
    secondUser = await User.signup("second@gmail.com");
  });

  test("Create and get organization", async () => {
    const organizationName = "test_org";
    const organization: RS.test.organizations.create = await api.test.organizations.create({name: organizationName}, firstUser.getAccessToken())
      .expectJsonLike({ok: true})
      .returns(makeResponse);

    const receivedOrganization: RS.organizations.get = await api.organizations.get({id: organization.id}, firstUser.getAccessToken())
      .expectJsonLike({ok: true})
      .returns(makeResponse);
    expect(receivedOrganization).toMatchObject({id: organization.id, name: organizationName, members: [firstUser.id]});
  });

  test("Invite user to organization", async () => {
    const organization: RS.test.organizations.create = await api.test.organizations.create({name: "test_org"}, firstUser.getAccessToken())
      .expectJsonLike({ok: true})
      .returns(makeResponse);

    await api.test.organizations.invite({organizationId: organization.id, userId: secondUser.id}, firstUser.getAccessToken())
      .expectJsonLike({ok: true});

    const receivedOrganization: RS.organizations.get = await api.organizations.get({id: organization.id}, firstUser.getAccessToken())
      .expectJsonLike({ok: true})
      .returns(makeResponse);
    expect(receivedOrganization).toMatchObject({id: organization.id, members: [firstUser.id, secondUser.id]});
  });

  test("Invite user to organization from unauthorized user", async () => {
      const organization: RS.test.organizations.create = await api.test.organizations.create({name: "test_org"}, firstUser.getAccessToken())
        .expectJsonLike({ok: true})
        .returns(makeResponse);

      // Try to invite a user from an unauthorized user
      await api.test.organizations.invite({organizationId: organization.id, userId: secondUser.id}, secondUser.getAccessToken())
        .expectJsonLike({ok: false, error: {code: ErrorCodes.ACCESS_DENIED}});

      // Ensure that the organization members remain unchanged
      const receivedOrganization: RS.organizations.get = await api.organizations.get({id: organization.id}, firstUser.getAccessToken())
        .expectJsonLike({ok: true})
        .returns(makeResponse);
      expect(receivedOrganization).toMatchObject({id: organization.id, members: [firstUser.id]});
    });

  test("Invite user already in organization", async () => {
    const organization: RS.test.organizations.create = await api.test.organizations.create({name: "test_org"}, firstUser.getAccessToken())
      .expectJsonLike({ok: true})
      .returns(makeResponse);

    // Invite the second user to the organization
    await api.test.organizations.invite({organizationId: organization.id, userId: secondUser.id}, firstUser.getAccessToken())
      .expectJsonLike({ok: true});

    // Try to invite the second user again
    await api.test.organizations.invite({organizationId: organization.id, userId: secondUser.id}, firstUser.getAccessToken())
      .expectJsonLike({ok: true});

    // Ensure that the organization members remain unchanged
    const receivedOrganization: RS.organizations.get = await api.organizations.get({id: organization.id}, firstUser.getAccessToken())
      .expectJsonLike({ok: true})
      .returns(makeResponse);
    expect(receivedOrganization).toMatchObject({id: organization.id, members: [firstUser.id, secondUser.id]});
    });
});
