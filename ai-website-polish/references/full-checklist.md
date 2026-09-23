# Pre-Launch Operational Checklist (Tier 3 Deep Reference)

Use this reference during Phase 5 (Asset & Link Hygiene and Pre-Launch Verification) when preparing an AI-generated site for public deployment.

## 1. SEO & Metadata Hygiene
- [ ] Unique, descriptive `<title>` on every route (format: `Primary Value Proposition | BrandName`)
- [ ] Unique meta description on every route (~150–160 characters, active voice)
- [ ] Open Graph metadata: `og:title`, `og:description`, `og:image` (1200×630 px), `og:url`
- [ ] Twitter card metadata: `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`
- [ ] Favicon bundle: `favicon.ico`, SVG icon, `apple-touch-icon.png`, and web manifest
- [ ] Crawl configuration: `robots.txt` and auto-generated `sitemap.xml`
- [ ] Semantic heading hierarchy: exactly one `<h1>` per view, sequential `<h2>`–`<h6>`
- [ ] Meaningful `alt` attributes on informative graphics; `alt=""` and `aria-hidden="true"` on purely decorative iconography

## 2. Mobile Touch & Responsive Hygiene
- [ ] Verified across 375px (iPhone SE) and 390px (iPhone 14/15/16) viewport widths
- [ ] Zero horizontal overflow (no body `overflow-x: hidden` hacks)
- [ ] Mobile navigation drawer traps focus, closes on Escape, and restores focus to hamburger trigger
- [ ] Touch targets for all interactive elements $\ge 44 \times 44\text{ px}$ on touch viewports
- [ ] Input zooming disabled safely: input font size $\ge 16\text{ px}$ on iOS Safari to prevent disruptive viewport zoom

## 3. Interaction & Async State Hygiene
- [ ] Indeterminate loading spinners or skeletons on every asynchronous dispatch exceeding 150ms
- [ ] Form submission buttons disabled and displaying spinner upon submit to prevent double-post mutations
- [ ] Clear field-level inline error messages linked with `aria-describedby`
- [ ] Meaningful empty states for zero-data lists, tables, and searches (with clear CTA to create/populate)
- [ ] Custom 404 Not Found page matching branding with navigation back to primary application routes
- [ ] Dedicated post-transaction confirmation state with clear transaction reference and next action

## 4. Content & Asset Hygiene
- [ ] All "Lorem Ipsum", "TODO", mock text, and placeholder copy completely removed
- [ ] Clickable `mailto:` and `tel:` links formatted with standard URI schemes
- [ ] Company logo links to root route (`/`)
- [ ] Copyright statement displays current dynamic year (`new Date().getFullYear()`)
- [ ] External links include `rel="noopener noreferrer"` when using `target="_blank"`
- [ ] Images served in modern formats (AVIF / WebP) with explicit `width`, `height`, and `aspect-ratio`

## 5. Legal, Trust & Compliance
- [ ] Privacy Policy page containing data handling, third-party analytics disclosures, and retention policies
- [ ] Terms of Service / Terms of Use page
- [ ] Cookie consent mechanism implemented where jurisdictionally required (GDPR, ePrivacy)
- [ ] Accessible contact or support channel clearly visible in navigation or footer
