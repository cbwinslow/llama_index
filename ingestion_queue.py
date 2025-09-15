#!/usr/bin/env python3
"""
Ingestion Queue Script for Political Document Analysis System
This script demonstrates how to queue up ingestion runs for later processing.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

def create_ingestion_job(sources, job_name=None, priority="normal"):
    """
    Create an ingestion job configuration file for later processing
    
    Args:
        sources: Dictionary of sources to ingest
        job_name: Name for the job (optional)
        priority: Priority level (low, normal, high)
        
    Returns:
        Path to the job file
    """
    # Create jobs directory
    jobs_dir = Path("./ingestion_jobs")
    jobs_dir.mkdir(exist_ok=True)
    
    # Generate job name if not provided
    if not job_name:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        job_name = f"ingestion_job_{timestamp}"
    
    # Create job file
    job_file = jobs_dir / f"{job_name}.json"
    
    # Create job configuration
    job_config = {
        "job_name": job_name,
        "created_at": datetime.now().isoformat(),
        "priority": priority,
        "sources": sources,
        "status": "pending"
    }
    
    # Save job configuration
    with open(job_file, 'w') as f:
        json.dump(job_config, f, indent=2)
    
    print(f"✅ Ingestion job '{job_name}' created and saved to {job_file}")
    return job_file

def list_pending_jobs():
    """List all pending ingestion jobs"""
    jobs_dir = Path("./ingestion_jobs")
    if not jobs_dir.exists():
        print("No ingestion jobs directory found.")
        return []
    
    job_files = list(jobs_dir.glob("*.json"))
    if not job_files:
        print("No pending ingestion jobs found.")
        return []
    
    print("Pending ingestion jobs:")
    pending_jobs = []
    for job_file in job_files:
        try:
            with open(job_file, 'r') as f:
                job_config = json.load(f)
            if job_config.get("status") == "pending":
                pending_jobs.append(job_file)
                print(f"  - {job_file.name} (priority: {job_config.get('priority', 'normal')})")
        except Exception as e:
            print(f"  - {job_file.name} (error reading: {e})")
    
    return pending_jobs

def process_next_job():
    """Process the next pending ingestion job"""
    pending_jobs = list_pending_jobs()
    if not pending_jobs:
        print("No pending jobs to process.")
        return
    
    # For simplicity, process the first job
    job_file = pending_jobs[0]
    
    print(f"Processing job: {job_file.name}")
    
    try:
        # Load job configuration
        with open(job_file, 'r') as f:
            job_config = json.load(f)
        
        # Update status to processing
        job_config["status"] = "processing"
        job_config["started_at"] = datetime.now().isoformat()
        with open(job_file, 'w') as f:
            json.dump(job_config, f, indent=2)
        
        print("Job status updated to 'processing'")
        
        # Here you would normally run the actual ingestion
        # For this demo, we'll just simulate it
        print("Running ingestion...")
        print(f"Sources to process: {job_config['sources']}")
        
        # Simulate processing time
        import time
        time.sleep(2)
        
        # Update status to completed
        job_config["status"] = "completed"
        job_config["completed_at"] = datetime.now().isoformat()
        with open(job_file, 'w') as f:
            json.dump(job_config, f, indent=2)
        
        print("✅ Job completed successfully!")
        
    except Exception as e:
        print(f"❌ Error processing job: {e}")
        # Update status to failed
        try:
            job_config["status"] = "failed"
            job_config["error"] = str(e)
            job_config["failed_at"] = datetime.now().isoformat()
            with open(job_file, 'w') as f:
                json.dump(job_config, f, indent=2)
        except:
            pass

def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python ingestion_queue.py create [job_name]  # Create a new ingestion job")
        print("  python ingestion_queue.py list              # List pending jobs")
        print("  python ingestion_queue.py process           # Process next pending job")
        return
    
    command = sys.argv[1]
    
    if command == "create":
        # Create a sample job
        sample_sources = {
            "local_directories": ["./data/sample_docs"],
            # Uncomment when web readers are available:
            # "websites": ["https://www.congress.gov/"],
            # "rss_feeds": ["https://feeds.reuters.com/Reuters/PoliticsNews"]
        }
        
        job_name = sys.argv[2] if len(sys.argv) > 2 else None
        create_ingestion_job(sample_sources, job_name)
        
    elif command == "list":
        list_pending_jobs()
        
    elif command == "process":
        process_next_job()
        
    else:
        print(f"Unknown command: {command}")
        print("Available commands: create, list, process")

if __name__ == "__main__":
    main()