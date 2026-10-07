# GitHub Pages site package

This package contains only a static website shell and a manually triggered GitHub Pages workflow. It does not contain the local database, research records, credentials, or the content-generation system.

## Before making it public

The prepared page is a neutral placeholder. Do not replace it with affiliate content or publish it until the Associates account and public disclosure have been verified and the account holder authorizes the release.

For GitHub Free, GitHub Pages requires a public repository. The repository will expose its files publicly. Create a dedicated repository for this package; do not push the full local project.

## Setup

1. Create a dedicated public repository on GitHub.
2. Copy this package's `.github` directory, `site` directory, and this `README.md` to the repository root.
3. In the repository's Settings > Pages, select GitHub Actions as the publishing source.
4. After account readiness and the disclosure are verified, add these repository variables under Settings > Secrets and variables > Actions > Variables:
   - `AMAZON_ACCOUNT_READY` = `true`
   - `PUBLICATION_APPROVED` = `true`
5. To publish, open Actions, choose “Publish website to GitHub Pages”, select `yes` for the manual confirmation, and run the workflow.

The workflow is manual-only. Its default confirmation is `no`, and it stops unless both readiness variables are set to `true`.

## Website files

- `site/index.html`
- `site/style.css`
