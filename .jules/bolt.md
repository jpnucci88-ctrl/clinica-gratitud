## 2024-11-20 - [Performance] Google Fonts Preconnect
**Learning:** Google Fonts suggests adding a `preconnect` for `fonts.gstatic.com` which is often missed and forces the browser to wait for the CSS to be parsed before initiating a connection for the fonts, slowing down the LCP and font loading.
**Action:** Adding `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>` to `<head>` next to `fonts.googleapis.com` improves font loading time.
