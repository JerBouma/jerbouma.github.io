# Every article with chart code gets one runnable script with all of it, at /articles/<slug>.py:
# the Python behind each chart's Python button, in the order of the charts, with the imports
# gathered at the top. The Data and method note links to it (article_method_note.rb). The script
# is built from the article itself, so it never drifts from the buttons.
module ArticleScript
  CAPTURE = /\{%-?\s*capture\s+(code_\w+)\s*-?%\}(.*?)\{%-?\s*endcapture\s*-?%\}/m
  INCLUDE = /\{%-?\s*include\s+ft-chart\.html\s+([^%]*?)-?%\}/m
  FENCE = /```python[ \t]*\n(.*?)```/m

  # the script for an article's Markdown source, or nil when it has no chart code
  def self.script_for(content, title, url)
    blocks = content.scan(CAPTURE).to_h { |name, body| [name, body[FENCE, 1].to_s] }
    return nil if blocks.values.all?(&:empty?)

    charts = content.scan(INCLUDE).filter_map do |(args)|
      name = args[/code=(code_\w+)/, 1]
      next unless name && !blocks[name].to_s.empty?

      [args[/label="([^"]*)"/, 1] || args[/id="([^"]*)"/, 1], blocks[name]]
    end
    return nil if charts.empty?

    imports = []
    current = {} # the same Toolkit or Economics set up again isn't repeated
    sections = charts.map do |label, code|
      body = code.lines.reject do |line|
        # only one-line constructor calls (toolkit = Toolkit(...)), which hold no state yet
        name = line[/\A(\w+) = [A-Z]\w*\(.*\)\s*\z/, 1]
        if line.match?(/\A(?:import |from \S+ import )/)
          imports << line.rstrip
          true
        elsif line.strip == "# pip install financetoolkit"
          true
        elsif name && current[name] == line.rstrip
          true
        else
          current[name] = line.rstrip if name
          false
        end
      end
      "# --- #{label} ---\n#{body.join.strip}\n"
    end

    <<~PY
      # #{title}
      # https://www.jeroenbouma.com#{url}
      #
      # The code behind every chart in the article, in the order of the charts.
      # Run it from top to bottom. Replace FINANCIAL_MODELING_PREP_KEY with your own key.
      #
      # pip install financetoolkit
      #{imports.uniq.join("\n")}


      #{sections.join("\n\n")}
    PY
  end

  def self.path_for(page)
    "#{page.url.sub(%r{/\z}, '').sub(/\.html\z/, '')}.py"
  end

  class Generator < Jekyll::Generator
    safe true
    priority :low

    def generate(site)
      site.pages.select { |p| p.data["collection"] == "article" }.each do |page|
        script = ArticleScript.script_for(page.content, page.data["title"], page.url.sub(/\.html\z/, ""))
        next unless script

        path = ArticleScript.path_for(page)
        file = Jekyll::PageWithoutAFile.new(site, site.source, File.dirname(path), File.basename(path))
        file.content = script
        file.data["layout"] = nil
        file.data["sitemap"] = false
        file.data["render_with_liquid"] = false
        page.data["script_url"] = path
        site.pages << file
      end
    end
  end
end
