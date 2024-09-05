import api from "./api";
import { JWTPair } from "./types";
import RS from "./responses";
import { makeResponse } from "./helpers";

export class User {
    private constructor(
        public id: number,
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
        }).returns(makeResponse);

        const currentUser: RS.users.current = await api.users.current(jwt_pair.accessToken)
            .expectJsonLike({ok: true})
            .returns(makeResponse);

        return new User(currentUser.id, currentUser.email, currentUser.firstName, password, jwt_pair);
    }

    public getAccessToken(): string {
        return this.jwt_pair.accessToken;
    }

    public getRefreshToken(): string {
        return this.jwt_pair.refreshToken;
    }
}