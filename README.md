# LinkedIn Job Scraper 🔍

A comprehensive Python tool to fetch the latest LinkedIn job postings using LinkedIn's public jobs API. This scraper can extract job listings with detailed information including job titles, companies, locations, posting dates, and more - all without requiring authentication.

## ✨ Features

- **No Authentication Required**: Uses LinkedIn's public jobs API
- **Advanced Search Filters**: Filter by job type, experience level, location, and remote work
- **Multiple Export Formats**: Save results to CSV and JSON
- **Respectful Scraping**: Built-in delays and rate limiting
- **Comprehensive Data**: Extracts job titles, companies, locations, posting dates, applicant counts, and more
- **Error Handling**: Robust error handling with logging
- **Async Operations**: Fast concurrent processing
- **Job Statistics**: Get insights about scraped jobs

## 🚀 Quick Start

### Installation

1. **Clone or download the files:**
```bash
# Save the linkedin_job_scraper.py file to your project directory
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Basic Usage

```python
import asyncio
from linkedin_job_scraper import LinkedInJobScraper

async def main():
    scraper = LinkedInJobScraper()
    
    # Search for jobs
    await scraper.search_jobs(
        keywords="python developer",
        location="United States",
        pages=3,
        remote=True
    )
    
    # Print summary and save results
    scraper.print_summary()
    scraper.save_to_csv()
    scraper.save_to_json()

asyncio.run(main())
```

### Run the Example

```bash
python linkedin_job_scraper.py
```

This will search for various job types and save the results to timestamped CSV and JSON files.

## 📊 Sample Output

```
==================================================
LINKEDIN JOBS SCRAPING SUMMARY
==================================================
Total Jobs Found: 175
Unique Companies: 98
Promoted Jobs: 12

Top Companies:
  • Google: 8 jobs
  • Microsoft: 6 jobs
  • Amazon: 5 jobs
  • Meta: 4 jobs
  • Apple: 3 jobs

Top Locations:
  • United States: 45 jobs
  • Remote: 32 jobs
  • San Francisco, CA: 18 jobs
  • New York, NY: 15 jobs
  • Seattle, WA: 12 jobs
==================================================
```

## 🔧 Configuration Options

### Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `keywords` | str | Job search keywords | "python developer", "data scientist" |
| `location` | str | Job location | "United States", "New York, NY", "Remote" |
| `pages` | int | Number of pages to scrape (25 jobs per page) | 3 |
| `job_type` | str | Job type filter | "full-time", "part-time", "contract", "internship" |
| `experience_level` | str | Experience level | "entry", "mid", "senior", "executive" |
| `remote` | bool | Filter for remote jobs | True/False |

### Example Searches

```python
# Search for remote Python jobs
await scraper.search_jobs(
    keywords="python developer",
    location="Remote",
    pages=2,
    job_type="full-time",
    remote=True
)

# Search for entry-level data science jobs
await scraper.search_jobs(
    keywords="data scientist",
    location="San Francisco, CA",
    pages=3,
    experience_level="entry"
)

# Search for contract work
await scraper.search_jobs(
    keywords="freelance developer",
    location="United States",
    pages=2,
    job_type="contract"
)
```

## 📁 Output Files

The scraper automatically saves results with timestamps:

- **CSV Format**: `linkedin_jobs_20240115_143025.csv`
- **JSON Format**: `linkedin_jobs_20240115_143025.json`
- **Log File**: `linkedin_scraper.log`

### Sample CSV Output

```csv
job_id,title,company,location,job_url,posted_date,posted_time_ago,applicants,is_promoted,search_keywords,search_location,scraped_at
4172359372,Machine Learning Engineer,Netflix,Los Angeles CA,https://linkedin.com/jobs/view/...,2024-01-15,2 days ago,25+ applicants,False,python developer,United States,2024-01-15T14:30:25
```

## 🎯 Advanced Usage Examples

### Multiple Location Search

```python
async def search_multiple_cities():
    scraper = LinkedInJobScraper()
    
    cities = ["New York, NY", "San Francisco, CA", "Seattle, WA", "Austin, TX"]
    
    for city in cities:
        await scraper.search_jobs(
            keywords="software engineer",
            location=city,
            pages=2
        )
        await asyncio.sleep(2)  # Be respectful
    
    return scraper
```

### Trending Keywords Search

```python
async def search_trending_roles():
    scraper = LinkedInJobScraper()
    
    trending_keywords = [
        "machine learning engineer",
        "devops engineer", 
        "cybersecurity analyst",
        "cloud architect"
    ]
    
    for keyword in trending_keywords:
        await scraper.search_jobs(
            keywords=keyword,
            location="United States",
            pages=1
        )
    
    return scraper
```

### Job Market Analysis

```python
# Get statistics about scraped jobs
stats = scraper.get_job_stats()
print(f"Total jobs: {stats['total_jobs']}")
print(f"Top companies: {stats['top_companies']}")
print(f"Top locations: {stats['top_locations']}")
```

## 📋 Data Fields

Each job posting includes the following fields:

| Field | Description |
|-------|-------------|
| `job_id` | Unique LinkedIn job identifier |
| `title` | Job title |
| `company` | Company name |
| `location` | Job location |
| `job_url` | Direct link to LinkedIn job posting |
| `posted_date` | ISO date when job was posted |
| `posted_time_ago` | Human-readable posting time |
| `applicants` | Number of applicants (if available) |
| `is_promoted` | Whether the job is promoted/sponsored |
| `search_keywords` | Keywords used in search |
| `search_location` | Location used in search |
| `scraped_at` | Timestamp when data was scraped |

## ⚙️ Technical Details

### Rate Limiting
- Built-in 2-second delays between requests
- Respectful to LinkedIn's servers
- Configurable timeout settings

### Error Handling
- Comprehensive logging to `linkedin_scraper.log`
- Graceful handling of network errors
- Continues scraping even if individual pages fail

### Data Validation
- Filters out invalid job postings
- Handles missing fields gracefully
- Ensures data quality

## 🛠️ Troubleshooting

### Common Issues

1. **No jobs found**: Try different keywords or locations
2. **HTTP errors**: LinkedIn may be rate limiting - increase delays
3. **Missing data**: Some job fields may not be available for all postings

### Debug Mode
Enable debug logging to see detailed information:

```python
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

## 📊 Use Cases

This scraper is perfect for:

- **Job Market Research**: Analyze hiring trends and salary patterns
- **Career Planning**: Find opportunities in your field
- **Recruitment Intelligence**: Track competitor hiring
- **Data Analysis**: Build datasets for ML/analytics projects
- **Job Alerts**: Monitor new postings in your area of interest

## ⚖️ Legal and Ethical Usage

- Uses only publicly available LinkedIn job data
- Implements respectful scraping practices
- Includes appropriate delays between requests
- Does not require authentication or personal data access

**Important**: This tool is for educational and research purposes. Please respect LinkedIn's terms of service and use responsibly.

## 🔗 Dependencies

- `httpx`: Async HTTP client for making requests
- `beautifulsoup4`: HTML parsing and data extraction
- `lxml`: Fast XML/HTML parser

## 🤝 Contributing

Feel free to contribute improvements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

---

**Happy job hunting! 🎉**

For questions or issues, please refer to the error logs or create an issue in the repository.