import re
import json
from urllib.parse import urlparse

from AI import config
from AI import prompts
from AI.crawl import Website


def get_links_user_prompt(website):
    user_prompt = f"Here is the list of links on the website of {website.url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the company, \
                    respond with the full https URL in JSON format. \
                    Do not include Terms of Service, Privacy, email links.\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(website.links)
    return user_prompt


# def get_links(url):
#     website = Website(url)
#     response = config.openai.chat.completions.create(
#         model=config.MODEL,
#         messages=[
#             {"role": "system", "content": prompts.system_prompt},
#             {"role": "user", "content": get_links_user_prompt(website)}
#       ],
#         response_format={"type": "json_object"}  # even if by defining response_format we have to specify an example in system prompt too
#     )
#     result = response.choices[0].message.content
#     return json.loads(result)

def get_links(url):
    # website = Website(url)

    # try:
    #     await website.scrape()
    user_prompt = get_links_user_prompt(url)
    response = config.openai.chat.completions.create(
        model=config.MODEL,
        messages=[
            {"role": "system", "content": prompts.system_prompt},
            {"role": "user", "content": user_prompt}
    ],
        response_format={"type": "json_object"}  # even if by defining response_format we have to specify an example in system prompt too
    )
    result = response.choices[0].message.content
    return json.loads(result)
    
    # finally:
    #     await website.close()



def clean_url(url):
    """Clean and validate URL string."""
    if not url or not isinstance(url, str):
        return None
    
    # If it looks like a string representation of a list
    if url.startswith('[') and url.endswith(']'):
        # Extract first URL from the list
        match = re.search(r"'(https?://[^']+)'", url)
        if match:
            return match.group(1)
        return None
    
    # Basic URL validation
    parsed = urlparse(url)
    if parsed.scheme and parsed.netloc:
        return url
    
    return None


async def get_all_details(url):
    website = Website(url)
    result = "Landing page:\n"
    try:
        await website.scrape()
        result += website.get_contents()
        # result += Website(url).get_contents()
        links = get_links(website)
        # print("Found links:", links)
        for link in links["links"]:
            link_type = link.get("type") or link.get("Type") or ""
            raw_url = link.get("url")
            # Clean the URL
            clean_url_str = clean_url(raw_url)
            if not clean_url_str:
                print(f"Warning: Invalid URL for {link_type}: {raw_url}")
                result += f"\n\n{link_type}\n[Unable to fetch: Invalid URL]"
                continue

            # try:
            #     result += f"\n\n{link_type}\n"
            #     scrape_link = Website(clean_url_str)
            #     scraped = await scrape_link.scrape()
            #     if scraped:
            #         result += scrape_link.get_contents()
            #     else:
            #         result += "[Failed to scrape page]"
            #         print(f"Failed to scrape {clean_url_str}")                 
            #     # result += website.link["url"].get_contents()
            #     print(f"Successfully scraped {clean_url_str}")

            # except Exception as e:
            #     print(f"Error fetching {clean_url_str}: {e}")
            #     result += f"\n\n{link_type}\n[Error loading page: {str(e)}]"

            # finally:
            #     await scrape_link.close()
                    
        return result
    
    finally:
        await website.close()