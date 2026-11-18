# The "Data and method" note at the end of an article is folded away by default: the reader who
# wants the sources, the calculations and the limits opens it with one click. The article source
# keeps a plain `### Data and method` heading; this wraps it and everything after it (up to the
# charts script include) in a <details> block before the Markdown is converted.
module ArticleMethodNote
  NOTE = /^### Data and method[ \t]*\n(.*?)(?=^\{%-?\s*include ft-charts-script\.html|\z)/m

  Jekyll::Hooks.register :pages, :pre_render do |page|
    next unless page.data["collection"] == "article" && page.content.match?(NOTE)

    page.content = page.content.sub(NOTE) do
      body = Regexp.last_match(1).rstrip
      <<~HTML
        <details class="article-method" markdown="1">
        <summary class="article-method__summary"><span>Data and method</span><span class="article-method__hint">Sources, calculations and limits</span></summary>

        #{body}

        </details>

      HTML
    end
  end
end
