---
name: website-data-protection
description: Hardens full-stack web applications against data breaches, broken access control (OWASP A01), injection flaws, and supply chain threats. Trigger when securing Next.js Server Actions, configuring strict Content Security Policies, auditing authentication/authorization boundaries, or mitigating slopsquatting package hallucinations. Do NOT trigger for purely visual styling or superficial design tweaks.
compatibility: Node.js 20+, Next.js 14+ App Router, Python 3.10+, Semgrep CLI.
---

# Website Data Protection Protocol

Apply this defense framework to eliminate structural vulnerabilities in modern web architectures, with specific focus on server-side authorization boundaries, dynamic CSP, and supply-chain vetting.

---

## 1. Server-Side Authorization Invariants (Next.js Server Actions & APIs)

Every Server Action (`"use server"`) compiles into an independent, publicly accessible HTTP POST endpoint callable by any client via the `next-action` header. Never rely on client-side UI visibility or assume parameters are trusted.

### Mandatory Execution Invariants:
1. **Server-Side Authentication**: Explicitly verify the caller's session identity server-side before executing any mutation logic.
2. **Runtime Schema Parsing**: Parse all arguments through strict `zod` schemas. Reject unvalidated parameters.
3. **Tenant Isolation (Object-Level Authorization / BOLA)**: Validate that the target resource is strictly owned by the authenticated tenant before mutating or querying.
4. **Parameterized Mutations**: Always use parameterized queries or trusted ORM methods to eliminate injection vectors.

```typescript
// Enforce strict server-side schema parsing and tenant authorization
'use server';

import { z } from 'zod';
import { auth } from '@/lib/auth';
import { db } from '@/lib/db';

const UpdateRecordSchema = z.object({
  recordId: z.string().uuid(),
  payload: z.string().min(1).max(5000).trim(),
});

export async function updateRecordAction(rawInput: unknown) {
  // 1. Mandatory server-side authentication check
  const session = await auth();
  if (!session?.user?.id) {
    throw new Error('UNAUTHORIZED: Authentication session required.');
  }

  // 2. Strict runtime schema validation
  const parsed = UpdateRecordSchema.safeParse(rawInput);
  if (!parsed.success) {
    throw new Error(`BAD_REQUEST: ${parsed.error.message}`);
  }

  const { recordId, payload } = parsed.data;

  // 3. Mandatory Object-Level Authorization (Tenant Isolation)
  const existingRecord = await db.document.findUnique({
    where: { id: recordId },
    select: { organizationId: true },
  });

  if (!existingRecord || existingRecord.organizationId !== session.user.organizationId) {
    throw new Error('FORBIDDEN: Caller lacks authorization for target resource.');
  }

  // 4. Parameterized mutation execution
  return await db.document.update({
    where: { id: recordId },
    data: { content: payload, updatedAt: new Date() },
  });
}
```

---

## 2. Cryptographic Nonce-Based Content Security Policy

Brittle domain allowlists are easily bypassed via CDN script hosting and open redirects. Production systems must implement dynamic cryptographic nonces using `'strict-dynamic'`:

```typescript
// middleware.ts - Production Strict Nonce CSP Implementation
import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  const nonce = Buffer.from(crypto.randomUUID()).toString('base64');

  const cspHeader = `
    default-src 'self';
    script-src 'self' 'nonce-${nonce}' 'strict-dynamic' ${
      process.env.NODE_ENV === 'development' ? "'unsafe-eval'" : ""
    };
    style-src 'self' 'nonce-${nonce}';
    img-src 'self' blob: data: https:;
    font-src 'self';
    object-src 'none';
    base-uri 'none';
    form-action 'self';
    frame-ancestors 'none';
    upgrade-insecure-requests;
  `.replace(/\s{2,}/g, ' ').trim();

  const requestHeaders = new Headers(request.headers);
  requestHeaders.set('x-nonce', nonce);
  requestHeaders.set('Content-Security-Policy', cspHeader);

  const response = NextResponse.next({
    request: { headers: requestHeaders },
  });

  response.headers.set('Content-Security-Policy', cspHeader);
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  response.headers.set(
    'Strict-Transport-Security',
    'max-age=63072000; includeSubDomains; preload'
  );

  return response;
}

export const config = {
  matcher: [
    {
      source: '/((?!api|_next/static|_next/image|favicon.ico).*)',
      missing: [
        { type: 'header', key: 'next-router-prefetch' },
        { type: 'header', key: 'purpose', value: 'prefetch' },
      ],
    },
  ],
};
```
*Note: Ensure any route utilizing nonce-based CSP is dynamically rendered at runtime (e.g., consuming `await connection()`) to prevent stale nonce caching.*

---

## 3. Client Secrets Exposure Prevention

AI models frequently import administrative credentials into client-side components:
- **Forbidden**: `const supabase = createClient(url, process.env.SUPABASE_SERVICE_ROLE_KEY)` inside client files (`"use client"`).
- **Enforcement**: Administrative clients must reside strictly in isolated backend modules (`lib/server/`). Use automated pre-commit scanners (TruffleHog, GitGuardian) to block any committed API keys or service role tokens.

---

## 4. Supply-Chain Hallucination Defense (Anti-Slopsquatting)

AI code generators hallucinate package dependencies in ~20% of complex dependency scenarios. Attackers register these hallucinated names on npm/PyPI with embedded post-install malware.

Before committing or installing packages:
1. Verify package existence on official registries.
2. Reject packages published $<14\text{ days}$ ago or possessing $<500$ weekly downloads unless explicitly reviewed.
3. Enforce deterministic CI verification with `slopgate`:
   ```bash
   pip install slopgate && slopgate scan . --strict
   ```

---

## 5. Automated DevSecOps Static Analysis Gate

Before approving or deploying code, execute Semgrep rulesets targeting broken access control and framework vulnerabilities:

```bash
semgrep scan --config "p/owasp-top-ten" --config "p/nextjs"
```

Verify zero `High` or `Critical` findings across all generated and refactored files.

---

## 6. Extended References & Templates (Tier 3)

- Slopsquat GitHub Actions Workflow: [assets/slopsquat-gate.yml](assets/slopsquat-gate.yml)
- Complete OWASP Top 10 & API Hardening Guide: [references/security-hardening-guide.md](references/security-hardening-guide.md)
