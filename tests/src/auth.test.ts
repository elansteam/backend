import {describe, test, expect} from "@jest/globals";
import { cleanup } from "./helpers/scripts";
import api from "./helpers/api";
import { ErrorCodes, SERVICE_TOKEN } from "./helpers/constants";
import RS from "./helpers/responses";
import { makeResponse } from "./helpers/helpers";


describe("Auth", () => {
  cleanup();

  test("Signup (test only method)", async () => {
    await api.test.signup({
        firstName: "first",
        email: "first@gmail.com",
        password: "first"
      })
      .expectJsonLike({ok: true})
    await api.test.signup({firstName: "second", email: "second@gmail.com", password: "second"})
      .expectJsonLike({ok: true})

    await api.test.signup({firstName: "second", email: "second@gmail.com", password: "password"})
      .expectJsonLike({ok: false, error: {code: ErrorCodes.EMAIL_ALREADY_TAKEN}});
  });

  test("Signin", async () => {
    await api.auth.signin({email: "first@gmail.com", password: "first"})
      .expectJsonLike({ok: true});
    await api.auth.signin({email: "second@gmail.com", password: "second"})
      .expectJsonLike({ok: true});
    await api.auth.signin({email: "first@gmail.com", password: "incorrect_password"})
      .expectJsonLike({ok: false, error: {code: ErrorCodes.ACCESS_DENIED}});
  });

  test("Get current user", async () => {
    const tokens: RS.auth.signin = await api.auth.signin({
      email: "first@gmail.com", password: "first"
    }).expectJsonLike({ok: true})
      .returns(makeResponse);

    const firstUser: RS.users.current = await api.users.current(tokens.accessToken)
      .expectJsonLike({ok: true})
      .returns(makeResponse);
    expect(firstUser.email).toBe("first@gmail.com");
    expect(firstUser.firstName).toBe("first");

    await api.users.current("invalid_token")
      .expectJsonLike({ok: false, error: {code: ErrorCodes.TOKEN_VALIDATION_FAILED}});
  });

  test("Refresh token", async () => {
    const oldTokens: RS.auth.signin = await api.auth.signin({
      email: "first@gmail.com", password: "first"
    }).expectJsonLike({ok: true})
      .returns(makeResponse);

    await api.users.current(oldTokens.accessToken).expectJsonLike({ok: true});
    const newTokens: RS.auth.refresh = await api.auth.refresh(oldTokens.refreshToken)
      .expectJsonLike({ok: true})
      .returns(makeResponse);

    await api.users.current(oldTokens.accessToken).expectJsonLike({ok: true});
    await api.users.current(newTokens.accessToken).expectJsonLike({ok: true});
  });
});
