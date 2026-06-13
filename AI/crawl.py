
from bs4 import BeautifulSoup

from AI import config

import httpx
from typing import List



class Website:
    """
    A utility class to represent a Website that we have scraped, now with links
    """

    def __init__(self, url: str):
        self.url = url
        self.session = httpx.AsyncClient(headers=config.headers, timeout=20.0)
        self.processed_urls = set()

        self.title: str = ""
        self.text: str = ""
        self.links: List[str] = []
        self.content: str|None = None

    async def fetch(self) -> str|None:
        """
        Fetch page content
        """
        try:
            response = await self.session.get(self.url)
            response.raise_for_status()  # Raise an exception for bad status codes
            # response = await self.session.get(url, headers=headers, verify=False)
            self.content = response.text
            return self.content
        except httpx.HTTPStatusError as e:
            self.error = f"HTTP error {e.response.status_code} for {self.url}"
            print(self.error)
        except httpx.RequestError as e:
            self.error = f"Request error for {self.url}: {e}"
            print(self.error)
        except Exception as e:
            self.error = f"An unexpected error occurred during fetch for {self.url}: {e}"
            print(self.error)
        return False
    

    async def parse(self) -> List[str]:
        """
        Parse HTML and extract title, text and links.
        """
        if not self.content:
            print(f"Cannot parse, no content for {self.url}")
            return
        
        try:
            soup = BeautifulSoup(self.content, 'html.parser')

            # Title
            self.title = soup.title.string if soup.title else "No title found"

            #Clean Text
            if soup.body:
                    for irrelevant in soup.body(["script", "style", "img", "input"]):
                        irrelevant.decompose()
                    self.text = soup.body.get_text(separator="\n", strip=True)

            #Extract Links
            self.links = [
                link.get('href') for link in soup.find_all('a') 
                if link.get("href")
                ]
        except Exception as e:
            print(f"Error parsing {self.url}: {e}")
            self.error = f"Parsing error for {self.url}: {e}"


    async def scrape(self):
        success = await self.fetch()
        if success:
            await self.parse()
            return True
        return False


    def get_contents(self):
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"
    

    async def close(self):
        await self.session.aclose()