# Post-render pass over every HTML page that gives <img> tags the attributes a
# static site cannot easily add by hand in Markdown:
#
#   * width/height  – intrinsic size of local images (read with fastimage) so
#                     the browser reserves the space before the file arrives
#                     and nothing jumps around while the page loads. The theme
#                     styles images with `max-width: 100%; height: auto`, so
#                     the attributes only fix the aspect ratio, not the size.
#   * loading=lazy  – offscreen images are fetched only when scrolled near.
#   * decoding=async
#
# Tags that already carry `loading` or `fetchpriority` keep that choice, so
# above-the-fold images (author avatar, home hero) opt out of lazy loading with
# loading="eager" / fetchpriority="high"; they still get their dimensions.
require "fastimage"

module ImageAttributes
  IMG_TAG = /<img\b[^>]*>/i
  DIMENSIONS = {}

  def self.dimensions(site, src)
    return nil if src.nil? || src.empty?
    return nil if src =~ %r{\A(https?:)?//} || src.start_with?("data:")
    path = src.split("?").first.split("#").first
    path = path.sub(/\A#{Regexp.escape(site.baseurl.to_s)}/, "") unless site.baseurl.to_s.empty?
    return nil unless path.start_with?("/")
    DIMENSIONS[path] ||= begin
      file = File.join(site.source, path)
      File.file?(file) ? (FastImage.size(file) || :none) : :none
    end
    DIMENSIONS[path] == :none ? nil : DIMENSIONS[path]
  end

  def self.process(doc)
    return unless doc.output_ext == ".html" && doc.output
    site = doc.site
    doc.output = doc.output.gsub(IMG_TAG) do |tag|
      attrs = ""
      unless tag =~ /\b(width|height)\s*=/i
        src = tag[/\bsrc\s*=\s*["']([^"']+)["']/i, 1]
        if (dims = dimensions(site, src))
          attrs << %( width="#{dims[0]}" height="#{dims[1]}")
        end
      end
      attrs << ' loading="lazy"' unless tag =~ /\b(loading|fetchpriority)\s*=/i
      attrs << ' decoding="async"' unless tag =~ /\bdecoding\s*=/i
      next tag if attrs.empty?
      tag.sub(/\s*\/?>\z/) { |close| "#{attrs}#{close}" }
    end
  end
end

Jekyll::Hooks.register [:pages, :documents], :post_render do |doc|
  ImageAttributes.process(doc)
end
