import {describe, test, expect, beforeEach} from "@jest/globals";
import { cleanup } from "./helpers/scripts";
import api from "./helpers/api";
import { ErrorCodes } from "./helpers/constants";
import RS from "./helpers/responses";
import { makeResponse } from "./helpers/helpers";
import { User } from "./helpers/objects";
import { Organization } from "./helpers/types";


describe("Groups", () => {
    let firstUser: User;
    let secondUser: User;

    let firstOrganization: Organization;
    let secondOrganization: Organization;
    beforeEach(async () => {
        await cleanup();
        firstUser = await User.signup("first@gmail.com");
        secondUser = await User.signup("second@gmail.com");

        firstOrganization = await api.test.organizations.create({name: "first_org"}, firstUser.getAccessToken())
          .returns(makeResponse);
        secondOrganization = await api.test.organizations.create({name: "second_org"}, secondUser.getAccessToken())
          .returns(makeResponse);
    });

    test("Simple create and get", async () => {
        // create group for first organization with first user
        const group: RS.test.groups.create = await api.test.groups.create({name: "test_group", organizationId: firstOrganization.id}, firstUser.getAccessToken())
            .expectJsonLike({ok: true})
            .returns(makeResponse);

        // get created group by id
        const receivedGroup: RS.groups.get = await api.groups.get({id: group.id}, firstUser.getAccessToken())
            .expectJsonLike({ok: true})
            .returns(makeResponse);
        expect(receivedGroup).toStrictEqual(group);
    });

    test("Create group from non org member", async () => {
        // create group to second org from first user
        await api.test.groups.create({name: "test_group", organizationId: secondOrganization.id}, firstUser.getAccessToken())
            .expectJsonLike({ok: false, error: {code: ErrorCodes.ACCESS_DENIED}});
    });

    test("Invite user to the group", async () => {
        // create group
        let group: RS.test.groups.create = await api.test.groups.create({name: "test_group", organizationId: firstOrganization.id}, firstUser.getAccessToken())
            .expectJsonLike({ok: true})
            .returns(makeResponse);
        // invite user
        await api.test.groups.invite({userId: secondUser.id, groupId: group.id}, firstUser.getAccessToken())
            .expectJsonLike({ok: true});
        // update group
        group = await api.groups.get({id: group.id}, firstUser.getAccessToken())
            .expectJsonLike({ok: true})
            .returns(makeResponse);
        expect(group.members).toContainEqual({customPermissions: 0, id: firstUser.id, roles: []});
        expect(group.members).toContainEqual({customPermissions: 0, id: secondUser.id, roles: []});
    });
});
