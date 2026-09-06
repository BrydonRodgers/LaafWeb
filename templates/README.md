# LaafWeb starter templates

10 free templates sourced from HTML5UP and Start Bootstrap, one subfolder each,
covering: service business, restaurant/local shop, portfolio/freelancer,
e-commerce-lite, and general small-business layouts.

| id | category | license |
|---|---|---|
| strata | General small business | CCA 3.0 (html5up.net), attribution required |
| solid-state | Service business / agency | CCA 3.0 (html5up.net), attribution required |
| story | General small business | CCA 3.0 (html5up.net), attribution required |
| editorial | Portfolio / freelancer | CCA 3.0 (html5up.net), attribution required |
| read-only | Portfolio / photographer | CCA 3.0 (html5up.net), attribution required |
| freelancer | Portfolio / freelancer | MIT (Start Bootstrap) |
| small-business | Restaurant / local shop | MIT (Start Bootstrap) |
| shop-homepage | E-commerce-lite | MIT (Start Bootstrap) |
| agency | Service business / agency | MIT (Start Bootstrap) |
| modern-business | General small business | MIT (Start Bootstrap) |

**Note on licensing accuracy:** HTML5UP templates are Creative Commons
Attribution 3.0 (CCA 3.0), not MIT — free to use commercially but require a
credit link to html5up.net (kept in each template's untouched footer/README).
Start Bootstrap templates are genuinely MIT. Do not relabel the HTML5UP ones
as MIT — check each template's own `README.txt`/`LICENSE.txt` if in doubt.

## Reskin mechanism

Each template is otherwise untouched upstream code (unzipped/cloned as-is).
Two small, non-destructive additions were made to each template's main HTML
file:

1. A `<script src=".../_shared/inject-config.js" defer></script>` tag before `</body>`.
2. `data-lw-brand` / `data-lw-logo` attributes added to the existing nav
   brand/logo element, where the template has one simple enough to safely
   auto-replace (a couple of the HTML5UP templates — `strata`, `editorial` —
   have a full marketing sentence instead of a simple brand string in that
   slot, so brand-text swapping doesn't apply there; everything else
   — title, contact bar, brand colors — still works).

`templates/_shared/inject-config.js` reads a sibling `config.json` at page
load and applies it: page title, CSS custom properties `--lw-primary`/
`--lw-accent`, a generated contact bar (phone/email/address/WhatsApp), and
the two `data-lw-*` hooks above. This was chosen over hand-templating
`{{business_name}}`-style tokens into each of 10 different unique codebases
because it's the same script for every template (one place to maintain),
never risks corrupting a template's internal layout, and still gives a
future generator step everything it needs via one consistent `config.json`
schema per template (see the schema comment at the top of
`inject-config.js`).

## Choosing a template (Phase 1 signup step)

The signup flow's "Choose your style" step (`signup.html`) shows a
screenshot per template (`screenshots/<id>.png`, generated with headless
Chrome against each template's real rendered page) and stores the picked
`template_id` on the signup record via `POST /signup`.

## Generating a real site later (not built here, by design)

A future generator takes `{template_id, business_name, logo, colors,
contact_info}` from a `laafweb.signups` row, copies `templates/<template_id>/`,
writes a real `config.json` from those fields, and deploys — no changes to
this folder's structure required.
