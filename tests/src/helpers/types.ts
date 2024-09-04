export interface JWTPair {
  accessToken: string;
  refreshToken: string;
}

export interface Organization {
  id: number;
  name: string;
  members: number[];
}
