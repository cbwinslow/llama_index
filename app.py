#!/usr/bin/env python3
"""
Main entry point for the LlamaIndex Political Document Manager application.

This script provides a command-line interface to start and manage the application,
including the web interface, MCP server, and background document processing.
"""
import argparse
import asyncio
import logging
import sys
from pathlib import Path
from typing import Optional

# Import our components
from llama_political_manager.config_manager import ConfigurationManager
from llama_political_manager.mcp_server import PoliticalDocumentMCPServer
from llama_political_manager.web_interface import WebInterface

def setup_logging(log_level: str = "INFO"):
    """Setup application logging."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('app.log')
        ]
    )

def create_sample_data(data_dir: Path):
    """Create sample political documents for testing."""
    data_dir.mkdir(exist_ok=True)
    
    # Sample political documents
    samples = [
        {
            "filename": "healthcare_reform_2024.txt",
            "content": """
Healthcare Reform Act of 2024

This comprehensive healthcare reform legislation aims to:
- Expand access to affordable healthcare for all Americans
- Reduce prescription drug costs through Medicare negotiation
- Strengthen the Affordable Care Act marketplace
- Invest in rural healthcare infrastructure
- Support mental health and substance abuse treatment

Key provisions include:
1. Public option for health insurance
2. Lowering Medicare eligibility age to 60
3. Dental and vision coverage for Medicare beneficiaries
4. Price transparency requirements for hospitals
5. Investment in community health centers

This bill represents a significant step toward ensuring healthcare
is a right, not a privilege, for every American.
            """
        },
        {
            "filename": "climate_action_plan.txt", 
            "content": """
National Climate Action Plan

Executive Summary:
The United States commits to achieving net-zero greenhouse gas emissions
by 2050 through comprehensive climate action across all sectors.

Key Strategies:
- Transition to 100% clean electricity by 2035
- Electrify transportation sector with EV infrastructure
- Retrofit buildings for energy efficiency
- Protect and restore natural ecosystems
- Support climate resilience in communities
- Create millions of good-paying clean energy jobs

Investment Priorities:
1. $500 billion for clean energy infrastructure
2. $200 billion for electric vehicle charging network
3. $150 billion for building retrofits and upgrades
4. $100 billion for climate resilience projects
5. $75 billion for environmental justice initiatives

This plan positions America as a global leader in the fight
against climate change while creating economic opportunities.
            """
        },
        {
            "filename": "economic_recovery_bill.txt",
            "content": """
American Economic Recovery and Resilience Act

Purpose:
To strengthen the U.S. economy, create jobs, and build resilience
against future economic shocks through strategic investments.

Core Components:
- Infrastructure modernization ($1.2 trillion over 10 years)
- Workforce development and skills training
- Small business support and entrepreneurship
- Manufacturing and supply chain resilience
- Technology innovation and research

Employment Provisions:
1. Direct job creation in infrastructure projects
2. Apprenticeship programs for skilled trades
3. Retraining programs for displaced workers
4. Support for union organizing and collective bargaining
5. Minimum wage increase to $15 per hour

Economic Impact:
- Projected to create 15 million jobs over 10 years
- GDP growth of 2-3% annually
- Reduced wealth inequality through targeted investments
- Enhanced competitiveness in global markets

This legislation represents the largest public investment
in the American economy since the New Deal.
            """
        }
    ]
    
    for sample in samples:
        doc_path = data_dir / sample["filename"]
        doc_path.write_text(sample["content"].strip())
    
    print(f"Created {len(samples)} sample documents in {data_dir}")

async def start_mcp_server(config_manager: ConfigurationManager, 
                          host: str = "localhost", port: int = 8080):
    """Start the MCP server."""
    mcp_server = PoliticalDocumentMCPServer(config_manager=config_manager)
    await mcp_server.start(host, port)
    return mcp_server

def start_web_interface(config_manager: ConfigurationManager,
                       host: str = "localhost", port: int = 8000, debug: bool = False):
    """Start the web interface."""
    web_app = WebInterface(config_manager=config_manager)
    web_app.run(host, port, debug)
    return web_app

def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(description="LlamaIndex Political Document Manager")
    parser.add_argument("--config-dir", type=str, default="./config",
                       help="Configuration directory (default: ./config)")
    parser.add_argument("--data-dir", type=str, default="./data",
                       help="Data directory for documents (default: ./data)")
    parser.add_argument("--log-level", type=str, default="INFO",
                       choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                       help="Logging level (default: INFO)")
    parser.add_argument("--create-sample-data", action="store_true",
                       help="Create sample political documents")
    parser.add_argument("--web-host", type=str, default="localhost",
                       help="Web interface host (default: localhost)")
    parser.add_argument("--web-port", type=int, default=8000,
                       help="Web interface port (default: 8000)")
    parser.add_argument("--mcp-host", type=str, default="localhost",
                       help="MCP server host (default: localhost)")
    parser.add_argument("--mcp-port", type=int, default=8080,
                       help="MCP server port (default: 8080)")
    parser.add_argument("--web-only", action="store_true",
                       help="Start only the web interface")
    parser.add_argument("--mcp-only", action="store_true",
                       help="Start only the MCP server")
    parser.add_argument("--debug", action="store_true",
                       help="Enable debug mode")
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    # Create directories
    config_dir = Path(args.config_dir)
    data_dir = Path(args.data_dir)
    config_dir.mkdir(exist_ok=True)
    data_dir.mkdir(exist_ok=True)
    
    # Create sample data if requested
    if args.create_sample_data:
        create_sample_data(data_dir)
    
    # Initialize configuration manager
    config_manager = ConfigurationManager(config_dir)
    
    # Update configuration with command line arguments
    deployment_updates = {
        "host": args.web_host,
        "port": args.web_port,
        "debug": args.debug,
        "log_level": args.log_level
    }
    config_manager.update_config("deployment", deployment_updates)
    
    logger.info("Starting LlamaIndex Political Document Manager")
    logger.info(f"Configuration directory: {config_dir}")
    logger.info(f"Data directory: {data_dir}")
    
    async def run_application():
        """Run the complete application."""
        tasks = []
        
        if not args.web_only:
            # Start MCP server
            logger.info(f"Starting MCP server on {args.mcp_host}:{args.mcp_port}")
            mcp_server = await start_mcp_server(config_manager, args.mcp_host, args.mcp_port)
            
            # Keep MCP server running
            async def keep_mcp_running():
                while mcp_server.is_running:
                    await asyncio.sleep(1)
            
            tasks.append(keep_mcp_running())
        
        if not args.mcp_only:
            # Start web interface
            logger.info(f"Starting web interface on {args.web_host}:{args.web_port}")
            web_app = start_web_interface(config_manager, args.web_host, args.web_port, args.debug)
            
            # In a real implementation, this would be an async web server
            async def keep_web_running():
                logger.info("Web interface is running (mock implementation)")
                while True:
                    await asyncio.sleep(10)
                    logger.debug("Web interface heartbeat")
            
            tasks.append(keep_web_running())
        
        if tasks:
            # Run all tasks concurrently
            await asyncio.gather(*tasks)
        else:
            logger.error("No services selected to run")
    
    try:
        if args.web_only and not args.mcp_only:
            # Synchronous web interface only
            web_app = start_web_interface(config_manager, args.web_host, args.web_port, args.debug)
            logger.info("Web interface started (press Ctrl+C to stop)")
            try:
                while True:
                    import time
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Shutting down web interface")
        else:
            # Run async services
            asyncio.run(run_application())
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()