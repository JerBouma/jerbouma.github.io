require "digest"

# Content drafts per article, shown on the unlisted page in _pages/q7v3.md.
#
# Every article gets a short id (the first six characters of the SHA-1 of its
# permalink). LinkedIn and Reddit drafts are written by hand in
# _data/q7v3/<id>.yml. The Medium version is the article itself, converted here
# on every build so it never drifts from the original:
#
# - the interactive charts become the static images in assets/images/q7v3/
#   (<chart id>.png, made with the interactive-charts skill), or a link back to
#   the article when there is no image yet;
# - tables become code blocks, since Medium has no tables;
# - relative links and images become absolute, and kramdown attributes,
#   scripts, layout divs and Liquid tags are removed;
# - a closing line points to the original, which is also the canonical URL.
module Q7v3
  module_function

  def id_for(permalink)
    Digest::SHA1.hexdigest(permalink.to_s)[0, 6]
  end

  def absolute(text, url)
    text.gsub(/\]\(\//, "](#{url}/").gsub(/(src|href)="\//, "\\1=\"#{url}/")
  end

  # consecutive table lines go into one code block, without inline HTML
  def tables_to_code(text)
    out = []
    table = []
    flush = lambda do
      unless table.empty?
        out << "```" << table.map { |l| l.gsub(/<[^>]+>/, "") } << "```"
        table.clear
      end
    end
    text.each_line(chomp: true) do |line|
      if line.lstrip.start_with?("|") then table << line.strip
      else
        flush.call
        out << line
      end
    end
    flush.call
    out.flatten.join("\n")
  end

  def medium(page, site, url)
    text = page.content.dup
    notes = []
    notes << "Formulas (MathJax) don't render on Medium; turn them into images or plain text." if text.include?("$$") || text.include?("\\(")
    notes << "The Mermaid diagram doesn't render on Medium; replace it with a screenshot." if text.include?("mermaid")
    missing = []
    text.gsub!(/\{%\s*include ft-chart\.html\s+id="([^"]+)"[^%]*?label="([^"]*)"[^%]*%\}/) do
      id, label = Regexp.last_match(1), Regexp.last_match(2)
      if File.exist?(File.join(site.source, "assets/images/q7v3/#{id}.png"))
        "![#{label}](#{url}/assets/images/q7v3/#{id}.png)"
      else
        missing << id
        "*#{label}: see the interactive chart in the [original article](#{url}#{page.url}).*"
      end
    end
    notes << "No image yet for #{missing.size} chart(s): #{missing.join(', ')}." unless missing.empty?
    text.gsub!(%r{<script\b.*?</script>}m, "")
    text.gsub!(/\{%-?\s*(raw|endraw|include [^%]*)\s*-?%\}/, "")
    text.gsub!(/\{:[^}]*\}/, "")
    text.gsub!(%r{^\s*</?div\b[^>]*>\s*$}, "")
    text = tables_to_code(absolute(text, url))
    text = text.gsub(/\n{3,}/, "\n\n").strip
    [text + "\n\n---\n\n*Originally published on [jeroenbouma.com](#{url}#{page.url}), where the charts are interactive.*\n", notes]
  end

  class Generator < Jekyll::Generator
    safe true
    priority :low

    def generate(site)
      url = site.config["url"].to_s.sub(%r{/\z}, "")
      drafts = site.data["q7v3"] || {}
      articles = site.pages.select { |p| p.data["collection"] == "article" }
                     .sort_by { |p| p.data["date"].to_s }.reverse
      site.data["q7v3_articles"] = articles.map do |page|
        id = Q7v3.id_for(page.url.sub(/\.html\z/, ""))
        body, notes = Q7v3.medium(page, site, url)
        {
          "id" => id,
          "title" => page.data["title"],
          "date" => page.data["date"],
          "url" => "#{url}#{page.url}",
          "excerpt" => page.data["excerpt"],
          "tags" => page.data["tags"],
          "medium" => body,
          "medium_notes" => notes,
          "drafts" => drafts[id],
        }
      end
    end
  end
end
