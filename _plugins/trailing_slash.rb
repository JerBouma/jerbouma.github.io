# The site's permalinks have no trailing slash (/projects/financetoolkit is
# served from projects/financetoolkit.html), so the same address typed or
# linked with a slash was a plain 404 on GitHub Pages. This registers the
# slashed variant of every such page as a `redirect_from` entry, and
# jekyll-redirect-from then writes a small canonical-tagged redirect page at
# /projects/financetoolkit/index.html that sends visitors and crawlers to the
# real URL. Runs before the generators so the redirect plugin picks it up.
Jekyll::Hooks.register :site, :post_read do |site|
  urls = site.pages.map(&:url)
  site.pages.each do |page|
    url = page.url
    next if url == "/" || url.end_with?("/") || !File.extname(url).empty?
    next if page.data["redirect_to"] || urls.include?("#{url}/")
    from = Array(page.data["redirect_from"]).compact
    next if from.include?("#{url}/")
    page.data["redirect_from"] = from + ["#{url}/"]
  end
end
