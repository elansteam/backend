import pactum from "pactum";


pactum.request.setBaseUrl("http://api_test:4242");

const api = {
    auth: {
        signin: () => pactum.spec().post("/api/auth/signin"),
        signup: () => pactum.spec().post("/api/auth/signup")
    },
    test: {
        cleanup: () => pactum.spec().post("/api/test/cleanup")
    }
}

export default api;
