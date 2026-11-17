require "json"
require "cgi"
require "fileutils"

# The index behind the search box in the masthead (_includes/site-search.html):
# /assets/data/search.json lists every public page with its title, section,
# description and, for a Finance Toolkit function page, the Python method name.
# The browser downloads it the first time someone opens the search and does
# the matching itself, so there's no search service to run or pay for.
#
# A second file, /assets/data/search-content.json, holds the text of every page
# cut at its h2 and h3 headings, so the search also finds words in the body and
# links straight to the heading they sit under. Code blocks, tables, maths and
# sentences that repeat on many pages (install lines, parameter lead-ins) are
# left out.
module SiteSearch
  PATH = "assets/data".freeze
  SKIP = %r{\A/(404\.html|q7v3|resume/cv|projects/financescenarios)}.freeze

  CONTENT = "search-content.json".freeze
  CHUNK_CHARS = 500
  REPEATED = 15 # a sentence on more pages than this is boilerplate

  class Index < Jekyll::PageWithoutAFile; end

  @chunks = {}

  class << self
    attr_accessor :chunks
  end

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

  # a parameters table as "period: The period to use… rolling: The rolling…"
  def params(table)
    table.scan(/<tr>\s*<td>(.*?)<\/td>\s*<td>.*?<\/td>\s*<td>(.*?)<\/td>/m).map do |name, desc|
      desc = CGI.unescapeHTML(desc.gsub(/<[^>]+>/, "")).strip
      "#{name.gsub(/<[^>]+>/, '')}: #{desc[/\A.*?[.!?](?=\s|\z)/m] || desc}"
    end.join(" ")
  end

  def text(html)
    t = html.gsub(/<div class="docs-params__table">(.*?)<\/table>/m) { " #{params(Regexp.last_match(1))} " }
    t = t.gsub(/<(script|style|svg|pre|table|figure)\b.*?<\/\1>/m, " ")
            .gsub(/<(p|div|li)\b[^>]*class="[^"]*docs-(boilerplate|mcp-note)[^"]*"[^>]*>.*?<\/\1>/m, " ")
            .gsub(/<[^>]+>/, " ")
    t = CGI.unescapeHTML(t)
    t.gsub(/\$\$.*?\$\$|\\\[.*?\\\]|\\\(.*?\\\)/m, " ").gsub(/\s+/, " ").strip
  end

  # [[anchor, heading, text], ...] for a page's converted HTML, the intro first
  def split(html)
    parts = html.split(/(<h[23]\b[^>]*>.*?<\/h[23]>)/m)
    out = [["", "", text(parts.shift.to_s)]]
    parts.each_slice(2) do |head, body|
      id = head[/\bid="([^"]+)"/, 1]
      out << [id.to_s, text(head), text(body.to_s)]
    end
    out
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

Jekyll::Hooks.register :site, :pre_render do |_site, _payload|
  SiteSearch.chunks = {}
end

Jekyll::Hooks.register :pages, :post_convert do |page|
  next unless SiteSearch.listed?(page)
  SiteSearch.chunks[page.url.sub(/\.html\z/, "")] = SiteSearch.split(page.content.to_s)
end

Jekyll::Hooks.register :site, :post_write do |site|
  sentence = ->(t) { t.split(/(?<=[.:!?])\s+/) }
  seen = Hash.new(0)
  SiteSearch.chunks.each_value do |chunks|
    chunks.flat_map { |c| sentence.(c[2]) }.uniq.each { |s| seen[s] += 1 }
  end
  rows = []
  SiteSearch.chunks.each do |url, chunks|
    chunks.each do |anchor, heading, text|
      # parameter descriptions repeat across functions but still belong to each
      body = anchor == "parameters" ? text : sentence.(text).reject { |s| seen[s] > SiteSearch::REPEATED }.join(" ")
      next if body.length < 40 && heading.empty?
      next if heading.start_with?("Related ") # the sidebar's list of sibling pages
      limit = anchor == "parameters" ? 3 * SiteSearch::CHUNK_CHARS : SiteSearch::CHUNK_CHARS
      body = body[0, limit].sub(/\s+\S*\z/, "") + "…" if body.length > limit
      rows << [url, anchor, heading, body]
    end
  end
  path = File.join(site.dest, SiteSearch::PATH, SiteSearch::CONTENT)
  FileUtils.mkdir_p(File.dirname(path))
  File.write(path, JSON.generate(rows))
end
