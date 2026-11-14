# Release notes of the Finance Toolkit, read from its GitHub releases at build
# time, so a new release shows up on /projects/financetoolkit/releases without
# a commit. The deploy workflow rebuilds the site every morning.
#
# The copy in _data/releases/<project>.json is the fallback when GitHub cannot
# be reached (offline builds, rate limits, LIVE_STATS=off), so a build never
# fails because of this. RELEASES_SNAPSHOT=1 writes the fetched notes back to
# that file.
#
# Each release becomes { tag, name, date, url, html }. The html is GitHub's
# own rendering of the release text (so #123 and @user links and the older
# notes' collapsible sections look as they do on GitHub), with GitHub's
# hovercard attributes removed, links opening in a new tab and the headings
# one level down with ids that are unique per release.

require "json"
require "net/http"
require "uri"

module ReleaseNotes
  PROJECTS = {
    "financetoolkit" => "JerBouma/FinanceToolkit",
  }.freeze

  module_function

  def github(path)
    uri = URI("https://api.github.com/#{path}")
    req = Net::HTTP::Get.new(uri)
    req["Accept"] = "application/vnd.github.html+json"
    req["User-Agent"] = "jeroenbouma.com"
    token = ENV["GITHUB_TOKEN"]
    req["Authorization"] = "Bearer #{token}" if token && !token.empty?
    res = Net::HTTP.start(uri.host, uri.port, use_ssl: true, open_timeout: 8, read_timeout: 20) { |h| h.request(req) }
    res.is_a?(Net::HTTPSuccess) ? JSON.parse(res.body) : nil
  rescue StandardError
    nil
  end

  def fetch(repo)
    all = []
    (1..10).each do |page|
      list = github("repos/#{repo}/releases?per_page=100&page=#{page}")
      return nil unless list.is_a?(Array)
      all.concat(list)
      break if list.size < 100
    end
    all.reject { |r| r["draft"] || r["prerelease"] }.map do |r|
      {
        "tag" => r["tag_name"],
        "name" => r["name"].to_s.strip.empty? ? r["tag_name"] : r["name"].strip,
        "date" => r["published_at"].to_s[0, 10],
        "url" => r["html_url"],
        "html" => r["body_html"].to_s,
      }
    end
  end

  def slug(text)
    text.downcase.gsub(/<[^>]+>/, "").gsub(/&[a-z]+;/, "").gsub(/[^a-z0-9]+/, "-").gsub(/\A-|-\z/, "")
  end

  def prepare(html, tag)
    prefix = slug(tag)
    seen = Hash.new(0)
    html
      .gsub(/\s(?:class|data-[a-z-]+)="[^"]*"/, "")
      .gsub(/<a href="(https?:[^"]+)"(?![^>]*target=)/, '<a href="\1" target="_blank" rel="noopener"')
      .gsub(%r{<h([1-6])>(.*?)</h\1>}m) do
        level = [Regexp.last_match(1).to_i + 2, 6].min
        text = Regexp.last_match(2)
        id = "#{prefix}-#{slug(text)}"
        seen[id] += 1
        id += "-#{seen[id]}" if seen[id] > 1
        %(<h#{level} id="#{id}">#{text}</h#{level}>)
      end
  end
end

Jekyll::Hooks.register :site, :post_read do |site|
  data = (site.data["releases"] ||= {})
  ReleaseNotes::PROJECTS.each do |key, repo|
    live = ENV["LIVE_STATS"] == "off" ? nil : ReleaseNotes.fetch(repo)
    if live && !live.empty?
      data[key] = live
      if ENV["RELEASES_SNAPSHOT"] == "1"
        File.write(File.join(site.source, "_data", "releases", "#{key}.json"), JSON.pretty_generate(live) + "\n")
      end
    end
    releases = Array(data[key])
    releases.each do |r|
      r["id"] = ReleaseNotes.slug(r["tag"])
      r["body_html"] = ReleaseNotes.prepare(r["html"].to_s, r["tag"])
    end
    Jekyll.logger.info "Release notes:", "#{releases.size} #{key} releases (#{live ? 'GitHub' : 'snapshot'})"
  end
end
