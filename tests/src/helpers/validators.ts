import { expect } from "@jest/globals";
import { AuthSignin, AuthSignup } from "./responses";

export const auth_signin = (body: any): AuthSignin => {
    const to_validate: AuthSignin = {
        access_token: body.access_token,
        refresh_token: body.refresh_token
    }
    expect(typeof to_validate.access_token).toBe("string");
    expect(typeof to_validate.refresh_token).toBe("string");

    return to_validate;
}

export const auth_signup = (body: any): AuthSignup => {
    const to_validate: AuthSignin = {
        access_token: body.access_token,
        refresh_token: body.refresh_token
    }
    expect(typeof to_validate.access_token).toBe("string");
    expect(typeof to_validate.refresh_token).toBe("string");

    return to_validate;
}
