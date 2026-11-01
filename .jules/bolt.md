## 2026-11-01 - [Missing Native Lazy Loading on HTML Images]
**Learning:** Found multiple images in the plain HTML static site missing the `loading="lazy"` attribute. By default images are eagerly loaded, which blocks the main thread parsing and wastes bandwidth on images off-screen. Since the codebase is plain HTML without a build step or bundler handling these optimizations, this must be added manually.
**Action:** Next time when encountering a plain HTML static site, grep for `<img` tags without `loading="lazy"` to easily find performance wins for network and parsing optimization.
