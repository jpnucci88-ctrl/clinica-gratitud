## 2024-05-19 - [Missing font preconnects]
**Learning:** Google Fonts requires preconnecting to both `fonts.googleapis.com` (for the CSS) and `fonts.gstatic.com` (for the font files). The codebase only preconnected to `fonts.googleapis.com`.
**Action:** Always check if `fonts.gstatic.com` preconnect is present when using Google Fonts to ensure optimal font loading performance.
