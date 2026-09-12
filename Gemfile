source "https://rubygems.org"

gem "minimal-mistakes-jekyll"
gem "kramdown-parser-gfm"
gem 'jekyll', '~> 4.3'
# image dimensions for the width/height attributes added by _plugins/image_attributes.rb
gem "fastimage"
# not default gems any more from Ruby 4.0 on, but still required by jekyll/mercenary (logger)
# and jekyll-algolia (ostruct)
gem "logger"
gem "ostruct"

group :jekyll_plugins do
  gem "jekyll-include-cache", group: :jekyll_plugins
  gem "jekyll-redirect-from", group: :jekyll_plugins
  gem "jekyll-seo-tag", group: :jekyll_plugins
  gem 'jekyll-algolia', '~> 1.0'
end