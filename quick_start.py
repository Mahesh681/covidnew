#!/usr/bin/env python3
"""
Quick Start - LinkedIn Job Scraper
Run this script to immediately fetch the latest LinkedIn jobs
"""

import asyncio
from linkedin_job_scraper import LinkedInJobScraper


async def quick_start():
    """Quick start function to fetch trending jobs immediately."""
    print("🚀 LinkedIn Job Scraper - Quick Start")
    print("=" * 50)
    print("Fetching the latest trending jobs...\n")
    
    scraper = LinkedInJobScraper()
    
    # Popular job searches
    trending_searches = [
        ("software engineer", "United States", 2),
        ("data scientist", "United States", 2),
        ("python developer", "Remote", 1),
        ("machine learning engineer", "San Francisco, CA", 1),
        ("devops engineer", "New York, NY", 1)
    ]
    
    for keywords, location, pages in trending_searches:
        print(f"🔍 Searching: {keywords} in {location}")
        
        await scraper.search_jobs(
            keywords=keywords,
            location=location,
            pages=pages,
            remote=(location == "Remote")
        )
        
        print(f"✓ Found jobs for '{keywords}'\n")
        await asyncio.sleep(1)  # Be respectful
    
    # Print results
    scraper.print_summary()
    
    # Save files
    csv_file = scraper.save_to_csv()
    json_file = scraper.save_to_json()
    
    print(f"\n📁 Results saved:")
    print(f"   📄 CSV: {csv_file}")
    print(f"   📄 JSON: {json_file}")
    
    # Show recent jobs
    recent_jobs = [job for job in scraper.job_postings 
                   if "hour" in job.get("posted_time_ago", "") or 
                      "day" in job.get("posted_time_ago", "")][:5]
    
    if recent_jobs:
        print(f"\n🕒 Recent Job Postings:")
        for i, job in enumerate(recent_jobs, 1):
            print(f"{i}. {job.get('title', 'N/A')}")
            print(f"   🏢 {job.get('company', 'N/A')}")
            print(f"   📍 {job.get('location', 'N/A')}")
            print(f"   ⏰ {job.get('posted_time_ago', 'N/A')}")
            print()
    
    print("🎉 Done! Check the CSV/JSON files for all job details.")
    return scraper


if __name__ == "__main__":
    asyncio.run(quick_start())