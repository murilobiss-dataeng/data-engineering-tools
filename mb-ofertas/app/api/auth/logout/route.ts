import { NextResponse } from "next/server";
import { cookies } from "next/headers";

const COOKIE_NAME = "mb_auth";

export async function POST() {
  const cookieStore = await cookies();
  cookieStore.delete(COOKIE_NAME);
  return NextResponse.json({ ok: true });
}
