import { describe, test, expect, beforeEach } from "@jest/globals";
import { cleanup } from "./helpers/scripts";
import api from "./helpers/api";
import { ErrorCodes } from "./helpers/constants";
import RS from "./helpers/responses";
import { makeResponse } from "./helpers/helpers";
import { User } from "./helpers/objects";


describe("Auth", () => {
  beforeEach(async () => {
    await cleanup();
  });

  test("Signup (test only method)", async () => {
    await api.test.signup({ firstName: "first", email: "first@gmail.com", password: "first" })
      .expectJsonLike({ ok: true })
    await api.test.signup({ firstName: "second", email: "second@gmail.com", password: "second" })
      .expectJsonLike({ ok: true })

    await api.test.signup({ firstName: "second", email: "second@gmail.com", password: "password" })
      .expectJsonLike({ ok: false, error: { code: ErrorCodes.EMAIL_ALREADY_TAKEN } });
  });

  test("Signin", async () => {
    const first_user = await User.signup("first@gmail.com");
    const second_user = await User.signup("second@gmail.com");

    await api.auth.signin({ email: first_user.email, password: first_user.password })
      .expectJsonLike({ ok: true });
    await api.auth.signin({ email: second_user.email, password: second_user.password })
      .expectJsonLike({ ok: true });

    // Try to pass incorrect password
    await api.auth.signin({ email: first_user.email, password: second_user.password + "incorrect" })
      .expectJsonLike({ ok: false, error: { code: ErrorCodes.ACCESS_DENIED } });
  });

  test("Get current user", async () => {
    const user = await User.signup("user@gmail.com");

    const userResponse: RS.users.current = await api.users.current(user.getAccessToken()).
      expectJsonLike({ ok: true })
      .returns(makeResponse);

    expect(userResponse.email).toBe(user.email);
    expect(userResponse.firstName).toBe(user.firstName);
  });

  test("Refresh token", async () => {
    const user = await User.signup("user@gmail.com");

    const newTokens: RS.auth.refresh = await api.auth.refresh(user.getRefreshToken())
      .expectJsonLike({ ok: true })
      .returns(makeResponse);

    // Check that both tokens are valid
    await api.users.current(user.getAccessToken()).expectJsonLike({ ok: true });
    await api.users.current(newTokens.accessToken).expectJsonLike({ ok: true });
  });
});
