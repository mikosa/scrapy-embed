# import pdfkit
import os
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from w3lib.html import remove_tags

# Configure pdfkit with the path to wkhtmltopdf executable
# pdfkit_config = pdfkit.configuration(wkhtmltopdf='path/to/wkhtmltopdf')

class GitHubDocSpider(CrawlSpider):
    name = 'github'
    start_urls = ['https://docs.github.com/en/enterprise-server@3.11']

    # Define rules to follow links within the same path and to other subpaths
    rules = (
        Rule(LinkExtractor(allow=('/en/enterprise-server@3.11/',)), callback='parse_page', follow=True),
    )

    def __init__(self, *args, **kwargs):
        super(GitHubDocSpider, self).__init__(*args, **kwargs)
        self.pdf_content = ""

    def parse_page(self, response):
        # Extract and process data from the page
        # You can use XPath or CSS selectors to extract specific content

        # Extract the title if available
        title = response.css('h1::text').get()

        # Extract the body text including links
        body_text = ""

        for paragraph in response.css('p'):
            # Extract text content from the paragraph (excluding links)
            text_content = remove_tags(paragraph.get())
            body_text += text_content + "\n"

            # Extract links from the paragraph
            links = paragraph.css('a::attr(href)').getall()
            for link in links:
                body_text += f"Link: {link}\n"

        # Check if title and body_text are not None before using get()
        if title:
            title = title.strip()
        if body_text:
            body_text = body_text.strip()

        # Append the content of this page to the pdf_content
        self.pdf_content += f"URL: {response.url}\n\nTitle: {title}\n\n{body_text}\n\n"

    def closed(self, reason):
        # Create the output subfolder if it doesn't exist
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)

        # Generate the PDF file name
        pdf_filename = os.path.join(output_dir, "merged_pages.pdf")

        # Save all the content to a single PDF file
        # pdfkit.from_string(self.pdf_content, pdf_filename, configuration=pdfkit_config)
        
                # Save the content to a file within the "output" subfolder
        filename = os.path.join(output_dir, "output.txt")
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(self.pdf_content)

# Rest of the code remains the same

