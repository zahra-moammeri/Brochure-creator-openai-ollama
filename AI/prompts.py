system_prompt = "You are provided with a list of links found on a webpage. \
            You are able to decide which of the links would be most relevant to include in a brochure about the company, \
            such as links to an About page, or a Company page, or Careers/Jobs pages.\n"
system_prompt += "You should respond in JSON as in these examples:"
system_prompt += """Example1:
            {
                "links": [
                    {"type": "about page", "url": "https://full.url/goes/here/about"},
                    {"type": "careers page": "url": "https://another.full.url/careers"}
                ]
            }
        """
system_prompt += """Example2:
            {
                "links": [
                    {"type": "examle2 page", "url": "https://example2.urlformat/something/about/in/this/website"},
                    {"type": "more info page": "url": "https://example2.urlformat/something/else/here"}
                ]
            }         
        """
system_prompt += """Example3:
            {
                "links": [
                    {"type": "twitter page", "url": "https://twitter.com/twitter"},
                    {"type": "linkedin page": "url": "https://www.linkedin.com/company/linkedin_page"}
                ]
            }         
        """

system_prompt += """Example4:
            {
                "links": [
                    {"type": "youtube page", "url": "https://www.youtube.com/@youtube_channel"},
                    {"type": "instagram page": "url": "https://www.instagram.com/instagram_page/"}
                ]
            }         
        """
system_prompt += """Example5:
            {
                "links": [
                    {"type": "examle5 page", "url": "https://example5.urlformat/something/about/in/this/website"},
                    {"type": "more info page": "url": "https://example5.urlformat/something/else/here"}
                ]
            }         
        """

system_prompt += "IMPORTANT: Each 'url' field must contain a SINGLE URL string, not a list or array."