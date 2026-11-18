# Adds each article's cover image to its <url> entry in the sitemap that jekyll-sitemap
# renders (Google's image sitemap extension), so search engines find the covers with
# their article. The rest of the sitemap stays as the plugin makes it.
require "cgi"

Jekyll::Hooks.register :pages, :post_render do |page|
  next unless page.url == "/sitemap.xml"

  site = page.site
  covers = {}
  site.pages.each do |p|
    next unless p.data["collection"] == "article" && p.data["cover"].is_a?(Hash) && p.data["cover"]["image"]
    loc = site.config["url"].to_s + site.baseurl.to_s + p.url
    covers[loc] = site.config["url"].to_s + site.baseurl.to_s + p.data["cover"]["image"]
  end
  next if covers.empty?

  out = page.output.sub('xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
                        'xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"')
  covers.each do |loc, image|
    escaped = CGI.escapeHTML(loc)
    out = out.sub(%r{(<loc>#{Regexp.escape(escaped)}</loc>.*?)(</url>)}m) do
      "#{Regexp.last_match(1)}  <image:image><image:loc>#{CGI.escapeHTML(image)}</image:loc></image:image>\n    #{Regexp.last_match(2)}"
    end
  end
  page.output = out
end
