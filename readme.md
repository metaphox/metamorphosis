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

Deploy the contents of `_site/` to a static web host. No Ruby server is needed
in production.

After building, run `python3 test/site_test.py` to check the archive, URLs,
assets, and RSS feed.

Everything is under the CC BY-SA licence. Feel free to take anything.
