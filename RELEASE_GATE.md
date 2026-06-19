# Release gate

This repository is a local, GitHub-ready staging package. It is not release-ready until the human-only metadata and publication choices below are completed.

## Current blocking items

- Replace the conservative `CITATION.cff` author placeholder with the final author metadata approved for public release.
- Confirm the public repository URL after the GitHub repository is created.
- Decide whether to mint an archive DOI or use the GitHub release URL only.
- Re-run both package checks immediately before public push.

## Required commands before public release

```bash
python scripts/write_manifest.py
python scripts/check_public_package.py
python scripts/check_release_ready.py
```

Expected current staging behavior:

- `check_public_package.py` should pass.
- `check_release_ready.py` should fail until `CITATION.cff` no longer contains the author-metadata placeholder.

## Human-only actions

- Create or publish the GitHub repository.
- Push `main`.
- Make the repository public.
- Create a release or mint an archive DOI.
- Replace citation metadata with final author-approved information.
