import { Organization } from "./types";

namespace RS {
  export namespace auth {
    export interface signin {
      accessToken: string;
      refreshToken: string;
    }
    export interface refresh {
      accessToken: string;
      refreshToken: string;
    }
  }
  export namespace users {
    export interface current {
      id: number;
      firstName: string;
      email: string;
    }
    export interface get_orgs {
      organizations: Organization[];
    }
  }
  export namespace test {
    export interface signup {
      accessToken: string;
      refreshToken: string;
    }
    export namespace orgs {
      export interface create extends Organization {}
      export interface invite {}
    }
  }
}

export default RS;
