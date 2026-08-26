# Project Brief — [Leather dynamic]

## What this project is
A premium e-commerce website for a company selling leather products (bags, wallets, belts, jackets — adjust to the actual product line). The site should feel like a high-end fashion/craft brand, not a generic Django admin-style storefront. Reference feel: cinematic scroll-triggered animations, confident large typography, a rotating hero product shot — similar to premium agency landing pages (e.g. "All Star Burgers" and "GymCare" style demos).

## Tech stack — HARD CONSTRAINTS
- Backend: Django + Django REST Framework
- Frontend: Django templates + vanilla HTML/CSS/JavaScript
- Do NOT use React, Vue, Next.js, or any JS framework/bundler (no npm build step for the frontend)
- Animation libraries: GSAP + ScrollTrigger (scroll-based reveals, pinning) and Lenis (smooth inertia scrolling) — loaded via CDN in base.html
- Optional: Three.js only if we add a real 3D rotating product model; otherwise fake "3D" rotation with a sprite-sheet of product photos + scroll-linked frame swapping

## Visual direction
- Palette: dark & luxurious — black / charcoal (#0a0a0a, #1a1a1a) base, with gold/brass accent (#c9a04d or similar) for CTAs, borders, and highlights
- Typography: a bold, high-contrast display serif or condensed sans for headings (evokes craftsmanship/luxury); a clean neutral sans for body text
- Imagery: full-bleed, high-contrast product photography on dark backgrounds; generous negative space; no clutter
- Motion: subtle and premium, not gimmicky — slow easing (power2/power3), fade+slide reveals on scroll, a hero section that animates in on load, smooth scroll throughout, a pinned/rotating product showcase section

## Page structure (v1)
1. **Home** — hero (brand statement + hero product), featured collection strip, brand story teaser, rotating product showcase section, footer
2. **Shop** — product grid, filter by category, pulled from DRF API
3. **Product Detail** — large imagery, description, materials/craftsmanship notes, add-to-cart
4. **About** — brand story, craftsmanship process, materials sourcing
5. **Contact** — form (wired to a DRF endpoint), store/workshop info if relevant

## Backend / API notes
- DRF endpoints needed: `/api/products/`, `/api/products/<id>/`, `/api/cart/`, `/api/contact/`
- Use Django templates for the actual pages (SEO-friendly, fast first paint); use DRF + fetch() for dynamic pieces (product grid filtering, cart updates, contact form submission) so pages don't fully reload
- Keep static assets organized: `static/css/`, `static/js/`, `static/img/`

## Working style for this project
- Build one section/page at a time — don't scaffold the whole site in one shot
- After each section, pause for review before moving to the next
- Keep animation code isolated in its own JS file(s) (e.g. `static/js/animations.js`) separate from any interactive/DRF-fetching JS
- Prioritize performance — lazy-load large images, keep GSAP timelines lightweight

## Not yet decided (fill in as we go)
- Final brand name and logo
- Product catalog (real products/photos vs placeholder)
- Payment integration (Stripe? Manual/WhatsApp order flow?)
- Hosting target (Railway, Render, VPS?)
