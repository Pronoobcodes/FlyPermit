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

async function refreshTokens(refreshToken: string) {
  try {
    const res = await fetch(`${BACKEND_URL}/api/token/refresh/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh: refreshToken }),
    });
    if (!res.ok) return null;
    return await res.json();
  } catch {
    return null;
  }
}

async function handleRequest(req: NextRequest) {
  try {
    const url = new URL(req.url);
    let path = url.pathname.replace(/^\/api/, "");
    const query = url.search;

    // Django expects trailing slashes for POST/PUT/PATCH/DELETE
    if (!path.endsWith("/")) {
      path += "/";
    }

    let accessToken = req.cookies.get("access_token")?.value;
    const refreshToken = req.cookies.get("refresh_token")?.value;

    const targetUrl = `${BACKEND_URL}/api${path}${query}`;
    const isAuthRequest = path.startsWith("/accounts/login") || path.startsWith("/accounts/register");

    let newlyRefreshedTokens: any = null;

    if (!isAuthRequest && !accessToken && refreshToken) {
      newlyRefreshedTokens = await refreshTokens(refreshToken);
      if (newlyRefreshedTokens && newlyRefreshedTokens.access) {
        accessToken = newlyRefreshedTokens.access;
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
        const parsedBody = await req.json();
        body = JSON.stringify(parsedBody);
      } catch (e) {
        console.warn("Failed to parse request JSON body:", e);
      }
    }

    if (path.startsWith("/accounts/logout") && req.method === "POST") {
      if (!refreshToken) {
        return NextResponse.json({ success: false, message: "No active session." }, { status: 400 });
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
        return response;
      }

      // If we refreshed tokens PRE-request, set the cookies now
      if (newlyRefreshedTokens) {
        if (newlyRefreshedTokens.access) setCookie(response, "access_token", newlyRefreshedTokens.access, 3600);
        if (newlyRefreshedTokens.refresh) setCookie(response, "refresh_token", newlyRefreshedTokens.refresh, 7 * 24 * 3600);
      }

      // If we got 401, try to refresh POST-request
      if (backendRes.status === 401 && refreshToken && !isAuthRequest && !newlyRefreshedTokens) {
        const tokens = await refreshTokens(refreshToken);
        if (tokens && tokens.access) {
          headers.set("Authorization", `Bearer ${tokens.access}`);
          const retryRes = await fetch(targetUrl, {
            method: req.method,
            headers,
            body,
          });
          const retryData = isJson ? await retryRes.json() : await retryRes.text();
          const finalResponse = NextResponse.json(retryData, { status: retryRes.status });
          setCookie(finalResponse, "access_token", tokens.access, 3600);
          if (tokens.refresh) {
            setCookie(finalResponse, "refresh_token", tokens.refresh, 7 * 24 * 3600);
          }
          return finalResponse;
        } else {
          // Refresh failed (e.g. refresh token is blacklisted or expired)
          deleteCookie(response, "access_token");
          deleteCookie(response, "refresh_token");
        }
      } else if (backendRes.status === 401 && newlyRefreshedTokens) {
         // Even our newly refreshed token failed, or we couldn't refresh. Kill session.
         deleteCookie(response, "access_token");
         deleteCookie(response, "refresh_token");
      }

      return response;
    } catch (err: any) {
      console.error("[PROXY FETCH ERROR]", err);
      return NextResponse.json(
        { success: false, message: "Backend connection error.", errors: err.message },
        { status: 502 }
      );
    }
  } catch (error: any) {
    console.error("[ROUTE HANDLER ERROR]", error);
    return NextResponse.json({ error: "Internal server error", details: error.message }, { status: 500 });
  }
}

export async function GET(req: NextRequest) { return handleRequest(req); }
export async function POST(req: NextRequest) { return handleRequest(req); }
export async function PUT(req: NextRequest) { return handleRequest(req); }
export async function PATCH(req: NextRequest) { return handleRequest(req); }
export async function DELETE(req: NextRequest) { return handleRequest(req); }
