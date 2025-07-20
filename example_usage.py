#!/usr/bin/env python3
"""
Example usage of LinkedIn Job Scraper
This script demonstrates different ways to search for jobs
"""

import asyncio
from linkedin_job_scraper import LinkedInJobScraper


async def search_specific_roles():
    """Search for specific job roles with different filters."""
    scraper = LinkedInJobScraper()
    
    print("🔍 Searching for Python Developer jobs (Remote)...")
    await scraper.search_jobs(
        keywords="python developer",
        location="Remote",
        pages=2,
        job_type="full-time",
        remote=True
    )
    
    print("\n🔍 Searching for Data Science jobs (Entry Level)...")
    await scraper.search_jobs(
        keywords="data scientist",
        location="United States",
        pages=2,
        experience_level="entry"
    )
    
    return scraper


async def search_multiple_locations():
    """Search for the same role in multiple locations."""
    scraper = LinkedInJobScraper()
    
    locations = ["New York, NY", "San Francisco, CA", "Seattle, WA", "Austin, TX"]
    
    for location in locations:
        print(f"\n🔍 Searching for Software Engineer jobs in {location}...")
        await scraper.search_jobs(
            keywords="software engineer",
            location=location,
            pages=1,
            job_type="full-time"
        )
        await asyncio.sleep(2)  # Be respectful between searches
    
    return scraper


async def search_trending_keywords():
    """Search for jobs using trending keywords."""
    scraper = LinkedInJobScraper()
    
    trending_keywords = [
        "machine learning engineer",
        "devops engineer", 
        "frontend developer",
        "cybersecurity analyst"
    ]
    
    for keyword in trending_keywords:
        print(f"\n🔍 Searching for {keyword} jobs...")
        await scraper.search_jobs(
            keywords=keyword,
            location="United States",
            pages=1
        )
        await asyncio.sleep(2)
    
    return scraper


async def search_contract_jobs():
    """Search specifically for contract and part-time opportunities."""
    scraper = LinkedInJobScraper()
    
    print("🔍 Searching for Contract Developer jobs...")
    await scraper.search_jobs(
        keywords="developer",
        location="United States",
        pages=2,
        job_type="contract"
    )
    
    print("\n🔍 Searching for Part-time Data Analyst jobs...")
    await scraper.search_jobs(
        keywords="data analyst",
        location="United States", 
        pages=1,
        job_type="part-time"
    )
    
    return scraper


async def main():
    """Main function to run different search examples."""
    print("LinkedIn Job Scraper - Example Usage")
    print("=" * 50)
    
    # Choose which example to run
    examples = {
        "1": ("Specific Roles with Filters", search_specific_roles),
        "2": ("Multiple Locations", search_multiple_locations),
        "3": ("Trending Keywords", search_trending_keywords),
        "4": ("Contract/Part-time Jobs", search_contract_jobs)
    }
    
    print("\nAvailable examples:")
    for key, (name, _) in examples.items():
        print(f"  {key}. {name}")
    
    choice = input("\nEnter your choice (1-4) or press Enter for all: ").strip()
    
    if choice in examples:
        name, func = examples[choice]
        print(f"\nRunning: {name}")
        scraper = await func()
    else:
        print("\nRunning all examples...")
        scraper = LinkedInJobScraper()
        
        # Run a quick search for demo
        await scraper.search_jobs(
            keywords="software engineer",
            location="United States",
            pages=2,
            remote=True
        )
    
    # Print results and save
    scraper.print_summary()
    
    if scraper.job_postings:
        csv_file = scraper.save_to_csv()
        json_file = scraper.save_to_json()
        
        print(f"\n📁 Files saved:")
        print(f"  CSV: {csv_file}")
        print(f"  JSON: {json_file}")
        
        # Show sample jobs
        print(f"\n📋 Sample jobs found:")
        for i, job in enumerate(scraper.job_postings[:5], 1):
            print(f"\n{i}. {job.get('title', 'N/A')}")
            print(f"   🏢 {job.get('company', 'N/A')}")
            print(f"   📍 {job.get('location', 'N/A')}")
            print(f"   ⏰ {job.get('posted_time_ago', 'N/A')}")
    else:
        print("\n❌ No jobs found. Try different search criteria.")


if __name__ == "__main__":
    asyncio.run(main())