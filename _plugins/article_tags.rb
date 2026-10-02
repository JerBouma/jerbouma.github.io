# Keeps the article tags (the filter buttons on /insights) from growing a new
# tag per article. Every tag used by a page with `collection: article` must be
# listed in _data/article_tags.yml, otherwise the build stops with the page and
# the offending tag, so the check also fails on pull requests.
Jekyll::Hooks.register :site, :post_read do |site|
  allowed = Array(site.data["article_tags"])
  next if allowed.empty?

  unknown = site.pages.select { |page| page.data["collection"] == "article" }.flat_map do |page|
    (Array(page.data["tags"]) - allowed).map { |tag| "#{page.relative_path}: \"#{tag}\"" }
  end
  next if unknown.empty?

  raise Jekyll::Errors::FatalException,
        "Article tags not in _data/article_tags.yml (use one of #{allowed.join(', ')} or add it there):\n  " +
        unknown.join("\n  ")
end
