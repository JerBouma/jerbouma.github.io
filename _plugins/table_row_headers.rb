# Post-render pass over every HTML page: in a table whose top-left header cell
# is empty (a pandas DataFrame printed as Markdown, with the index as its first
# column), each row's first cell becomes <th scope="row">. Screen readers then
# announce a value with both its row and column label ("Gross Margin, 2021"),
# and accessibility checks no longer flag the table as having cells without
# headers. The row headers are styled like ordinary cells (_sass/custom.scss).
module TableRowHeaders
  TABLE = %r{<table>\s*<thead>\s*<tr>\s*<th[^>]*>[\s\u00A0]*(?:&nbsp;)?[\s\u00A0]*</th>.*?</table>}m
  CORNER = %r{(<thead>\s*<tr>\s*)<th([^>]*)>[\s\u00A0]*(?:&nbsp;)?[\s\u00A0]*</th>}m
  FIRST_CELL = %r{(<tr>\s*)<td([^>]*)>(.*?)</td>}m

  def self.process(html)
    return html unless html.include?("<table>")
    html.gsub(TABLE) do |table|
      head, body = table.split("<tbody>", 2)
      next table unless body
      # the empty corner cell gets a label only screen readers hear: an empty <th>
      # is a header without text (axe: empty-table-header); it keeps its styling
      head = head.sub(CORNER) { "#{$1}<th#{$2}><span class=\"visually-hidden\">Item</span></th>" }
      head + "<tbody>" + body.gsub(FIRST_CELL) { "#{$1}<th scope=\"row\"#{$2}>#{$3}</th>" }
    end
  end
end

Jekyll::Hooks.register [:pages, :documents], :post_render do |doc|
  next unless doc.output_ext == ".html" && doc.output
  doc.output = TableRowHeaders.process(doc.output)
end
