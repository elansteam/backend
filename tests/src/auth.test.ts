import {describe, test, expect} from "@jest/globals";
import { cleanup } from "./helpers/scripts";
import api from "./helpers/api";
import { ErrorCodes, SERVICE_TOKEN } from "./helpers/constants";
import RS from "./helpers/responses";
import { makeResponse } from "./helpers/helpers";


describe("Auth", () => {
  cleanup();

  test("Signup (ELAN team only)", async () => {
    await api.auth.signup().withBody({first_name: "first", email: "first@gmail.com", password: "first"})
      .withHeaders("Authorization", SERVICE_TOKEN)
      .expectJsonLike({ok: true})
    await api.auth.signup().withBody({first_name: "second", email: "second@gmail.com", password: "second"})
      .withHeaders("Authorization", SERVICE_TOKEN)
      .expectJsonLike({ok: true})

    await api.auth.signup().withBody({first_name: "second", email: "second@gmail.com", password: "password"})
      .withHeaders("Authorization", SERVICE_TOKEN)
      .expectJsonLike({ok: false, error: {code: ErrorCodes.EMAIL_ALREADY_TAKEN}});

    await api.auth.signup().withBody({first_name: "foo", email: "foo@gmail.com", password: "password"})
      .expectJsonLike({ok: false, error: {code: ErrorCodes.UNPROCESSABLE_ENTITY}});
    await api.auth.signup().withBody({first_name: "foo", email: "foo@gmail.com", password: "password"})
      .withHeaders("Authorization", SERVICE_TOKEN + "make_token_incorrect")
      .expectJsonLike({ok: false, error: {code: ErrorCodes.ACCESS_DENIED}});
  });

  test("Signin", async () => {
    await api.auth.signin()
      .withBody({email: "first@gmail.com", password: "first"})
      .expectJsonLike({ok: true});
    await api.auth.signin()
      .withBody({email: "second@gmail.com", password: "second"})
      .expectJsonLike({ok: true});
    await api.auth.signin()
      .withBody({email: "first@gmail.com", password: "incorrect_password"})
      .expectJsonLike({ok: false, error: {code: ErrorCodes.ACCESS_DENIED}});
  });

  test("Get current user", async () => {
    const tokens: RS.AuthSignin = await api.auth.signin()
      .withBody({email: "first@gmail.com", password: "first"})
      .expectJsonLike({ok: true})
      .returns(makeResponse);

    const first_user: RS.UserCurrent = await api.users.current()
      .withBearerToken(tokens.accessToken)
      .expectJsonLike({ok: true})
      .returns(makeResponse);
    expect(first_user.email).toBe("first@gmail.com");

    await api.users.current()
      .withBearerToken("invalid_token")
      .expectJsonLike({ok: false, error: {code: ErrorCodes.TOKEN_VALIDATION_FAILED}});
  });

  test("Refresh token", async () => {
    const old_tokens: RS.AuthSignin = await api.auth.signin()
      .withBody({email: "first@gmail.com", password: "first"})
      .expectJsonLike({ok: true})
      .returns(makeResponse);

    await api.users.current().withBearerToken(old_tokens.accessToken).expectJsonLike({ok: true});
    const new_tokens: RS.AuthRefresh = await api.auth.refresh()
      .withBearerToken(old_tokens.refreshToken)
      .expectJsonLike({ok: true})
      .returns(makeResponse);

    await api.users.current().withBearerToken(old_tokens.accessToken).expectJsonLike({ok: true});
    await api.users.current().withBearerToken(new_tokens.accessToken).expectJsonLike({ok: true});
  });
});
