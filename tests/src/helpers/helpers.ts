import { JWTPair } from "./types";
import api from "./api";
import { CaptureContext } from "pactum/src/exports/handler";
import RS from "./responses";


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
    public id: number,
    public tokens: JWTPair
  ) {}

  static async signin(
    email: string,
    password: string
  ): Promise<User> {
    const tokens: RS.AuthSignin = await api.auth.signin()
      .withBody({email, password})
      .expectJsonLike({ok: true})
      .returns(makeResponse);
    const current_user: RS.AuthCurrent = await api.auth.current()
      .withBearerToken(tokens.accessToken)
      .returns(makeResponse);
    return new User(current_user.first_name, current_user.email, current_user.id, tokens);
  }

  static async signup(
    first_name: string,
    email: string,
    password: string
  ): Promise<User> {
    const tokens: RS.AuthSignup = await api.auth.signup()
      .withBody({first_name, password, email})
      .expectJsonLike({ok: true})
      .returns(ctx => ctx.res.body);
    const current_user: RS.AuthCurrent = await api.auth.current()
      .withBearerToken(tokens.accessToken)
      .returns(makeResponse);
    return new User(current_user.first_name, current_user.email, current_user.id, tokens);
  }
}
