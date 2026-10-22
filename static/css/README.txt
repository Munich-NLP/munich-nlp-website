Compatibility stylesheets for HTML cached before the switch to stable asset URLs.
Cloudflare currently caches HTML for four hours. Keep these exact original bytes
so older pages with Subresource Integrity continue working during that window.
New pages use /css/site.min.css?v=<content hash>, which survives future deploys.
