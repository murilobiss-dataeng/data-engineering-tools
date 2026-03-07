import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const COOKIE_NAME = "mb_auth";
const MESSAGE = "mb_ofertas_session";

async function getExpectedToken(secret: string): Promise<string> {
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  const sig = await crypto.subtle.sign(
    "HMAC",
    key,
    new TextEncoder().encode(MESSAGE)
  );
  const b64 = btoa(String.fromCharCode(...new Uint8Array(sig)))
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, "");
  return b64;
}

export async function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl;

  if (pathname === "/login") {
    const token = req.cookies.get(COOKIE_NAME)?.value;
    const secret = process.env.SESSION_SECRET;
    if (token && secret) {
      try {
        const expected = await getExpectedToken(secret);
        if (token === expected) {
          return NextResponse.redirect(new URL("/", req.url));
        }
      } catch {
        // invalid cookie, show login
      }
    }
    return NextResponse.next();
  }

  if (pathname.startsWith("/api/auth/login")) {
    return NextResponse.next();
  }

  if (pathname.startsWith("/r/")) {
    return NextResponse.next();
  }

  if (pathname === "/logs") {
    return NextResponse.next();
  }

  const loginUser = process.env.LOGIN_USER;
  const loginPassword = process.env.LOGIN_PASSWORD;
  if (!loginUser || !loginPassword) {
    return NextResponse.next();
  }

  const token = req.cookies.get(COOKIE_NAME)?.value;
  const secret = process.env.SESSION_SECRET;
  if (!token || !secret) {
    return NextResponse.redirect(new URL("/login", req.url));
  }

  try {
    const expected = await getExpectedToken(secret);
    if (token !== expected) {
      return NextResponse.redirect(new URL("/login", req.url));
    }
  } catch {
    return NextResponse.redirect(new URL("/login", req.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
