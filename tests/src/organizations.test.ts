import {describe, test, expect, beforeEach} from "@jest/globals";
import { cleanup } from "./helpers/scripts";
import api from "./helpers/api";
import { ErrorCodes } from "./helpers/constants";
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
    const organization: RS.test.organizations.create = await api.test.organizations.create({name: "test_org"}, firstUser.getAccessToken())
      .expectJsonLike({ok: true})
      .returns(makeResponse);

    // Ensure that organization have only creator as a member
    const members: RS.organizations.get_members = await api.organizations.get_members({id: organization.id}, firstUser.getAccessToken())
      .expectJsonLike({"ok": true})
      .returns(makeResponse)
    expect(members.members).toContain(firstUser.id);
  });

  test("Invite user to organization", async () => {
    const organization: RS.test.organizations.create = await api.test.organizations.create({name: "test_org"}, firstUser.getAccessToken())
      .expectJsonLike({ok: true})
      .returns(makeResponse);

    await api.test.organizations.invite({organizationId: organization.id, userId: secondUser.id}, firstUser.getAccessToken())
      .expectJsonLike({ok: true});

    // Ensure that the organization members have been updated
    const members: RS.organizations.get_members = await api.organizations.get_members({id: organization.id}, firstUser.getAccessToken())
      .expectJsonLike({ok: true})
      .returns(makeResponse);
    expect(members.members).toContain(firstUser.id);
    expect(members.members).toContain(secondUser.id);
  });

  test("Invite user to organization from unauthorized user", async () => {
    const organization: RS.test.organizations.create = await api.test.organizations.create({name: "test_org"}, firstUser.getAccessToken())
      .expectJsonLike({ok: true})
      .returns(makeResponse);

    // Try to invite a user from an unauthorized user
    await api.test.organizations.invite({organizationId: organization.id, userId: secondUser.id}, secondUser.getAccessToken())
      .expectJsonLike({ok: false, error: {code: ErrorCodes.ACCESS_DENIED}});

    // Ensure that the organization members remain unchanged
    const members: RS.organizations.get_members = await api.organizations.get_members({id: organization.id}, firstUser.getAccessToken())
      .expectJsonLike({ok: true})
      .returns(makeResponse);
    expect(members).toMatchObject({members: [firstUser.id]})
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
      .expectJsonLike({ok: false, error: {code: ErrorCodes.USER_ALREADY_MEMBER}});

    // Ensure that the organization members remain unchanged
    const members: RS.organizations.get_members = await api.organizations.get_members({id: organization.id}, firstUser.getAccessToken())
      .expectJsonLike({ok: true})
      .returns(makeResponse);
    expect(members).toMatchObject({members: [firstUser.id, secondUser.id]});
  });

  test("Get user organizations", async () => {
    // Create two different organizations and ensure that after each creation method returns new organization
    const firstOrganization: RS.test.organizations.create = await api.test.organizations.create({name: "first_org"}, firstUser.getAccessToken())
      .expectJsonLike({ok: true})
      .returns(makeResponse);
    let firstUserOrganizations: RS.users.get_organizations = await api.users.get_organizations({id: firstUser.id}, firstUser.getAccessToken())
      .expectJsonLike({ok: true})
      .returns(makeResponse);
    expect(firstUserOrganizations.organizations).toMatchObject(
      [{name: "first_org"}]
    );

    // Get first user organizations from the second user
    await api.test.organizations.create({name: "second_org"}, firstUser.getAccessToken()).expectJsonLike({ok: true});
    firstUserOrganizations = await api.users.get_organizations({id: firstUser.id}, secondUser.getAccessToken())
      .expectJsonLike({ok: true})
      .returns(makeResponse);
    expect(firstUserOrganizations.organizations).toMatchObject(
      [{name: "first_org"}, {name: "second_org"}]
    );

    // Test that second user has no organizations
    let secondUserOrganizations: RS.users.get_organizations = await api.users.get_organizations({id: secondUser.id}, secondUser.getAccessToken())
      .expectJsonLike({ok: true})
      .returns(makeResponse);
    expect(secondUserOrganizations.organizations.length).toBe(0);

    // Create organization for the second user and ensure that the second user are it
    await api.test.organizations.create({name: "third_org"}, secondUser.getAccessToken());
    secondUserOrganizations = await api.users.get_organizations({id: secondUser.id}, secondUser.getAccessToken())
      .expectJsonLike({ok: true})
      .returns(makeResponse);
    expect(secondUserOrganizations.organizations).toMatchObject(
      [{name: "third_org"}]
    );

    // invite second user to an organization and ensure that he is in the organization
    await api.test.organizations.invite({organizationId: firstOrganization.id, userId: secondUser.id}, firstUser.getAccessToken())
      .expectJsonLike({ok: true});
    secondUserOrganizations = await api.users.get_organizations({id: secondUser.id}, secondUser.getAccessToken())
      .expectJsonLike({ok: true})
      .returns(makeResponse);
    expect(secondUserOrganizations.organizations).toContainEqual(expect.objectContaining({ name: "third_org" }));
    expect(secondUserOrganizations.organizations).toContainEqual(expect.objectContaining({ name: "first_org" }));
  });
});
