## 2026-10-30 - [Missing gstatic.com preconnect]
**Learning:** Google Fonts suggests adding a `preconnect` link to `fonts.gstatic.com` for cross-origin font downloads. The site only had `fonts.googleapis.com` preconnected.
**Action:** Always verify if external CDNs are properly preconnected (especially for Google Fonts) to improve download and rendering times.
