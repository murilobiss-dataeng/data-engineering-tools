import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import crypto from "crypto";

const COOKIE_NAME = "mb_auth";
const MESSAGE = "mb_ofertas_session";

function signToken(secret: string): string {
  return crypto.createHmac("sha256", secret).update(MESSAGE).digest("base64url");
}

export async function POST(req: NextRequest) {
  const secret = process.env.SESSION_SECRET;
  const loginUser = process.env.LOGIN_USER;
  const loginPassword = process.env.LOGIN_PASSWORD;

  if (!secret || !loginUser || !loginPassword) {
    return NextResponse.json(
      { error: "Login não configurado (defina LOGIN_USER, LOGIN_PASSWORD e SESSION_SECRET no .env)" },
      { status: 500 }
    );
  }

  let body: { username?: string; password?: string };
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "Corpo inválido" }, { status: 400 });
  }

  const username = String(body.username ?? "").trim();
  const password = String(body.password ?? "");

  if (username !== loginUser || password !== loginPassword) {
    return NextResponse.json({ error: "Usuário ou senha incorretos" }, { status: 401 });
  }

  const token = signToken(secret);
  const cookieStore = await cookies();
  cookieStore.set(COOKIE_NAME, token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    maxAge: 60 * 60 * 24 * 7, // 7 dias
    path: "/",
  });

  return NextResponse.json({ ok: true });
}
