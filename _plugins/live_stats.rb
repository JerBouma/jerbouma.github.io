# Keeps the project numbers on the site up to date without editing them by
# hand. After the data files are read, every hash in _data that has a
# `github` URL and a `stats` list gets its stars, forks and downloads
# refreshed: stars and forks from the GitHub API, downloads (all-time PyPI)
# from pepy.tech, for the package named after the repository. The values in
# the data files are the fallback when a source cannot be reached (offline
# builds, rate limits), so a build never fails because of this.
#
# _data/projects.yml can also hold `github: { stars:, downloads: }` totals;
# those become the sum over all of @JerBouma's own repositories and over
# the packages refreshed above.
#
# The deploy workflow rebuilds the site every week, so the numbers stay
# current even when nothing is merged.

require "json"
require "net/http"
require "uri"

module LiveStats
  USER = "JerBouma"

  module_function

  def get(url, headers = {})
    uri = URI(url)
    req = Net::HTTP::Get.new(uri)
    headers.each { |k, v| req[k] = v }
    Net::HTTP.start(uri.host, uri.port, use_ssl: true, open_timeout: 8, read_timeout: 12) do |http|
      res = http.request(req)
      res.is_a?(Net::HTTPSuccess) ? res.body : nil
    end
  rescue StandardError
    nil
  end

  def github(path)
    headers = { "Accept" => "application/vnd.github+json", "User-Agent" => "jeroenbouma.com" }
    token = ENV["GITHUB_TOKEN"]
    headers["Authorization"] = "Bearer #{token}" if token && !token.empty?
    body = get("https://api.github.com/#{path}", headers)
    body && JSON.parse(body)
  rescue JSON::ParserError
    nil
  end

  # pepy.tech's badge reads e.g. "644k" or "1.2M"; its API needs a key
  def downloads(package)
    svg = get("https://static.pepy.tech/badge/#{package.downcase}", "User-Agent" => "jeroenbouma.com")
    text = svg && svg.scan(/>([0-9.,]+)\s*([kKmM]?)</).last
    return nil unless text
    n = text[0].delete(",").to_f
    n *= { "k" => 1e3, "m" => 1e6 }.fetch(text[1].downcase, 1)
    n.to_i
  end

  # round down to a figure that stays true for a while: 9,383 -> "9,300+",
  # 971 -> "950+", 644,000 -> "640,000+", 1,416,000 -> "1.4M+"
  def label(n)
    return format("%.1fM+", (n / 100_000).floor / 10.0) if n >= 1_000_000
    step = if n >= 100_000 then 10_000
           elsif n >= 10_000 then 1_000
           elsif n >= 1_000 then 100
           elsif n >= 100 then 50
           else 10
           end
    with_commas((n / step) * step) + "+"
  end

  def with_commas(n)
    n.to_s.reverse.scan(/\d{1,3}/).join(",").reverse
  end

  def repo_of(url)
    url.to_s[%r{github\.com/([^/]+/[^/#?]+)}, 1]
  end

  # every hash with a github URL and a stats list, anywhere in the data
  def each_entry(node, &block)
    case node
    when Hash
      yield node if node["stats"].is_a?(Array) && repo_of(node["github"])
      node.each_value { |v| each_entry(v, &block) }
    when Array
      node.each { |v| each_entry(v, &block) }
    end
  end
end

Jekyll::Hooks.register :site, :post_read do |site|
  next if ENV["LIVE_STATS"] == "off"

  repos = {}
  pypi = {}
  LiveStats.each_entry(site.data) { |e| repos[LiveStats.repo_of(e["github"])] = nil }
  repos.each_key do |r|
    repos[r] = LiveStats.github("repos/#{r}")
    owner, name = r.split("/")
    pypi[r] = LiveStats.downloads(name) if owner == LiveStats::USER
  end

  updated = 0
  LiveStats.each_entry(site.data) do |e|
    r = LiveStats.repo_of(e["github"])
    info = repos[r]
    e["stats"].each do |s|
      label = s["label"].to_s.downcase
      n = if label.include?("star") then info && info["stargazers_count"]
          elsif label.include?("fork") then info && info["forks_count"]
          elsif label.include?("download") then pypi[r]
          end
      next unless n && n.positive?
      s["value"] = LiveStats.label(n)
      updated += 1
    end
  end

  totals = site.data.dig("projects", "github")
  if totals.is_a?(Hash)
    stars = 0
    page = 1
    loop do
      list = LiveStats.github("users/#{LiveStats::USER}/repos?per_page=100&page=#{page}")
      break unless list.is_a?(Array) && !list.empty?
      stars += list.reject { |x| x["fork"] }.sum { |x| x["stargazers_count"].to_i }
      page += 1
    end
    totals["stars"] = LiveStats.label(stars) if stars.positive?
    # each package counted once, even when it shows up in several data files
    total = pypi.values.compact.sum
    totals["downloads"] = LiveStats.label(total) if total.positive?
    user = LiveStats.github("users/#{LiveStats::USER}")
    totals["followers"] = LiveStats.label(user["followers"].to_i) if user && user["followers"].to_i.positive?
  end

  Jekyll.logger.info "Live stats:", "#{updated} numbers refreshed from GitHub and pepy.tech"
end
