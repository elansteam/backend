import pactum from "pactum";
import {describe, test, expect} from "@jest/globals";

pactum.request.setBaseUrl("http://api_test:4242");

describe("Test methods", () => {
    test("Ping", async () => {
        await pactum.spec()
            .get("/api/service/ping")
            .expectStatus(200)
            .expectBody("pong")
        });
});
