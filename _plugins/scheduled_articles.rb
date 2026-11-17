# Articles with a date in the future (front matter `date: 2026-11-29 09:00:00 +0100`) are left
# out of the build until that moment, so they don't appear on /insights, in the sitemap, feed or
# search before then. The Pages workflow rebuilds on Sunday morning to publish them on time.
# Set SHOW_SCHEDULED=1 to build them anyway (previewing a scheduled article locally).
module ScheduledArticles
  class Generator < Jekyll::Generator
    safe true
    priority :highest

    def generate(site)
      return if ENV["SHOW_SCHEDULED"] == "1"

      now = Time.now
      scheduled = site.pages.select do |page|
        page.data["collection"] == "article" && page.data["date"] && to_time(page.data["date"]) > now
      end
      scheduled.each do |page|
        Jekyll.logger.info "Scheduled:", "#{page.url} (#{page.data['date']})"
        site.pages.delete(page)
      end
    end

    private

    # A plain date (2026-11-29) counts as midnight in the site's time zone.
    def to_time(value)
      value.is_a?(Date) && !value.is_a?(DateTime) ? Time.new(value.year, value.month, value.day) : Time.parse(value.to_s)
    end
  end
end
