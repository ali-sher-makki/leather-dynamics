---
name: premium-ui-ux
description: Design and animation standards for building premium, agency-quality web pages with vanilla HTML/CSS/JS + GSAP/Lenis. Use whenever building, styling, or animating any page or section of the leather e-commerce site.
---

# Premium UI/UX Standards

Apply these rules to every page/section you build for this project, without being asked each time.

## Typography
- Max 2 font families: one bold display font for headings, one neutral sans for body
- Type scale should feel deliberate, not default - headings noticeably larger than typical Bootstrap defaults (hero H1: 4.5-7rem on desktop)
- Generous line-height on body text (1.5-1.7), tight line-height on large display headings (1.0-1.1)

## Spacing and Layout
- Section vertical padding: minimum 6-10rem on desktop, never cramped
- Use a consistent spacing scale (e.g. 8px base unit: 8/16/24/32/48/64/96/128) - never arbitrary pixel values
- Generous negative space around hero product imagery - don't let content touch edges

## Color and Contrast
- Stick to the project's defined palette (see CLAUDE.md) - no ad-hoc colors
- On dark backgrounds, avoid pure white text (#fff) - use a slightly warm off-white (#f2f0ec) for comfort
- Accent color (gold) used sparingly: CTAs, borders, hover states - never as a large fill

## Motion (GSAP + ScrollTrigger + Lenis)
- Default easing: power2.out or power3.out - never linear, never bouncy/elastic unless explicitly asked
- Default duration: 0.6-1.2s for reveals, 0.3-0.4s for hover/micro-interactions
- Scroll-triggered reveals: elements start slightly offset (20-40px translateY, opacity 0) and settle into place - don't overdo it with rotation/skew unless it's a hero moment
- Stagger related elements (e.g. product cards) by 0.08-0.15s rather than animating them all at once
- Always initialize Lenis smooth scroll once, globally, and sync it with ScrollTrigger's scrollerProxy
- Respect prefers-reduced-motion - disable/simplify animations for users who request it

## Imagery
- Product photography should be full-bleed or large-format, never small thumbnails in hero/feature sections
- Use object-fit: cover with fixed-aspect containers to keep layouts stable
- Lazy-load below-the-fold images

## Code hygiene for this project
- Keep animation logic in static/js/animations.js, separate from DRF-fetching logic
- Use CSS custom properties for the color palette and spacing scale, defined once in a :root block
- Every interactive element needs a visible hover/focus state - no dead-looking buttons

## What to avoid
- Generic Bootstrap-card layouts with default shadows
- Animation for animation's sake - every motion should reinforce hierarchy or delight, not distract
- More than 2-3 animation styles per page (keep the motion language consistent)
