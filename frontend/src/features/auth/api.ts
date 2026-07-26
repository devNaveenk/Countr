/** Auth feature — API calls + token/session storage. All auth transport lives here. */

import { api } from "@/lib/api/client";

export type UserRole = "owner" | "cashier";

export interface AuthUser {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: AuthUser;
}

const TOKEN_KEY = "countr.access_token";
const USER_KEY = "countr.user";

export const authStorage = {
  save(res: TokenResponse) {
    localStorage.setItem(TOKEN_KEY, res.access_token);
    localStorage.setItem(USER_KEY, JSON.stringify(res.user));
  },
  token(): string | null {
    if (typeof window === "undefined") return null;
    return localStorage.getItem(TOKEN_KEY);
  },
  user(): AuthUser | null {
    if (typeof window === "undefined") return null;
    const raw = localStorage.getItem(USER_KEY);
    return raw ? (JSON.parse(raw) as AuthUser) : null;
  },
  clear() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  },
};

export function registerUser(input: {
  email: string;
  full_name: string;
  password: string;
}) {
  return api.post<TokenResponse>("/auth/register", { ...input, role: "owner" });
}

export function loginUser(input: { email: string; password: string }) {
  return api.post<TokenResponse>("/auth/login", input);
}

/** Verify the current token against the backend and return the fresh user, or null. */
export async function fetchMe(): Promise<AuthUser | null> {
  const token = authStorage.token();
  if (!token) return null;
  const base = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";
  const res = await fetch(`${base}/auth/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) return null;
  return (await res.json()) as AuthUser;
}
