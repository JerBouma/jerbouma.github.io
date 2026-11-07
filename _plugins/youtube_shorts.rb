# Fills /insights/youtube with the shorts of my YouTube channel, grouped by
# the playlists in _data/youtube.yml (News Explained, Finance Explained).
#
# Each playlist is read from YouTube's public RSS feed at build time (no API
# key needed). A feed holds the 15 most recent videos, so the result is merged
# with _data/youtube_shorts.json, the snapshot of every short seen so far:
# older shorts stay on the page, and when YouTube can't be reached (offline
# builds, LIVE_STATS=off) the snapshot alone is used, so a build never fails
# because of this.
#
# The deploy workflow keeps the snapshot up to date by itself: it restores the
# latest one from the `youtube-data` branch before the build, builds with
# YOUTUBE_SNAPSHOT=1 (which writes the merged list back to the file) and
# commits the result to that branch. The copy in _data on main is only the
# starting point for local builds.
#
# Each short gets the Finance Toolkit MCP concepts it uses, matched from its
# title and description with the patterns in _data/youtube.yml (`overrides`
# there sets them by hand), plus a summary, the closing lesson and the data
# line from the description. The deploy workflow rebuilds the site every day,
# so a new short appears without a commit.

require "json"
require "net/http"
require "rexml/document"
require "time"
require "uri"

module YouTubeShorts
  SNAPSHOT = "_data/youtube_shorts.json"
  NS = {
    "a" => "http://www.w3.org/2005/Atom",
    "yt" => "http://www.youtube.com/xml/schemas/2015",
    "media" => "http://search.yahoo.com/mrss/"
  }.freeze

  module_function

  def fetch(playlist_id)
    uri = URI("https://www.youtube.com/feeds/videos.xml?playlist_id=#{playlist_id}")
    res = Net::HTTP.start(uri.host, uri.port, use_ssl: true, open_timeout: 8, read_timeout: 12) do |http|
      http.request(Net::HTTP::Get.new(uri, "User-Agent" => "jeroenbouma.com"))
    end
    res.is_a?(Net::HTTPSuccess) ? parse(res.body) : nil
  rescue StandardError
    nil
  end

  def parse(xml)
    doc = REXML::Document.new(xml)
    REXML::XPath.match(doc, "//a:entry", NS).map do |e|
      text = ->(path) { REXML::XPath.first(e, path, NS)&.text.to_s }
      {
        "id" => text.call("yt:videoId"),
        "title" => text.call("a:title"),
        "published" => text.call("a:published"),
        "description" => text.call("media:group/media:description")
      }
    end
  rescue StandardError
    nil
  end

  # the description's paragraphs without the channel's boilerplate
  def paragraphs(description)
    description.split(/\n\s*\n/).map do |para|
      para.lines.map(&:strip).reject do |line|
        line.empty? || line =~ %r{https?://} || line =~ /^pip install/i ||
          line =~ /^Not investment advice/i || line =~ /^(#\S+\s*)+$/ ||
          line =~ /"Finance Toolkit MCP" to give your AI/i
      end.join(" ")
    end.reject(&:empty?)
  end

  def enrich(video, series, config)
    paras = paragraphs(video["description"].to_s)
    data_at = paras.index { |p| p =~ /^(Data|Numbers|Prices)\b/ && p =~ /Finance Toolkit/ }
    body = data_at ? paras[0...data_at] : paras
    lesson = body.length > 1 && body.last.length <= 180 ? body.last : nil
    haystack = [video["title"], *body, data_at && paras[data_at]].compact.join(" ")

    override = (config["overrides"] || {})[video["id"]] || {}
    concepts = override["concepts"] || config["concepts"].select do |c|
      Regexp.new(c["match"], Regexp::IGNORECASE).match?(haystack)
    end.map { |c| c["key"] }

    data = data_at && paras[data_at].sub(/\s*(News|Source)s?:.*$/, "")
                                    .sub(/\s*Your AI assistant.*$/, "").sub(/^Data:\s*/, "")
    first = body.first.to_s.split(/(?<=[.!?])\s+(?=[A-Z])/).first.to_s

    video.reject { |k, _| k == "description" }.merge(
      "series" => series,
      "title" => video["title"].gsub(/\s*#[^\s#]+/, "").squeeze(" ").strip,
      "summary" => body.first.to_s,
      "lesson" => lesson,
      "teaser" => lesson || first,
      "data" => data,
      "concepts" => concepts
    )
  end

  def snapshot(site)
    path = File.join(site.source, SNAPSHOT)
    File.exist?(path) ? JSON.parse(File.read(path, encoding: "UTF-8")) : []
  rescue JSON::ParserError
    []
  end
end

Jekyll::Hooks.register :site, :post_read do |site|
  config = site.data["youtube"]
  next unless config

  offline = ENV["LIVE_STATS"] == "off" && ENV["YOUTUBE_SNAPSHOT"] != "1"
  known = YouTubeShorts.snapshot(site).to_h { |v| [v["id"], v] }

  config["playlists"].each do |playlist|
    entries = offline ? nil : YouTubeShorts.fetch(playlist["id"])
    if entries.nil?
      Jekyll.logger.info "YouTube:", "#{playlist['name']} from the snapshot" unless offline
      next
    end
    # a feed with fewer than 15 videos is the whole playlist, so a short that
    # was taken out of it leaves the page too
    if entries.size < 15
      ids = entries.map { |v| v["id"] }
      known.reject! { |id, v| v["series"] == playlist["key"] && !ids.include?(id) }
    end
    entries.each do |v|
      # keep the raw description so the snapshot can be enriched again later
      known[v["id"]] = (known[v["id"]] || {}).merge(v).merge("series" => playlist["key"])
    end
  end

  if ENV["YOUTUBE_SNAPSHOT"] == "1"
    raw = known.values.sort_by { |v| v["published"] }.reverse
    File.write(File.join(site.source, YouTubeShorts::SNAPSHOT), JSON.pretty_generate(raw) + "\n", encoding: "UTF-8")
    Jekyll.logger.info "YouTube:", "snapshot written (#{raw.size} shorts)"
  end

  shorts = known.values.map { |v| YouTubeShorts.enrich(v, v["series"], config) }
                .sort_by { |v| v["published"] }.reverse
  site.data["youtube_shorts"] = shorts
end
