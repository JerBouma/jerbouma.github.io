# Reading time of an article, from the prose a reader reads: the Markdown without
# the Python behind each chart's button ({% capture %} blocks), code blocks, Liquid
# tags, HTML tags, link targets and the front matter. Set once per article as
# `reading_minutes` (at 220 words a minute), so the byline and the /insights cards
# show the same number.
module ReadingTime
  WORDS_PER_MINUTE = 220

  def self.minutes(markdown)
    text = markdown.dup
    text.gsub!(/\{%-?\s*capture\b.*?\{%-?\s*endcapture\s*-?%\}/m, " ")
    text.gsub!(/^(```|~~~).*?^\1/m, " ")
    text.gsub!(/\{%.*?%\}/m, " ")
    text.gsub!(/\{\{.*?\}\}/m, " ")
    text.gsub!(/\{:[^}]*\}/, " ")
    text.gsub!(/<[^>]+>/, " ")
    text.gsub!(/\]\([^)]*\)/, "]")
    text.gsub!(/\$\$.*?\$\$/m, " ")
    words = text.scan(/[[:alnum:]][[:alnum:]'’.,%-]*/).size
    [(words.to_f / WORDS_PER_MINUTE).round, 1].max
  end
end

Jekyll::Hooks.register :pages, :post_init do |page|
  next unless page.data["collection"] == "article"
  page.data["reading_minutes"] = ReadingTime.minutes(page.content.to_s)
end
