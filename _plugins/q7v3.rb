require "digest"
require "kramdown"

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


  # inline HTML to Markdown, for the text inside a component
  def inline_md(html)
    html.to_s
        .gsub(%r{<i\b[^>]*>\s*</i>}, "")
        .gsub(%r{<(strong|b)>(.*?)</\1>}m) { "**#{Regexp.last_match(2).strip}**" }
        .gsub(%r{<em>(.*?)</em>}m) { "*#{Regexp.last_match(1).strip}*" }
        .gsub(%r{<code>(.*?)</code>}m) { "`#{Regexp.last_match(1)}`" }
        .gsub(%r{<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>}m) { "[#{Regexp.last_match(2).gsub(/<[^>]+>/, '').strip}](#{Regexp.last_match(1)})" }
        .gsub(/<[^>]+>/, "")
        .gsub(/[ \t]+/, " ")
        .strip
  end

  # The article components (see _sass/_article-components.scss) as plain
  # Markdown that survives pasting into Medium: lists, bold, quotes and links.
  def components_to_md(text)
    text = text.gsub(%r{<div class="ca-nav[^"]*">.*?</div>}m, "")
    text = text.gsub(%r{<div class="ca-strip">(.*?)\n</div>}m) do
      Regexp.last_match(1).scan(%r{<strong>(.*?)</strong>\s*<span>(.*?)</span>}m)
                          .map { |a, b| "- **#{inline_md(a)}** · #{inline_md(b)}" }.join("\n") + "\n"
    end
    text = text.gsub(%r{<div class="article-cta">(.*?)\n</div>}m) do
      inner = Regexp.last_match(1)
      title = inner[%r{<p class="article-cta__title">(.*?)</p>}m, 1]
      body = inner.scan(%r{<p>(.*?)</p>}m).flatten.map { |b| inline_md(b) }
      links = inner[%r{<p class="article-cta__actions">(.*?)</p>}m, 1].to_s
                   .scan(%r{<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>}m)
                   .map { |u, t| "[#{inline_md(t)}](#{u})" }
      ["**#{inline_md(title)}**", *body, links.join(" · ")].reject(&:empty?).join("\n\n") + "\n"
    end
    text = text.gsub(%r{<div class="ca-cards[^"]*">(.*?)\n</div>}m) do
      Regexp.last_match(1).scan(%r{<p class="ca-card-title">(.*?)</p>\s*<p>(.*?)</p>}m)
                          .map { |t, b| "- **#{inline_md(t)}**: #{inline_md(b)}" }.join("\n") + "\n"
    end
    text = text.gsub(%r{<div class="ca-clients">(.*?)\n</div>}m) do
      Regexp.last_match(1).scan(%r{<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>}m)
                          .map { |u, t| "- [#{inline_md(t)}](#{u})" }.join("\n") + "\n"
    end
    text = text.gsub(%r{<div class="ca-q">[^\n]*?<p>([^\n]*?)<span class="ca-q__tool">([^\n]*?)</span></p></div>}) do
      "> **Question:** #{inline_md(Regexp.last_match(1))}\n>\n> *#{inline_md(Regexp.last_match(2))}*\n"
    end
    text = text.gsub(%r{<div class="ca-q">[^\n]*?<p>([^\n]*?)</p></div>}) { "> **Question:** #{inline_md(Regexp.last_match(1))}\n" }
    # the showcase blocks: counts, the steps behind the answer, the charts and the conclusion
    text = text.gsub(%r{<div class="mcp-show__meta">(.*?)</div>}m) do
      "*" + Regexp.last_match(1).scan(%r{<span><b>(.*?)</b>(.*?)</span>}m).map { |a, b| "#{inline_md(a)} #{inline_md(b)}" }.join(" · ") + "*\n"
    end
    text = text.gsub(%r{<details class="mcp-show__trace"><summary>(.*?)</summary><ol>(.*?)</ol></details>}m) do
      title = inline_md(Regexp.last_match(1))
      steps = Regexp.last_match(2).scan(%r{<li><code>(.*?)</code><span>(.*?)</span></li>}m)
                                  .each_with_index.map { |(c, d), i| "#{i + 1}. `#{c}`: #{inline_md(d)}" }
      "**#{title}:**\n\n#{steps.join("\n")}\n"
    end
    text = text.gsub(%r{<div class="mcp-show__cell[^"]*">(.*?)</div>}m) { "\n#{Regexp.last_match(1).strip}\n" }
    text = text.gsub(%r{<div class="mcp-show__verdict"><p class="mcp-show__label">(.*?)</p><p>(.*?)</p></div>}m) do
      "**#{inline_md(Regexp.last_match(1))}:** #{inline_md(Regexp.last_match(2))}\n"
    end
    text = text.gsub(%r{<div class="ca-nums">(.*?)</div>}m) do
      Regexp.last_match(1).scan(%r{<span><b>(.*?)</b>(.*?)</span>}m)
                          .map { |a, b| "- **#{inline_md(a)}** #{inline_md(b)}" }.join("\n") + "\n"
    end
    text.gsub(%r{<div class="ca-take"><p>(.*?)</p></div>}m) { "**Takeaway:** #{inline_md(Regexp.last_match(1))}\n" }
  end

  # Medium has no code blocks inside list items: a numbered list that holds one
  # becomes numbered paragraphs, with the code as its own block in between.
  def steps_with_code(text)
    lines = text.split("\n", -1)
    out = []
    i = 0
    while i < lines.length
      if lines[i] =~ /\A\d+\.\s/
        j = i
        j += 1 while j < lines.length && (lines[j] =~ /\A\d+\.\s/ || lines[j] =~ /\A\s+\S/ || (lines[j].strip.empty? && lines[j + 1].to_s =~ /\A(\d+\.\s|\s+\S)/))
        block = lines[i...j]
        if block.any? { |l| l =~ /\A\s+```/ }
          block.each do |l|
            if l =~ /\A(\d+)\.\s+(.*)\z/
              out << "" << "**#{Regexp.last_match(1)}.** #{Regexp.last_match(2)}"
            elsif l =~ /\A\s+```/
              out << "" if out.last.to_s.strip != "" && !out.last.to_s.start_with?("```") && l.strip.length > 3
              out << l.strip
            else
              out << l.sub(/\A\s{1,4}/, "")
            end
          end
          out << ""
        else
          out.concat(block)
        end
        i = j
      else
        out << lines[i]
        i += 1
      end
    end
    out.join("\n")
  end

  # The HTML that is copied into Medium: plain code blocks without syntax
  # highlighting, whose markup Medium drops.
  def medium_html(markdown)
    Kramdown::Document.new(markdown, input: "GFM", hard_wrap: false, syntax_highlighter: nil).to_html
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
    text = components_to_md(text)
    text = steps_with_code(text)
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
          "medium_html" => Q7v3.medium_html(body),
          "medium_notes" => notes,
          "drafts" => drafts[id],
        }
      end
    end
  end
end
