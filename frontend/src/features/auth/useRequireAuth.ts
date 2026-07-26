"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { authStorage, fetchMe, type AuthUser } from "@/features/auth/api";

/**
 * Client-side route guard. Verifies the token against the backend; redirects to /login if
 * absent or invalid. Returns the current user once confirmed (null while checking).
 */
export function useRequireAuth(): { user: AuthUser | null; checking: boolean } {
  const router = useRouter();
  const [user, setUser] = useState<AuthUser | null>(null);
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    let active = true;
    (async () => {
      const me = await fetchMe();
      if (!active) return;
      if (!me) {
        authStorage.clear();
        router.replace("/login");
        return;
      }
      setUser(me);
      setChecking(false);
    })();
    return () => {
      active = false;
    };
  }, [router]);

  return { user, checking };
}
