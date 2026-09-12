# Fills in `last_modified_at` for every page and document from the git history
# (the commit that last touched the source file), unless the front matter sets
# it explicitly. jekyll-sitemap turns the value into <lastmod> and
# jekyll-seo-tag into "dateModified" in the JSON-LD, so search engines can tell
# which pages actually changed instead of treating every deploy as new.
#
# The theme prints a visible "Updated:" line whenever `last_modified_at` is set,
# which is only wanted where the front matter asks for it, so pages dated here
# are flagged with `last_modified_at_from_git` and _includes/page__date.html
# skips those.
#
# One `git log` for the whole repository is parsed up front, so the cost is a
# fraction of a second regardless of page count. The CI checkout needs the full
# history (fetch-depth: 0) for the dates to mean anything; on a shallow clone
# every file would simply report the single fetched commit.
module LastModified
  def self.dates(site)
    @dates ||= begin
      dates  = {}
      prefix = IO.popen(["git", "-C", site.source, "rev-parse", "--show-prefix"], &:read).to_s.strip
      log    = IO.popen(["git", "-C", site.source, "log", "--format=%ct", "--name-only"], &:read).to_s
      stamp  = nil
      log.each_line do |line|
        line = line.chomp
        next if line.empty?
        if line =~ /\A\d+\z/
          stamp = Time.at(line.to_i)
        elsif line.start_with?(prefix)
          dates[line.delete_prefix(prefix)] ||= stamp
        end
      end
      dates
    rescue SystemCallError
      {}
    end
  end

  def self.apply(item)
    return unless item.data["last_modified_at"].nil?
    return unless item.respond_to?(:relative_path)
    date = dates(item.site)[item.relative_path]
    if date.nil?
      file = File.join(item.site.source, item.relative_path)
      date = File.mtime(file) if File.file?(file)
    end
    return unless date
    item.data["last_modified_at"] = date
    item.data["last_modified_at_from_git"] = true
  end
end

Jekyll::Hooks.register [:pages, :documents], :post_init do |item|
  LastModified.apply(item)
end
