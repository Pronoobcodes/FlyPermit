import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_API_URL || "http://127.0.0.1:8000";

function setCookie(response: NextResponse, name: string, value: string, maxAge: number) {
  response.cookies.set({
    name,
    value,
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    path: "/",
    maxAge,
  });
}

function deleteCookie(response: NextResponse, name: string) {
  response.cookies.delete(name);
}

async function refreshAccessToken(refreshToken: string) {
  try {
    const res = await fetch(`${BACKEND_URL}/api/token/refresh/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh: refreshToken }),
    });
    if (!res.ok) return null;
    const data = await res.json();
    return data.access;
  } catch {
    return null;
  }
}

async function handleRequest(req: NextRequest) {
  const url = new URL(req.url);
  const path = url.pathname.replace(/^\/api/, "");
  const query = url.search;

  let accessToken = req.cookies.get("access_token")?.value;
  const refreshToken = req.cookies.get("refresh_token")?.value;

  const targetUrl = `${BACKEND_URL}/api${path}${query}`;
  const isAuthRequest = path.startsWith("/accounts/login") || path.startsWith("/accounts/register");

  if (!isAuthRequest && !accessToken && refreshToken) {
    const newAccess = await refreshAccessToken(refreshToken);
    if (newAccess) {
      accessToken = newAccess;
    }
  }

  const headers = new Headers();
  headers.set("Content-Type", "application/json");
  if (accessToken) {
    headers.set("Authorization", `Bearer ${accessToken}`);
  }

  let body: string | undefined = undefined;
  if (req.method !== "GET" && req.method !== "DELETE") {
    try {
      body = JSON.stringify(await req.json());
    } catch {}
  }

  if (path.startsWith("/accounts/logout") && req.method === "POST") {
    if (!refreshToken) {
      const errorRes = NextResponse.json({ success: false, message: "No active session." }, { status: 400 });
      return errorRes;
    }
    try {
      const backendRes = await fetch(targetUrl, {
        method: "POST",
        headers,
        body: JSON.stringify({ refresh: refreshToken }),
      });
      let data;
      try {
        data = await backendRes.json();
      } catch {
        data = { success: true, message: "Logout successful." };
      }
      const res = NextResponse.json(data, { status: backendRes.status });
      deleteCookie(res, "access_token");
      deleteCookie(res, "refresh_token");
      return res;
    } catch (e) {
      const res = NextResponse.json({ success: false, message: "Failed to log out." }, { status: 500 });
      deleteCookie(res, "access_token");
      deleteCookie(res, "refresh_token");
      return res;
    }
  }

  try {
    const backendRes = await fetch(targetUrl, {
      method: req.method,
      headers,
      body,
    });

    const isJson = backendRes.headers.get("content-type")?.includes("application/json");
    const data = isJson ? await backendRes.json() : await backendRes.text();

    const response = NextResponse.json(data, { status: backendRes.status });

    if (isAuthRequest && backendRes.ok && data.success && data.data) {
      const { access, refresh } = data.data;
      if (access) {
        setCookie(response, "access_token", access, 3600);
      }
      if (refresh) {
        setCookie(response, "refresh_token", refresh, 7 * 24 * 3600);
      }
      delete data.data.access;
      delete data.data.refresh;
      return NextResponse.json(data, { status: backendRes.status });
    }

    if (backendRes.status === 401 && refreshToken && !isAuthRequest) {
      const newAccess = await refreshAccessToken(refreshToken);
      if (newAccess) {
        headers.set("Authorization", `Bearer ${newAccess}`);
        const retryRes = await fetch(targetUrl, {
          method: req.method,
          headers,
          body,
        });
        const retryData = isJson ? await retryRes.json() : await retryRes.text();
        const finalResponse = NextResponse.json(retryData, { status: retryRes.status });
        setCookie(finalResponse, "access_token", newAccess, 3600);
        return finalResponse;
      }
    }

    return response;
  } catch (err: any) {
    return NextResponse.json(
      { success: false, message: "Backend connection error.", errors: err.message },
      { status: 502 }
    );
  }
}

export async function GET(req: NextRequest) { return handleRequest(req); }
export async function POST(req: NextRequest) { return handleRequest(req); }
export async function PUT(req: NextRequest) { return handleRequest(req); }
export async function PATCH(req: NextRequest) { return handleRequest(req); }
export async function DELETE(req: NextRequest) { return handleRequest(req); }
