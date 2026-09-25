import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const authRoutes = ["/login", "/signup"];
const protectedRoutes = ["/documents", "/settings", "/chats"];

export function proxy(request: NextRequest) {
  const token = request.cookies.get("access_token")?.value;
  const { pathname } = request.nextUrl;

  const isAuthRoute = authRoutes.some((route) => pathname.startsWith(route));
  
  // FIX: Check exact match for home route "/" separately from prefixes like "/documents"
  const isProtectedRoute = 
    pathname === "/" || 
    protectedRoutes.some((route) => pathname.startsWith(route));

  // Redirect authenticated users away from /login & /signup to Home
  if (isAuthRoute && token) {
    return NextResponse.redirect(new URL("/", request.url));
  }

  // Redirect unauthenticated users to /login
  if (isProtectedRoute && !token) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("from", pathname);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * Match all request paths except static files, Next.js internal RSC data requests, and API routes
     */
    "/((?!api|_next/static|_next/image|_next/data|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
};