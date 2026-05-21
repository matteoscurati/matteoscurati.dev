---
name: verify
description: Run lint, type check, and build to catch errors before marking work done.
---

Run all checks in sequence. Stop at the first failure and fix it before continuing.

```bash
npm run lint && npm run check && npm run build
```

If any step fails:

1. Read the error output carefully
2. Fix the issue
3. Re-run from the beginning to confirm

Do not mark work as complete until all three pass.
