require "digest"

# Sharing drafts per article, shown on the unlisted page in _pages/q7v3.html.
#
# Every article gets a short id (the first six characters of the SHA-1 of its
# permalink). The LinkedIn and Reddit drafts are written by hand in
# _data/q7v3/<id>.yml; this lists the articles with their drafts.
module Q7v3
  module_function

  def id_for(permalink)
    Digest::SHA1.hexdigest(permalink.to_s)[0, 6]
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
        {
          "id" => id,
          "title" => page.data["title"],
          "date" => page.data["date"],
          "url" => "#{url}#{page.url}",
          "drafts" => drafts[id],
        }
      end
    end
  end
end
