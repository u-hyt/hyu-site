# GitHub Pages: purchase guides

This static site package contains fifty source-attributed, non-product-specific guides for checking PC accessory compatibility, plus a link to the independent university, high-school entrance, and parent-oriented elementary study guide site. The study guides compare books by subject and learning stage, cite publisher and MEXT sources, and link to tagged Amazon.co.jp search pages. The site does not claim product testing, personal use, rankings, or guaranteed admissions outcomes.

The site is a static package. It contains no credentials, local database, research inbox, or content-generation system. Article sources and check dates are shown on the page.

## Publish

1. In repository Settings > Pages, select GitHub Actions as the publishing source.
2. Open Actions and choose “Publish website to GitHub Pages”.
3. Select `yes` for the manual publication confirmation and run the workflow.

The workflow is manual-only and defaults to `no`. It deploys the static `site` folder. Once the deployment succeeds, GitHub Pages displays the live URL in the workflow run.

## Contents

- `site/mama/` — legacy URL redirects to the independent public Site `https://mama-reference-book.russet-sun-6909.chatgpt.site/`; parent and household guide content is maintained there.

- `site/index.html` — public guide index, including independent study-series links
- `site/about/` — editorial policy, source approach, and affiliate disclosure
- `site/university-books/`, `site/highschool-entrance/`, and `site/elementary-entrance/` — legacy redirects to the independent study guide site
- `site/highschool-entrance/` — high-school entrance reference-book routes for junior-high students
- `site/elementary-entrance/` — parent guide to elementary lesson-support materials and middle-school entrance prep
- `site/guide-1.html` through `site/guide-10.html` plus forty topic-named pages — individual guides with source notes and affiliate disclosures
- `site/style.css` — responsive layout
- `site/assets/` — original, accessible SVG diagrams
- `site/robots.txt` and `site/sitemap.xml` — crawl guidance and public URL list
- `.github/workflows/pages.yml` — manually triggered Pages deployment

The site displays an Associates disclosure near each search link and the program's required statement in the footer. Product facts and product endorsements are not generated from the search links.
