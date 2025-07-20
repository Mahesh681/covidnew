#!/usr/bin/env python3
"""
LinkedIn Job Scraper
Fetches the latest LinkedIn job postings using the public jobs API
"""

import asyncio
import csv
import json
import logging
import sys
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urlencode, quote_plus

import httpx
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('linkedin_scraper.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class LinkedInJobScraper:
    """
    A comprehensive LinkedIn job scraper that fetches job postings
    from LinkedIn's public jobs API without requiring authentication.
    """
    
    def __init__(self):
        self.base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
        self.jobs_per_page = 25
        self.headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "priority": "u=1, i",
            "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        }
        self.job_postings = []

    async def search_jobs(
        self,
        keywords: str = "software engineer",
        location: str = "United States",
        pages: int = 5,
        job_type: Optional[str] = None,
        experience_level: Optional[str] = None,
        remote: bool = False
    ) -> List[Dict]:
        """
        Search for LinkedIn jobs with specified criteria.
        
        Args:
            keywords: Job search keywords (e.g., "python developer", "data scientist")
            location: Job location (e.g., "United States", "New York, NY")
            pages: Number of pages to scrape (25 jobs per page)
            job_type: Job type filter ("full-time", "part-time", "contract", etc.)
            experience_level: Experience level ("entry", "mid", "senior", "executive")
            remote: Whether to filter for remote jobs
            
        Returns:
            List of job posting dictionaries
        """
        logger.info(f"Starting job search for '{keywords}' in '{location}' - {pages} pages")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            for page in range(pages):
                try:
                    params = self._build_search_params(
                        keywords, location, page, job_type, experience_level, remote
                    )
                    
                    logger.info(f"Fetching page {page + 1}/{pages}")
                    response = await client.get(
                        self.base_url,
                        headers=self.headers,
                        params=params
                    )
                    
                    if response.status_code == 200:
                        jobs = self._parse_jobs_page(response.content, keywords, location)
                        self.job_postings.extend(jobs)
                        logger.info(f"Found {len(jobs)} jobs on page {page + 1}")
                        
                        # Add delay to be respectful
                        await asyncio.sleep(2)
                    else:
                        logger.warning(f"Failed to fetch page {page + 1}: HTTP {response.status_code}")
                        
                except Exception as e:
                    logger.error(f"Error fetching page {page + 1}: {str(e)}")
                    continue
        
        logger.info(f"Total jobs found: {len(self.job_postings)}")
        return self.job_postings

    def _build_search_params(
        self,
        keywords: str,
        location: str,
        page: int,
        job_type: Optional[str] = None,
        experience_level: Optional[str] = None,
        remote: bool = False
    ) -> Dict:
        """Build search parameters for the LinkedIn API request."""
        params = {
            "keywords": keywords,
            "location": location,
            "trk": "public_jobs_jobs-search-bar_search-submit",
            "position": "1",
            "pageNum": "0",
            "start": str(page * self.jobs_per_page)
        }
        
        # Add optional filters
        filters = []
        
        if job_type:
            type_mapping = {
                "full-time": "F",
                "part-time": "P", 
                "contract": "C",
                "temporary": "T",
                "internship": "I"
            }
            if job_type.lower() in type_mapping:
                filters.append(f"JT-{type_mapping[job_type.lower()]}")
        
        if experience_level:
            level_mapping = {
                "internship": "1",
                "entry": "2", 
                "associate": "3",
                "mid": "4",
                "senior": "5",
                "director": "6",
                "executive": "7"
            }
            if experience_level.lower() in level_mapping:
                filters.append(f"E-{level_mapping[experience_level.lower()]}")
        
        if remote:
            filters.append("WRA-1")  # Remote work filter
        
        if filters:
            params["f_JT"] = ",".join([f for f in filters if f.startswith("JT-")])
            params["f_E"] = ",".join([f for f in filters if f.startswith("E-")])
            params["f_WRA"] = ",".join([f for f in filters if f.startswith("WRA-")])
        
        return params

    def _parse_jobs_page(self, html_content: bytes, search_keywords: str, search_location: str) -> List[Dict]:
        """Parse job listings from HTML content."""
        soup = BeautifulSoup(html_content, "html.parser")
        job_elements = soup.select("li")
        jobs = []
        
        for job_element in job_elements:
            try:
                job_data = self._extract_job_data(job_element, search_keywords, search_location)
                if job_data and job_data.get('title'):  # Only add valid jobs
                    jobs.append(job_data)
            except Exception as e:
                logger.debug(f"Error parsing job element: {str(e)}")
                continue
        
        return jobs

    def _extract_job_data(self, job_element, search_keywords: str, search_location: str) -> Optional[Dict]:
        """Extract job data from a single job listing element."""
        # Extract job URL
        link_element = job_element.select_one("a[data-tracking-control-name='public_jobs_jserp-result_search-card']")
        if not link_element:
            link_element = job_element.select_one("a.base-card__full-link")
        
        job_url = link_element.get("href") if link_element else None
        
        # Extract job title
        title_element = job_element.select_one("h3.base-search-card__title")
        if not title_element:
            title_element = job_element.select_one("h3")
        title = title_element.get_text(strip=True) if title_element else None
        
        # Extract company name
        company_element = job_element.select_one("h4.base-search-card__subtitle a")
        if not company_element:
            company_element = job_element.select_one("h4.base-search-card__subtitle")
        company = company_element.get_text(strip=True) if company_element else None
        
        # Extract location
        location_element = job_element.select_one(".job-search-card__location")
        if not location_element:
            location_element = job_element.select_one(".base-search-card__metadata span")
        location = location_element.get_text(strip=True) if location_element else None
        
        # Extract posting date
        date_element = job_element.select_one("time.job-search-card__listdate")
        if not date_element:
            date_element = job_element.select_one("time")
        
        posted_date = None
        posted_time_ago = None
        if date_element:
            posted_date = date_element.get("datetime")
            posted_time_ago = date_element.get_text(strip=True)
        
        # Extract job ID from URL or data attributes
        job_id = None
        if job_url and "/view/" in job_url:
            try:
                job_id = job_url.split("/view/")[1].split("?")[0].split("-")[-1]
            except:
                pass
        
        if not job_id:
            urn_element = job_element.get("data-entity-urn")
            if urn_element:
                job_id = urn_element.split(":")[-1]
        
        # Extract additional metadata
        applicants_element = job_element.select_one(".job-search-card__applicants")
        applicants = applicants_element.get_text(strip=True) if applicants_element else None
        
        # Check for promoted/sponsored jobs
        promoted = bool(job_element.select_one(".job-search-card__promoted"))
        
        # Build job data dictionary
        job_data = {
            "job_id": job_id,
            "title": title,
            "company": company,
            "location": location,
            "job_url": job_url,
            "posted_date": posted_date,
            "posted_time_ago": posted_time_ago,
            "applicants": applicants,
            "is_promoted": promoted,
            "search_keywords": search_keywords,
            "search_location": search_location,
            "scraped_at": datetime.now().isoformat()
        }
        
        return job_data

    def get_trending_keywords(self) -> List[str]:
        """Get trending job search keywords."""
        return [
            "software engineer", "data scientist", "product manager", "devops engineer",
            "frontend developer", "backend developer", "full stack developer",
            "machine learning engineer", "cybersecurity analyst", "cloud architect",
            "ui/ux designer", "business analyst", "project manager", "marketing manager",
            "sales manager", "hr manager", "financial analyst", "operations manager"
        ]

    def get_popular_locations(self) -> List[str]:
        """Get popular job search locations."""
        return [
            "United States", "New York, NY", "San Francisco, CA", "Los Angeles, CA",
            "Seattle, WA", "Chicago, IL", "Boston, MA", "Austin, TX", "Denver, CO",
            "Atlanta, GA", "Remote", "London, UK", "Toronto, Canada", "Berlin, Germany"
        ]

    def save_to_csv(self, filename: str = None) -> str:
        """Save job postings to CSV file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"linkedin_jobs_{timestamp}.csv"
        
        if not self.job_postings:
            logger.warning("No job postings to save")
            return filename
        
        fieldnames = [
            "job_id", "title", "company", "location", "job_url", 
            "posted_date", "posted_time_ago", "applicants", "is_promoted",
            "search_keywords", "search_location", "scraped_at"
        ]
        
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.job_postings)
        
        logger.info(f"Saved {len(self.job_postings)} jobs to {filename}")
        return filename

    def save_to_json(self, filename: str = None) -> str:
        """Save job postings to JSON file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"linkedin_jobs_{timestamp}.json"
        
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(self.job_postings, file, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(self.job_postings)} jobs to {filename}")
        return filename

    def get_job_stats(self) -> Dict:
        """Get statistics about scraped jobs."""
        if not self.job_postings:
            return {}
        
        companies = [job.get("company") for job in self.job_postings if job.get("company")]
        locations = [job.get("location") for job in self.job_postings if job.get("location")]
        
        from collections import Counter
        
        stats = {
            "total_jobs": len(self.job_postings),
            "unique_companies": len(set(companies)),
            "top_companies": dict(Counter(companies).most_common(10)),
            "top_locations": dict(Counter(locations).most_common(10)),
            "promoted_jobs": sum(1 for job in self.job_postings if job.get("is_promoted")),
            "jobs_with_applicant_count": sum(1 for job in self.job_postings if job.get("applicants"))
        }
        
        return stats

    def print_summary(self):
        """Print a summary of scraped jobs."""
        stats = self.get_job_stats()
        
        print("\n" + "="*50)
        print("LINKEDIN JOBS SCRAPING SUMMARY")
        print("="*50)
        print(f"Total Jobs Found: {stats.get('total_jobs', 0)}")
        print(f"Unique Companies: {stats.get('unique_companies', 0)}")
        print(f"Promoted Jobs: {stats.get('promoted_jobs', 0)}")
        
        print("\nTop Companies:")
        for company, count in list(stats.get('top_companies', {}).items())[:5]:
            print(f"  • {company}: {count} jobs")
        
        print("\nTop Locations:")
        for location, count in list(stats.get('top_locations', {}).items())[:5]:
            print(f"  • {location}: {count} jobs")
        
        print("="*50)


async def main():
    """Main function to demonstrate the scraper."""
    scraper = LinkedInJobScraper()
    
    # Example searches
    search_configs = [
        {
            "keywords": "python developer",
            "location": "United States",
            "pages": 3,
            "remote": True
        },
        {
            "keywords": "data scientist",
            "location": "San Francisco, CA",
            "pages": 2,
            "experience_level": "mid"
        },
        {
            "keywords": "software engineer",
            "location": "Remote",
            "pages": 2,
            "job_type": "full-time"
        }
    ]
    
    # Run searches
    for config in search_configs:
        print(f"\nSearching for {config['keywords']} jobs...")
        await scraper.search_jobs(**config)
        await asyncio.sleep(3)  # Be respectful between searches
    
    # Print summary and save results
    scraper.print_summary()
    
    # Save to both CSV and JSON
    csv_file = scraper.save_to_csv()
    json_file = scraper.save_to_json()
    
    print(f"\nResults saved to:")
    print(f"  CSV: {csv_file}")
    print(f"  JSON: {json_file}")
    
    # Show some sample jobs
    if scraper.job_postings:
        print(f"\nSample jobs (first 3):")
        for i, job in enumerate(scraper.job_postings[:3], 1):
            print(f"\n{i}. {job.get('title', 'N/A')}")
            print(f"   Company: {job.get('company', 'N/A')}")
            print(f"   Location: {job.get('location', 'N/A')}")
            print(f"   Posted: {job.get('posted_time_ago', 'N/A')}")
            if job.get('job_url'):
                print(f"   URL: {job['job_url']}")


if __name__ == "__main__":
    print("LinkedIn Job Scraper - Fetching Latest Jobs")
    print("=" * 50)
    asyncio.run(main())