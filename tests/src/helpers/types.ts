export interface JWTPair {
  accessToken: string;
  refreshToken: string;
}

export interface Organization {
  id: number;
  name: string;
  members: {
    id: number;
    customPermissions: number;
    roles: string[];
  }[];
  roles: {
    id: number;
    name: string;
    permissions: number;
  }[];
}
