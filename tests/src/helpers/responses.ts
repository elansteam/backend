namespace RS {
  export interface AuthSignin {
    accessToken: string;
    refreshToken: string;
  }

  export interface AuthSignup {
    accessToken: string;
    refreshToken: string;
  }

  export interface AuthCurrent {
    id: number;
    first_name: string;
    email: string
  }

  export interface AuthRefresh {
    accessToken: string;
    refreshToken: string;
  }
}

export default RS;
