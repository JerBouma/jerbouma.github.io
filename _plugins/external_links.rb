# Post-render pass that makes every link opening in a new tab carry
# rel="noopener". Without it the opened page gets a `window.opener` handle back
# to this site (a tabnabbing vector) and Lighthouse/Bing flag every such link.
# Links that already declare a rel attribute keep it and just get "noopener"
# appended when missing; everything else in the tag is left untouched.
module ExternalLinks
  A_TAG = /<a\b[^>]*\btarget\s*=\s*["']?_blank["']?[^>]*>/i
  REL   = /\brel\s*=\s*(["'])(.*?)\1/i

  def self.process(doc)
    return unless doc.output_ext == ".html" && doc.output
    doc.output = doc.output.gsub(A_TAG) do |tag|
      if (match = tag.match(REL))
        tokens = match[2].split
        next tag if tokens.map(&:downcase).include?("noopener")
        tag.sub(match[0], %(rel="#{(tokens + ["noopener"]).join(" ")}"))
      else
        tag.sub(/\s*\/?>\z/) { |close| %( rel="noopener"#{close}) }
      end
    end
  end
end

Jekyll::Hooks.register [:pages, :documents], :post_render do |doc|
  ExternalLinks.process(doc)
end
