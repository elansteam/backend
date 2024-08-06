import pactum from "pactum";
import {describe, test, expect} from "@jest/globals";
import { GlobalCounter } from "./helpers/scripts";
import ErrorCodes from "./helpers/error_codes";

pactum.request.setBaseUrl("http://api_test:4242");


describe("Basic auth", () => {
  const first_email = GlobalCounter.getNextEmail();
  const second_email = GlobalCounter.getNextEmail();
  const third_domain = GlobalCounter.getNextString();
  const third_email = GlobalCounter.getNextEmail();
  test("Registration", async () => {
    await pactum.spec()
      .post("/api/auth/signup")
      .withBody({
        email: first_email,
        password: "1234"
      })
      .expectJsonLike({ok: true});
    await pactum.spec()
      .post("/api/auth/signup")
      .withBody({
        email: second_email,
        password: "1234"
      })
      .expectJsonLike({ok: true});

    await pactum.spec()
      .post("/api/auth/signup")
      .withBody({
        email: second_email,
        password: "1234"
      })
      .expectJsonLike({
        ok: false,
        error: {
          code: ErrorCodes.NAME_ALREADY_TAKEN
        }
      });

    await pactum.spec()
      .post("/api/auth/signup")
      .withBody({
        email: third_email,
        domain: third_domain,
        password: "1234"
      })
      .expectStatus(200)

    await pactum.spec()
      .post("/api/auth/signup")
      .withBody({
        email: GlobalCounter.getNextEmail(),
        domain: third_domain,
        password: "1234"
      })
      .expectJsonLike({
        ok: false,
        error: {
          code: ErrorCodes.NAME_ALREADY_TAKEN
        }
      });
  });

  test("Auth", async () => {
    await pactum.spec()
      .post("/api/auth/signin")
      .withBody({
        email: first_email,
        password: "1234"
      })
      .expectJsonLike({ok: true});

    await pactum.spec()
      .post("/api/auth/signin")
      .withBody({
        email: first_email,
        password: "incorrect_password"
      })
      .expectJsonLike({
        ok: false,
        error: {
          code: ErrorCodes.ACCESS_DENIED
        }
      });

    const access_token = await pactum.spec()
      .post("/api/auth/signin")
      .withBody({
        domain: third_domain,
        password: "1234"
      })
      .expectJsonLike({ok: true})
      .returns((ctx) => {
        return ctx.res.body.access
      });

    await pactum.spec()
      .post("/api/auth/signin")
      .withBody({
        domain: third_domain,
        password: "incorrect_password"
      })
      .expectJsonLike({ok: false});
  });
})