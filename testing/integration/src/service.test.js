const {spec, request} = require("pactum");
const { like } = require('pactum-matchers');
const {describe, test, expect} = require("@jest/globals");

request.setBaseUrl("http://integration_test_backend:8080");

test("Ping", async () => {
    result = await spec()
            .get("/api/service/test/ok")
            .expectStatus(200)
            .expectBody({
                "ok": true,
                "response": {
                    "some_result": "BANANA"
                }
            }).retry()
});

test("validate int", async () => {
    await spec()
        .get("/api/service/test/validate_int/{int}")
        .withPathParams({
            int: "some_string"
        })
        .expectStatus(422)
        .expectJsonLike({
            ok: false,
            error: {
                code: 2,
            }
        }).expect((ctx) => {
            expect(typeof ctx.res.body?.error.message).toBe("string");
        })

    await spec()
        .get("/api/service/test/validate_int/{int}")
        .withPathParams({
            int: 1
        })
        .expectStatus(200)
        .expectBody({
            ok: true,
            response: {}
        })
});

test("internal server error", async () => {
    await spec()
        .get("/api/service/test/500")
        .expectStatus(500)
        .expectJsonLike({
            ok: false,
            error: {
                code: 1,
                message: "Internal Server Error"
            }
        })
});

test("signup", async () => {
    await spec()
        .post("/api/auth/signup")
        .withBody({
            password: "123",
            first_name: "John",
            last_name: "Doe",
            email: "1john.doe@banana.com"
        })
        .expect(200)

    // await spec()
    //     .post("/api/auth/signup")
    //     .withBody({
    //         password: "123",
    //         first_name: "John",
    //         last_name: "Doe",
    //         email: "1john.doe@banana.com"
    //     })
    //     .expect(400)
});