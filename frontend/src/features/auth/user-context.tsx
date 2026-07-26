"use client";

import { createContext, useContext } from "react";

import type { AuthUser } from "@/features/auth/api";

/** The signed-in user, provided by the /app layout after the auth guard passes. */
export const UserContext = createContext<AuthUser | null>(null);

export function useCurrentUser(): AuthUser | null {
  return useContext(UserContext);
}
