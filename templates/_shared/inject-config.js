/**
 * LaafWeb template config injector.
 *
 * Every template in templates/<id>/ ships an unmodified copy of the
 * upstream template plus a config.json following the shared schema below.
 * Rather than hand-editing each template's unique markup (10 different
 * codebases, each with its own CSS structure — editing internals risks
 * breaking layouts and would need re-doing per template forever), this one
 * script does the reskin generically at load time from config.json, using
 * only two non-destructive hooks:
 *
 *   1. Elements marked `data-lw-logo`  -> swapped to config.logo_path
 *   2. Elements marked `data-lw-brand` -> text replaced with config.business_name
 *
 * Those two attributes are the only edits made to each template's HTML
 * (added to the existing nav/logo markup, nothing removed or restructured).
 * Everything else (page <title>, a standard contact bar, CSS custom
 * properties for brand colors) is injected purely via JS/DOM, so it works
 * identically across every template regardless of its internal structure.
 *
 * config.json schema (same keys, same meaning, in every templates/<id>/):
 * {
 *   "business_name": "string",
 *   "logo_path": "relative/path/or/url.png",
 *   "primary_color": "#rrggbb",
 *   "accent_color": "#rrggbb",
 *   "contact": {
 *     "phone": "string",
 *     "email": "string",
 *     "address": "string",
 *     "whatsapp": "27xxxxxxxxx"
 *   }
 * }
 *
 * A future site-generation step reads {template_id, business_name, logo,
 * colors, contact_info} from a signup record and can drop a config.json
 * into a copy of templates/<template_id>/ to produce a real site — no
 * changes to this folder's structure required.
 */
(function () {
  async function loadConfig() {
    const res = await fetch('config.json', { cache: 'no-store' });
    if (!res.ok) throw new Error('config.json not found next to this template');
    return res.json();
  }

  function applyBrand(cfg) {
    if (cfg.business_name) {
      document.title = cfg.business_name + ' — ' + document.title;
      document.querySelectorAll('[data-lw-brand]').forEach((el) => {
        el.textContent = cfg.business_name;
      });
    }
    if (cfg.logo_path) {
      document.querySelectorAll('[data-lw-logo]').forEach((el) => {
        if (el.tagName === 'IMG') el.src = cfg.logo_path;
        else el.style.backgroundImage = `url(${cfg.logo_path})`;
      });
    }
  }

  function applyColors(cfg) {
    const root = document.documentElement.style;
    if (cfg.primary_color) root.setProperty('--lw-primary', cfg.primary_color);
    if (cfg.accent_color) root.setProperty('--lw-accent', cfg.accent_color);
  }

  function applyContactBar(cfg) {
    const c = cfg.contact || {};
    const bar = document.createElement('div');
    bar.id = 'lw-contact-bar';
    bar.style.cssText =
      'position:fixed;left:0;right:0;bottom:0;z-index:99999;background:#111;color:#eee;' +
      'font:13px/1.5 -apple-system,Arial,sans-serif;padding:8px 16px;display:flex;' +
      'gap:16px;flex-wrap:wrap;justify-content:center;border-top:2px solid var(--lw-primary,#007847)';
    const parts = [];
    if (c.phone) parts.push(`<a href="tel:${c.phone}" style="color:#eee;text-decoration:none">📞 ${c.phone}</a>`);
    if (c.email) parts.push(`<a href="mailto:${c.email}" style="color:#eee;text-decoration:none">✉️ ${c.email}</a>`);
    if (c.address) parts.push(`<span>📍 ${c.address}</span>`);
    if (c.whatsapp) parts.push(`<a href="https://wa.me/${c.whatsapp}" style="color:#25D366;text-decoration:none">WhatsApp</a>`);
    if (parts.length === 0) return;
    bar.innerHTML = parts.join(' &nbsp;·&nbsp; ');
    document.body.appendChild(bar);
  }

  loadConfig()
    .then((cfg) => {
      applyBrand(cfg);
      applyColors(cfg);
      applyContactBar(cfg);
    })
    .catch((err) => console.warn('LaafWeb config injection skipped:', err.message));
})();
