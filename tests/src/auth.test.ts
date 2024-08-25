import {describe, test} from "@jest/globals";
import { cleanup } from "./helpers/scripts";
import api from "./helpers/api";
import { ErrorCodes } from "./helpers/constants";


describe("Auth", () => {
  cleanup();

  test("Signup", async () => {
    await api.auth.signup().withBody({
      first_name: "first", email: "first@gmail.com", password: "first"})
    .expectJsonLike({ok: true});
    await api.auth.signup().withBody({first_name: "second", email: "second@gmail.com", password: "second"})
      .expectJsonLike({ok: true});
    await api.auth.signup()
      .withBody({first_name: "second", email: "second@gmail.com", password: "password"})
      .expectJsonLike({ok: false, error: {code: ErrorCodes.NAME_ALREADY_TAKEN}});
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

  // TODO: test("Get current user", async () => {});
});