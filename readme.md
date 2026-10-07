Metamorphosis
=============

Personal blog built with Jekyll 4.4. Posts live in `_posts/`, templates in
`_layouts/`, and Sass in `css/screen.scss`. `_hidden/` contains unpublished
archive material; `resource/` and `_resource/` contain design source files.

Use Ruby 3.2 or newer (Ruby 3.4 recommended):

On macOS with Homebrew, select the installed Ruby before running Bundler:

```sh
brew install ruby@3.4
export PATH="$(brew --prefix ruby@3.4)/bin:$PATH"
```

```sh
bundle install
bundle exec jekyll serve
```

Preview at <http://localhost:4000>. To generate static files for hosting:

```sh
bundle exec jekyll build
```

### Cloudflare Workers

`wrangler.jsonc` builds Jekyll in production mode and publishes `_site/` as
Workers Static Assets for the Worker named `blog` at
<https://blog.metaphox.com>. No Ruby server or Worker script is needed.

For the connected repository in Cloudflare Workers Builds, use:

- Root directory: repository root
- Build command: leave empty (Wrangler runs the build)
- Deploy command: `npx wrangler deploy`

Cloudflare installs the locked npm and Ruby dependencies automatically.
`.ruby-version` selects Ruby 3.4.7, matching the existing build environment.
`Gemfile.lock` includes Linux variants for Cloudflare and macOS variants for
local development; `package-lock.json` pins Wrangler and its dependencies.
The explicit build command is `bundle exec jekyll build`, with
`JEKYLL_ENV=production`; do not prefix Ruby's `bundle` command with `npx`.

To validate and deploy locally (Node.js 22 or newer and Ruby 3.2 or newer):

```sh
bundle install
npm ci
npx wrangler deploy --dry-run
python3 test/site_test.py
npx wrangler login
npm run deploy
```

The `metaphox.com` zone must be active in the deploying Cloudflare account.
The [custom domain](https://developers.cloudflare.com/workers/configuration/routing/custom-domains/)
manages DNS and TLS configuration. The existing blog hostname already has a
Cloudflare-managed DNS record, so no manual DNS change is needed.
Keep the existing Disqus URLs and RSS GUIDs to preserve comment threads and
feed item identities.

After building, run `python3 test/site_test.py` to check the archive, URLs,
assets, and RSS feed.

Everything is under the CC BY-SA licence. Feel free to take anything.
