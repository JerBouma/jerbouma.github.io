require "json"

# A share image (og:image) per page, showing that page's title, so a link
# shared on LinkedIn, X or elsewhere shows what it points to instead of one
# generic banner.
#
# This plugin decides the text: the section the page sits in (from the URL
# and _data/breadcrumbs.yml), the title and the description. It points the
# page's og:image at /assets/images/share/<key>.jpg and lists everything in
# /assets/images/share/manifest.json. The deploy workflow then renders the
# images with _scripts/build-share-images.js and _scripts/share-banner.html,
# the same design as assets/images/default/share-banner.jpg (the fallback).
#
# The Finance Toolkit function pages share their module's image (one image
# for Ratios instead of one per ratio); the homepage keeps its headline.
module ShareImages
  DIR = "assets/images/share".freeze
  DOCS = "/projects/financetoolkit/docs/".freeze
  SKIP = %w[/404.html /q7v3 /resume/cv].freeze

  class Manifest < Jekyll::PageWithoutAFile; end

  module_function

  def key_for(url)
    url == "/" ? "home" : Jekyll::Utils.slugify(url.sub(/\.html\z/, ""), :mode => "default")
  end

  def plain(text, limit)
    text = text.to_s.gsub(/<[^>]+>/, "").gsub(/\[([^\]]*)\]\([^)]*\)/, '\1').gsub(/[*_`]/, "").gsub(/\s+/, " ").strip
    return text if text.length <= limit
    text[0, limit].sub(/\s+\S*\z/, "") + "…"
  end

  def section_for(url, site)
    names = site.data["breadcrumbs"] || {}
    parts = url.sub(/\.html\z/, "").split("/").reject(&:empty?)[0..-2]
    parts.last(2).map { |p| names[p] || p.tr("-", " ").capitalize }.join(" · ")
  end

  def shareable?(page)
    page.output_ext == ".html" && !page.data["redirect"] && page.data["layout"] != "redirect" &&
      !SKIP.include?(page.url.sub(/\.html\z/, "")) && page.data["title"]
  end

  class Generator < Jekyll::Generator
    safe true
    # after the docs pages and the article list, before the sitemap
    priority :low

    def generate(site)
      images = {}
      site.pages.each do |page|
        next unless ShareImages.shareable?(page)
        url = page.url
        # a Finance Toolkit function page uses its module's image
        if url.start_with?(ShareImages::DOCS) && page.data["docs_module_url"]
          target = page.data["docs_module_url"]
          title = "#{page.data['docs_module']} module"
          section = "Finance Toolkit · Documentation"
          description = ""
        else
          target = url
          title = page.data["title"]
          section = ShareImages.section_for(url, site)
          description = page.data["description"] || page.data["excerpt"]
        end
        key = ShareImages.key_for(target)
        images[key] ||= {
          "key" => key,
          "home" => url == "/",
          "section" => section,
          "title" => ShareImages.plain(title, 110),
          "description" => ShareImages.plain(description, 150),
          "path" => target == "/" ? "" : target.sub(/\.html\z/, ""),
        }
        page.data["header"] = (page.data["header"] || {}).merge("og_image" => "/#{ShareImages::DIR}/#{key}.jpg")
      end
      manifest = Manifest.new(site, site.source, ShareImages::DIR, "manifest.json")
      manifest.content = JSON.pretty_generate(images.values)
      manifest.data["layout"] = nil
      manifest.data["sitemap"] = false
      site.pages << manifest
    end
  end
end
