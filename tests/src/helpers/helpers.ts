import { JWTPair } from "./types";
import api from "./api";


export class GlobalCounter {
  static counter: number = 0;

  static getNextNumber(): number {
    return ++GlobalCounter.counter;
  }

  static getNextEmail(): string {
    return GlobalCounter.getNextNumber() + '.email@gmail.com';
  }

  static getNextString(): string {
    return GlobalCounter.getNextNumber().toString();
  }
}

export class User {
  private constructor(
    public first_name: string,
    public email: string,
    public tokens: JWTPair
  ) {}

  static async signin(
    login: string,
    password: string
  ): Promise<User> {
    // TODO: create `get current user` method on backend
    throw new Error("Not implemented")
    const tokens: AuthSignin = await api.auth.signin()
      .withBody({login, password})
      .expectJsonLike({ok: true})
      .returns(ctx => ctx.res.body);
    return new User("no_username", "no_email", tokens);
  }

  static async signup(
    first_name: string,
    email: string,
    password: string
  ): Promise<User> {
    const tokens: AuthSignup = await api.auth.signup()
      .withBody({first_name, password, email})
      .expectJsonLike({ok: true})
      .returns(ctx => ctx.res.body);
    return new User(first_name, email, tokens)
  }
}