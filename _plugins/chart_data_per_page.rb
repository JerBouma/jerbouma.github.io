# Every article used to download all of assets/data/article-charts.json (345 KB, every
# article's charts) to draw its own handful. This gives each page that draws charts
# from that file a small file with only its own charts, assets/data/charts/<page>.json,
# and points the page's charts at it. article-charts.json stays the one file that is
# edited and committed; the per-page files exist only in the build.
require "json"

module ChartDataPerPage
  SOURCE = "/assets/data/article-charts.json"
  ATTR = %r{data-chart="([^"]+)" data-src="#{Regexp.escape(SOURCE)}\?v=(\d+)"}

  def self.charts(site)
    @charts = nil if @charts_for != site.time
    @charts_for = site.time
    @charts ||= JSON.parse(File.read(File.join(site.source, SOURCE)))["charts"]
  end

  def self.split(page)
    return unless page.output&.include?(SOURCE)

    ids = page.output.scan(ATTR).map(&:first).uniq
    return if ids.empty?

    all = charts(page.site)
    return unless ids.all? { |id| all.key?(id) } # a missing chart keeps the full file and its error path

    name = page.url.sub(%r{\A/}, "").sub(/\.html\z/, "").sub(%r{/\z}, "").gsub(/[^a-z0-9]+/i, "-")
    name = "index" if name.empty?
    path = "/assets/data/charts/#{name}.json"
    (page.site.config["chart_data_files"] ||= {})[path] = JSON.generate("charts" => ids.to_h { |id| [id, all[id]] })
    page.output = page.output.gsub(ATTR) { %(data-chart="#{Regexp.last_match(1)}" data-src="#{path}?v=#{Regexp.last_match(2)}") }
  end
end

Jekyll::Hooks.register :pages, :post_render do |page|
  ChartDataPerPage.split(page)
end

Jekyll::Hooks.register :site, :post_write do |site|
  files = site.config.delete("chart_data_files") || {}
  files.each do |path, json|
    dest = File.join(site.dest, path)
    FileUtils.mkdir_p(File.dirname(dest))
    File.write(dest, json)
  end
end
