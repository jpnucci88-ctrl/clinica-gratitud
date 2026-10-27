## 2024-05-24 - HTML files are the source of truth

**Learning:** Despite the existence of a build script `_ferramentas/build_site.py` meant to process `.dc.html` files, the repository does not contain `.dc.html` files. The standard `.html` files in the root directory act as the source of truth and must be directly modified.

**Action:** Before assuming a build pipeline is active, check for the presence of the source files it expects. Direct modification of artifacts might be required if the upstream sources are missing.
