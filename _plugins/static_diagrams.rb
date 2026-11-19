# Mermaid diagrams drawn ahead of time. Each <div class="mermaid"> gets data-diagram, a
# hash of its source. When _includes/diagrams/<hash>-dark.svg and -light.svg exist
# (drawn by _scripts/render_diagrams.js from a local build), the build puts those two
# SVGs in place of the source, and _includes/mermaid.html doesn't load Mermaid (3.5 MB)
# on a page where every diagram is drawn. A diagram whose source changed has a new hash
# and no SVGs yet, so it is drawn in the browser as before until it is rendered again.
require "digest"

module StaticDiagrams
  BLOCK = %r{<div class="mermaid"([^>]*)>(.*?)</div>}m

  def self.apply(page)
    return unless page.output&.include?('class="mermaid"')

    dir = File.join(page.site.source, "_includes", "diagrams")
    page.output = page.output.gsub(BLOCK) do
      attrs, source = Regexp.last_match(1), Regexp.last_match(2)
      next Regexp.last_match(0) if attrs.include?("data-diagram")

      hash = Digest::SHA1.hexdigest(source.strip)[0, 12]
      dark = File.join(dir, "#{hash}-dark.svg")
      light = File.join(dir, "#{hash}-light.svg")
      if File.exist?(dark) && File.exist?(light)
        %(<div class="mermaid mermaid--static"#{attrs} data-diagram="#{hash}">) +
          %(<div class="mermaid__theme mermaid__theme--dark">#{File.read(dark)}</div>) +
          %(<div class="mermaid__theme mermaid__theme--light">#{File.read(light)}</div></div>)
      else
        %(<div class="mermaid"#{attrs} data-diagram="#{hash}">#{source}</div>)
      end
    end
  end
end

Jekyll::Hooks.register :pages, :post_render do |page|
  StaticDiagrams.apply(page)
end
