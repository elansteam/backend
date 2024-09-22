import { CaptureContext } from "pactum/src/exports/handler";


export const makeResponse = (ctx: CaptureContext): any => {
  const fromSnakeToCamelCase = (str: string) => {
    let result = "";
    for (let i = 0; i < str.length; ++i) {
      if (str[i] == "_" && i != str.length - 1) {
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
      const upper = fromSnakeToCamelCase(prop);
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
  if ("ok" in ctx.res.body) {
    delete ctx.res.body["ok"];
  }
  return ctx.res.body;
}

export const makeRequest = (object: any): any => {
  const fromCamelCaseToSnake = (str: string) => {
    let result = "";
    for (let i = 0; i < str.length; ++i) {
      if (str[i].toUpperCase() == str[i]) {
        result += "_" + str[i].toLowerCase();
      } else {
        result += str[i];
      }
    }
    return result;
  }
  const replaceKeys = (source: any) => {
    for (let prop in source) {
      const upper = fromCamelCaseToSnake(prop);
      if (prop !== upper) {
        source[upper] = source[prop];
        delete source[prop];
      }
      if ('object' === typeof source[upper]) {
        replaceKeys(source[upper]);
      }
    }
  }
  replaceKeys(object);
  return object;
}
