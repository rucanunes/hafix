import os
import psutil
import logging

logger = logging.getLogger("ha_diagnostics.system_health")

class SystemHealthChecker:
    def check_health(self):
        """Check system health metrics and identify potential issues."""
        health_data = {
            "memory": self._check_memory(),
            "disk": self._check_disk(),
            "cpu": self._check_cpu(),
            "issues": []
        }
        
        # Analyze metrics for potential issues
        self._analyze_metrics(health_data)
        
        return health_data
    
    def _check_memory(self):
        """Check memory usage and identify potential issues."""
        try:
            memory = psutil.virtual_memory()
            return {
                "total": memory.total,
                "available": memory.available,
                "percent": memory.percent,
                "used": memory.used
            }
        except Exception as e:
            logger.error(f"Error checking memory: {str(e)}")
            return {"error": "Unable to read memory info"}

    def _check_disk(self):
        """Check disk usage and identify potential issues."""
        try:
            disk = psutil.disk_usage("/")
            return {
                "total": disk.total,
                "free": disk.free,
                "used": disk.used,
                "percent": disk.percent
            }
        except Exception as e:
            logger.error(f"Error checking disk: {str(e)}")
            return {"error": "Unable to read disk info"}

    def _check_cpu(self):
        """Check CPU usage and identify potential issues."""
        try:
            return {
                "percent": psutil.cpu_percent(interval=1),
                "load_avg": os.getloadavg()
            }
        except Exception as e:
            logger.error(f"Error checking CPU: {str(e)}")
            return {"error": "Unable to read CPU info"}

    def _analyze_metrics(self, health_data):
        """Analyze collected metrics and identify potential issues."""
        issues = health_data["issues"]
        
        # Check memory usage
        if "percent" in health_data["memory"]:
            if health_data["memory"]["percent"] > 90:
                issues.append({
                    "type": "memory",
                    "severity": "critical",
                    "message": "Memory usage is critically high",
                    "details": "System is using more than 90% of available memory"
                })
            elif health_data["memory"]["percent"] > 80:
                issues.append({
                    "type": "memory",
                    "severity": "warning",
                    "message": "Memory usage is high",
                    "details": "System is using more than 80% of available memory"
                })

        # Check disk usage
        if "percent" in health_data["disk"]:
            if health_data["disk"]["percent"] > 90:
                issues.append({
                    "type": "disk",
                    "severity": "critical",
                    "message": "Disk space is critically low",
                    "details": "Less than 10% disk space remaining"
                })
            elif health_data["disk"]["percent"] > 80:
                issues.append({
                    "type": "disk",
                    "severity": "warning",
                    "message": "Disk space is running low",
                    "details": "Less than 20% disk space remaining"
                })

        # Check CPU usage
        if "percent" in health_data["cpu"]:
            if health_data["cpu"]["percent"] > 90:
                issues.append({
                    "type": "cpu",
                    "severity": "critical",
                    "message": "CPU usage is critically high",
                    "details": "CPU usage is above 90%"
                })
            elif health_data["cpu"]["percent"] > 80:
                issues.append({
                    "type": "cpu",
                    "severity": "warning",
                    "message": "CPU usage is high",
                    "details": "CPU usage is above 80%"
                })
