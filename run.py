import os
import sys
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from modules.system_health import SystemHealthChecker
from modules.log_analyzer import LogAnalyzer
from modules.config_checker import ConfigChecker
from modules.solution_engine import SolutionEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ha_diagnostics")

class HADiagnostics:
    def __init__(self):
        self.config = self.load_config()
        self.setup_logging()
        
        # Initialize modules
        self.system_health = SystemHealthChecker()
        self.log_analyzer = LogAnalyzer()
        self.config_checker = ConfigChecker()
        self.solution_engine = SolutionEngine()
        
    def load_config(self):
        """Load the add-on configuration."""
        with open("/data/options.json") as config_file:
            return json.load(config_file)

    def setup_logging(self):
        """Configure logging based on the configuration."""
        log_levels = {
            "trace": logging.DEBUG,
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL
        }
        logger.setLevel(log_levels.get(self.config["log_level"], logging.INFO))

    def collect_diagnostics(self):
        """Collect all diagnostic data and generate solutions."""
        try:
            # Collect data from all modules
            system_health = self.system_health.check_health()
            log_issues = self.log_analyzer.analyze()
            config_issues = self.config_checker.check_all()
            
            # Generate solutions for identified issues
            solutions = self.solution_engine.generate_solutions(
                system_health=system_health,
                log_issues=log_issues,
                config_issues=config_issues
            )
            
            return {
                "timestamp": datetime.now().isoformat(),
                "system_health": system_health,
                "log_analysis": log_issues,
                "config_issues": config_issues,
                "solutions": solutions
            }
        except Exception as e:
            logger.error(f"Error collecting diagnostics: {str(e)}")
            return {"error": str(e)}

    def run(self):
        """Main run loop."""
        logger.info("Starting HA Diagnostics Helper")
        
        while True:
            try:
                # Collect diagnostic data and solutions
                diagnostic_data = self.collect_diagnostics()

                # Save diagnostic data
                with open("/share/ha_diagnostics.json", "w") as f:
                    json.dump(diagnostic_data, f, indent=2)

                logger.info("Diagnostic data collected and solutions generated")
                
                # Wait for next scan interval
                time.sleep(self.config["scan_interval"])
                
            except Exception as e:
                logger.error(f"Error in diagnostic run: {str(e)}")
                time.sleep(60)  # Wait a minute before retrying

if __name__ == "__main__":
    diagnostics = HADiagnostics()
    diagnostics.run()