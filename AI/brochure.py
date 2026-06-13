import asyncio
from AI import utils, config, prompts


def get_brochure_user_prompt(company_name, url):
    user_prompt = f"You are looking at a company called: {company_name}\n"
    user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
    user_prompt += f"Based on these information and contents figure out what this website is about.\n"
    user_prompt += "Structure the brochure clearly with headings. Ensure the language is professional and concise.\n"
    user_prompt += f"Add socila media links to a separate list and add the links at the end of the brochure. \n"
    details = asyncio.run(utils.get_all_details(url))
    user_prompt += details
    user_prompt = user_prompt[:5_000] # Truncate if more than 5,000 characters
    return user_prompt



def create_brochure(company_name, url):
    response = config.openai.chat.completions.create(
        model=config.MODEL,
        messages=[
            {"role": "system", "content": prompts.system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
          ],
    )
    result = response.choices[0].message.content
    return result