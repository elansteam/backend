export interface JWTPair {
  accessToken: string;
  refreshToken: string;
}

interface HasMembersWithRoles {
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

export interface Organization extends HasMembersWithRoles {
  id: number;
  name: string;
}
