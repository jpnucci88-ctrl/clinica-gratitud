## 2026-10-26 - Missing Preconnect for Google Fonts
**Learning:** Google Fonts are often added with `<link rel="preconnect" href="https://fonts.googleapis.com">` but miss the connection to `fonts.gstatic.com`, where the actual font files are hosted. Adding `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>` can significantly improve FCP (First Contentful Paint) by eliminating the connection overhead for downloading the font files themselves.
**Action:** Always check for missing `fonts.gstatic.com` preconnect when optimizing Google Fonts.
