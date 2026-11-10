## YYYY-MM-DD - [Title]
**Learning:** [Insight]
**Action:** [How to apply next time]

## 2024-05-18 - Missing lazy loading on images
**Learning:** Found multiple places where images, including hero images and corridor navigation images, were missing the `loading="lazy"` attribute or missing it incorrectly. The journal also mentioned that the first image (hero) should NOT be lazy-loaded, to maintain LCP performance. The `.dc.html` files mentioned in `build_site.py` don't exist in the current tree, so I must modify the generated `.html` directly as stated in memory.
**Action:** When adding `loading="lazy"`, I must ensure I am NOT adding it to hero images, but only to images below the fold (e.g. corridor navigation images).
