import api from "./api";
import { JWTPair } from "./types";
import RS from "./responses";

export class User {
    private constructor(
        public email: string,
        public firstName: string,
        public password: string,
        private jwt_pair: JWTPair
    ) {}

    static async signup(
        email: string,
        firstName: string = "test_user"
    ): Promise<User> {
        const password = "password";
        const jwt_pair: RS.test.signup = await api.test.signup({
            email,
            firstName: firstName,
            password
        }).expectJsonLike({
            ok: true
        });

        return new User(email, firstName, password, jwt_pair);
    }

    public getAccessToken(): string {
        return this.jwt_pair.accessToken;
    }
}