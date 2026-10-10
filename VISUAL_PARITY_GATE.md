# Altora visual-parity gate

Canonical reference: `index.html` at the same desktop and mobile viewport.

A non-home page may have a project accent, but must pass every shared-system rule below before deployment.

## 1. Shell
- Floating white pill nav: same homepage top offset, `max-width:1240px`, radius, shadow, logo scale, nav link scale, and green CTA. The 20px value applies to the inner viewport gutter before the max width is reached.
- Same mobile header/burger/menu panel and link destinations.
- Same purple/blue gradient footer, column rhythm, brand block, footer base, and mobile stacking.

## 2. Typography
- Font files load on every page: Plus Jakarta Sans and JetBrains Mono.
- Shared heading scale only: H1 `clamp(2.55rem,5.25vw,4.05rem)`, H2 `clamp(1.9rem,3.5vw,2.85rem)`, H3 `1.06rem`.
- Same weights, line-height, tracking, eyebrow dot treatment, lead/body muted colors.

## 3. Layout rhythm
- Shared content container `width:min(100% - 40px,1240px)`.
- Shared section padding `var(--section-y)` and section gap `var(--section-gap)`.
- No independent fixed/max dimensions that create a second template unless it is evidence media.

## 4. Components
- Buttons use canonical `.btn`, `.btn-lg`, colors and pill radius.
- Cards use canonical radius/shadow/border tokens and hover behavior.
- CTA uses an existing home-page surface pattern, not an isolated flat band.

## 5. Page soul (allowed variance)
- Project-specific color/mood can appear in evidence framing, one accent, image treatment, and copy rhythm only.
- It must not alter the shell, type scale, button geometry, card system, mobile interaction, or footer.

## Verification (required)
1. Render `index.html`, page desktop 1440px, and page mobile 390px.
2. Compare header, first heading, one content card, CTA, and footer side-by-side.
3. Check each exact computed font family, size, line-height, border radius and background where applicable.
4. Test the mobile burger open/close and each shell link returns HTTP 200.
5. Do not deploy or say complete if a mismatch remains.
