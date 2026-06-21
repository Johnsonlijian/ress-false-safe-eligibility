# Release gate

This repository is the public reproducibility package for the associated RESS submission. The author metadata has been inserted, and the package is ready for release after the checks below pass.

## Release items

- Re-run both package checks immediately before public push.
- Confirm the public repository URL after the GitHub repository is created.
- Create a versioned release.
- Mint or attach an archive DOI when an archival service is available.

## Required commands before public release

```bash
python scripts/write_manifest.py
python scripts/check_public_package.py
python scripts/check_release_ready.py
```

Expected behavior:

- `check_public_package.py` should pass.
- `check_release_ready.py` should pass.

## Public-release actions

- Create or publish the GitHub repository.
- Push `main`.
- Make the repository public.
- Create a release or mint an archive DOI.
