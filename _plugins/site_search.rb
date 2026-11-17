require "json"

# The index behind the search box in the masthead (_includes/site-search.html):
# /assets/data/search.json lists every public page with its title, section,
# description and, for a Finance Toolkit function page, the Python method name.
# The browser downloads it the first time someone opens the search and does
# the matching itself, so there's no search service to run or pay for.
module SiteSearch
  PATH = "assets/data".freeze
  SKIP = %r{\A/(404\.html|q7v3|resume/cv|projects/financescenarios)}.freeze

  class Index < Jekyll::PageWithoutAFile; end

  module_function

  def plain(text, limit)
    text = text.to_s.gsub(/<[^>]+>/, "").gsub(/\[([^\]]*)\]\([^)]*\)/, '\1')
               .gsub(/[*`]/, "").gsub(/\s+/, " ").strip
    return text if text.length <= limit
    text[0, limit].sub(/\s+\S*\z/, "") + "…"
  end

  # where the page sits, shown above its title: "Finance Toolkit · Fixed Income"
  # for a function page (its module's own name), else from the URL
  def section(page, site)
    if page.data["docs_module"] && page.data["docs_function"]
      name = page.data["docs_module"] == "Toolkit" ? "Data" : page.data["docs_module"]
      return "Finance Toolkit · #{name}"
    end
    ShareImages.section_for(page.url, site)
  end

  def listed?(page)
    page.output_ext == ".html" && page.data["title"] && !page.data["redirect"] &&
      page.data["layout"] != "redirect" && !page.data["noindex"] &&
      page.data["sitemap"] != false && page.url !~ SKIP
  end

  class Generator < Jekyll::Generator
    safe true
    # after the docs pages are generated, like the share images
    priority :low

    def generate(site)
      entries = site.pages.select { |page| SiteSearch.listed?(page) }.map do |page|
        entry = {
          "t" => SiteSearch.plain(page.data["title"], 120),
          "u" => page.url.sub(/\.html\z/, ""),
          "s" => SiteSearch.section(page, site),
          "d" => SiteSearch.plain(page.data["description"] || page.data["excerpt"], 160),
        }
        entry["f"] = page.data["docs_function"] if page.data["docs_function"]
        entry
      end
      entries.sort_by! { |e| [e["u"].count("/"), e["u"]] }
      index = Index.new(site, site.source, PATH, "search.json")
      index.content = JSON.generate(entries)
      index.data["layout"] = nil
      index.data["sitemap"] = false
      site.pages << index
    end
  end
end
