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
  }
  export namespace test {
    export interface signup {
      accessToken: string;
      refreshToken: string;
    }
  }
}

export default RS;
