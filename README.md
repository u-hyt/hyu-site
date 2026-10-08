# GitHub Pages: purchase guides

This static site package contains ten source-attributed, non-product-specific guides for checking PC accessory compatibility. Each guide is available at its own URL and links to a tagged Amazon.co.jp search page for related products. The site does not claim product testing, personal use, prices, or rankings.

The site is a static package. It contains no credentials, local database, research inbox, or content-generation system. Article sources and check dates are shown on the page.

## Publish

1. In repository Settings > Pages, select GitHub Actions as the publishing source.
2. Open Actions and choose “Publish website to GitHub Pages”.
3. Select `yes` for the manual publication confirmation and run the workflow.

The workflow is manual-only and defaults to `no`. It deploys the static `site` folder. Once the deployment succeeds, GitHub Pages displays the live URL in the workflow run.

## Contents

- `site/index.html` — public guide index
- `site/guide-1.html` through `site/guide-10.html` — individual guides with source notes and affiliate disclosures
- `site/style.css` — responsive layout
- `site/assets/` — original, accessible SVG diagrams
- `site/robots.txt` and `site/sitemap.xml` — crawl guidance and public URL list
- `.github/workflows/pages.yml` — manually triggered Pages deployment

The site displays an Associates disclosure near each search link and the program's required statement in the footer. Product facts and product endorsements are not generated from the search links.
