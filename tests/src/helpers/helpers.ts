import { JWTPair } from "./types";
import api from "./api";
import { CaptureContext } from "pactum/src/exports/handler";


export const makeResponse = (ctx: CaptureContext) => {
  const fromSnaketoCamelCase = (str: string) => {
    let result = '';
    for (let i = 0; i < str.length; ++i) {
      if (str[i] == '_' && i != str.length - 1) {
        ++i;
        result += str[i].toUpperCase();
      } else {
        result += str[i];
      }
    }
    return result;
  }
  const replaceKeys = (source: any) => {
    for (let prop in source) {
      const upper = fromSnaketoCamelCase(prop);
      if (prop !== upper) {
        source[upper] = source[prop];
        delete source[prop];
      }
      if ('object' === typeof source[upper]) {
        replaceKeys(source[upper]);
      }
    }
  }
  replaceKeys(ctx.res.body);
  return ctx.res.body;
}

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
