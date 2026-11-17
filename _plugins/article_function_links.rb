# Ends every article with the Finance Toolkit functions its code calls, each
# linking to its own documentation page (formula, parameters, MCP question).
#
# The functions come from the article's Python code blocks:
# `toolkit.ratios.get_return_on_equity(` names its module, so that one is
# exact; a bare `x.get_historical_data(` is linked only when the name exists
# in a single module. The pages are the ones _plugins/docs_metric_pages.rb
# generates, read once per build.

require "cgi"

module ArticleFunctionLinks
  # attribute on a Toolkit instance -> docs_module of the generated pages
  MODULES = {
    "ratios" => "Ratios", "models" => "Models", "options" => "Options",
    "technicals" => "Technicals", "fixedincome" => "Fixed Income", "risk" => "Risk",
    "performance" => "Performance", "econometrics" => "Econometrics",
    "economics" => "Economics", "etf" => "ETF", "portfolio" => "Portfolio Optimization",
    "discovery" => "Discovery",
  }.freeze

  CODE = /^```(?:python|py)\s*\n(.*?)^```/m
  QUALIFIED = /\.(#{MODULES.keys.join('|')})\.((?:get|collect)_\w+)\s*\(/
  BARE = /\.((?:get|collect)_\w+)\s*\(/

  @index = nil

  module_function

  def reset
    @index = nil
  end

  # [module, function] -> page, and function -> pages (to tell unique names)
  def index(site)
    @index ||= begin
      exact = {}
      by_name = Hash.new { |h, k| h[k] = [] }
      site.pages.each do |page|
        fn = page.data["docs_function"]
        next unless fn
        exact[[page.data["docs_module"], fn.downcase]] = page
        by_name[fn.downcase] << page
      end
      { :exact => exact, :by_name => by_name }
    end
  end

  def functions_in(markdown, site)
    idx = index(site)
    found = []
    markdown.scan(CODE).each do |(code)|
      code.scan(QUALIFIED) { |mod, fn| found << idx[:exact][[MODULES[mod], fn.downcase]] }
      code.scan(BARE) do |(fn)|
        pages = idx[:by_name][fn.downcase]
        found << pages.first if pages.size == 1
      end
    end
    found.compact.uniq.map { |page| { "url" => page.url, "title" => page.data["title"].to_s } }
  end

  def section(pages)
    pills = pages.map do |page|
      %(<a href="#{page['url']}" class="ft-module-pill">#{CGI.escapeHTML(page['title'])}</a>)
    end
    <<~HTML
      <section class="article-functions">
      <h2 id="functions-used-in-this-article">Functions Used in This Article</h2>
      <p>Each function has its own page with the formula, the parameters and an example:</p>
      <div class="ft-module-switcher docs-related">
        #{pills.join("\n  ")}
      </div>
      </section>
    HTML
  end
end

Jekyll::Hooks.register :site, :pre_render do |_site, _payload|
  ArticleFunctionLinks.reset
end

Jekyll::Hooks.register :pages, :pre_render do |page|
  next unless page.data["collection"] == "article"
  page.data["ft_functions"] = ArticleFunctionLinks.functions_in(page.content.to_s, page.site)
end

Jekyll::Hooks.register :pages, :post_convert do |page|
  pages = page.data["ft_functions"]
  next unless page.data["collection"] == "article" && pages && !pages.empty?
  page.content = page.content + "\n" + ArticleFunctionLinks.section(pages)
end
