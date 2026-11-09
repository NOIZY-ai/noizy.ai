#!/usr/bin/env python3
"""
PREDICTIVE ANALYTICS - AI-Powered Volume Usage Forecasting
ML-based prediction of volume capacity and growth patterns
"""

import json
import statistics
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict

class PredictiveAnalytics:
    """AI-powered predictive analytics for volume management"""
    
    def __init__(self):
        self.history_file = Path(__file__).parent / "volume_history.json"
        self.history = self._load_history()
    
    def _load_history(self) -> Dict:
        """Load historical volume data"""
        if self.history_file.exists():
            try:
                with open(self.history_file, "r") as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _save_history(self):
        """Save historical volume data"""
        with open(self.history_file, "w") as f:
            json.dump(self.history, f, indent=2)
    
    def record_volume_state(self, volume_name: str, usage_percent: int, size_bytes: int = 0):
        """Record current volume state for history"""
        timestamp = datetime.now().isoformat()
        
        if volume_name not in self.history:
            self.history[volume_name] = []
        
        self.history[volume_name].append({
            "timestamp": timestamp,
            "usage_percent": usage_percent,
            "size_bytes": size_bytes
        })
        
        # Keep only last 30 days of history
        cutoff = (datetime.now() - timedelta(days=30)).isoformat()
        self.history[volume_name] = [
            entry for entry in self.history[volume_name]
            if entry["timestamp"] >= cutoff
        ]
        
        self._save_history()
    
    def predict_fill_date(self, volume_name: str, target_percent: int = 100) -> Optional[Dict]:
        """Predict when volume will reach target percent"""
        if volume_name not in self.history or len(self.history[volume_name]) < 2:
            return None
        
        history = self.history[volume_name]
        
        # Calculate growth rate
        usage_points = [entry["usage_percent"] for entry in history]
        if len(usage_points) < 2:
            return None
        
        # Simple linear regression
        days = list(range(len(usage_points)))
        if len(days) < 2:
            return None
        
        # Calculate slope (growth per day)
        n = len(days)
        sum_x = sum(days)
        sum_y = sum(usage_points)
        sum_xy = sum(x * y for x, y in zip(days, usage_points))
        sum_x2 = sum(x * x for x in days)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x) if (n * sum_x2 - sum_x * sum_x) != 0 else 0
        current_usage = usage_points[-1]
        
        if slope <= 0:
            return {
                "volume": volume_name,
                "prediction": "No growth detected - volume usage stable or decreasing",
                "current_usage": current_usage,
                "target_percent": target_percent,
                "growth_rate_per_day": slope
            }
        
        # Predict days until target
        days_until_target = (target_percent - current_usage) / slope if slope > 0 else None
        
        if days_until_target and days_until_target > 0:
            predicted_date = datetime.now() + timedelta(days=int(days_until_target))
            return {
                "volume": volume_name,
                "current_usage": current_usage,
                "target_percent": target_percent,
                "predicted_fill_date": predicted_date.isoformat(),
                "days_until_full": int(days_until_target),
                "growth_rate_per_day": round(slope, 3),
                "confidence": "MEDIUM" if len(history) >= 7 else "LOW"
            }
        
        return None
    
    def predict_critical_volumes(self, volumes: Dict) -> List[Dict]:
        """Predict which volumes will become critical soon"""
        predictions = []
        
        for vol_name, vol_info in volumes.items():
            usage = vol_info.get("percent", 0)
            
            # Record current state
            self.record_volume_state(vol_name, usage)
            
            # Predict if will hit 95% in next 30 days
            prediction = self.predict_fill_date(vol_name, 95)
            if prediction and prediction.get("days_until_full"):
                if prediction["days_until_full"] <= 30:
                    predictions.append({
                        "volume": vol_name,
                        "current_usage": usage,
                        "predicted_critical_date": prediction["predicted_fill_date"],
                        "days_until_critical": prediction["days_until_full"],
                        "growth_rate": prediction["growth_rate_per_day"],
                        "urgency": "HIGH" if prediction["days_until_full"] <= 7 else "MEDIUM"
                    })
        
        return sorted(predictions, key=lambda x: x["days_until_critical"])
    
    def generate_predictions_report(self, volumes: Dict) -> str:
        """Generate predictive analytics report"""
        predictions = self.predict_critical_volumes(volumes)
        
        report = []
        report.append("╔══════════════════════════════════════════════════════════════╗")
        report.append("║         PREDICTIVE ANALYTICS REPORT                         ║")
        report.append("╚══════════════════════════════════════════════════════════════╝")
        report.append(f"\n📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        if predictions:
            report.append(f"⚠️  PREDICTED CRITICAL VOLUMES (Next 30 Days): {len(predictions)}\n")
            report.append("─" * 70)
            
            for pred in predictions:
                report.append(f"\n📁 Volume: {pred['volume']}")
                report.append(f"   Current Usage: {pred['current_usage']}%")
                report.append(f"   Predicted Critical Date: {pred['predicted_critical_date'][:10]}")
                report.append(f"   Days Until Critical: {pred['days_until_critical']}")
                report.append(f"   Growth Rate: {pred['growth_rate']}% per day")
                report.append(f"   Urgency: {pred['urgency']}")
        else:
            report.append("✅ No volumes predicted to become critical in the next 30 days")
        
        report.append("")
        return "\n".join(report)

def main():
    """Main analytics function"""
    analytics = PredictiveAnalytics()
    
    # Get current volumes
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from volume_monitor_UPGRADED import VolumeMonitorUpgraded
        
        monitor = VolumeMonitorUpgraded()
        monitor.scan_volumes()
        
        print("🔮 Running predictive analytics...")
        report = analytics.generate_predictions_report(monitor.volumes)
        print("\n" + report)
        
        # Save report
        report_path = Path(__file__).parent / "predictive_analytics_report.md"
        with open(report_path, "w") as f:
            f.write(report)
        print(f"📊 Report saved to: {report_path}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    main()

