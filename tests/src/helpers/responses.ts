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
    export interface get_organizations {
      organizations: Organization[];
    }
  }
  export namespace organizations {
    export interface get extends Organization {};
    export interface get_members {
      members: number[];
    };
  }
  export namespace test {
    export interface signup {
      accessToken: string;
      refreshToken: string;
    }
    export namespace organizations {
      export interface create extends Organization {}
      export interface invite {}
    }
  }
}

export default RS;
