# Eterna Jan Clone Workspace

This repository is prepared to host a clean clone of the [Jan](https://github.com/janhq/jan) project as requested.

The previous generated assets have been removed so that the tree matches Jan's structure once the clone completes. Because the build environment cannot reach GitHub directly (CONNECT tunnel returns 403), the actual `git clone` must be executed from a network-enabled environment. The helper script below documents the exact command to run:

```bash
./scripts/clone_jan.sh
```

After cloning Jan, you can proceed with any Eterna-specific adaptations on top of that baseline.
