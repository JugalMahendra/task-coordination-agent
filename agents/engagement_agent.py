import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'mcp_servers', 'analytics_tools'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from analytics_tools import get_engagement_metrics
from seed_demo import FAMILY

def analyze_engagement():
    results = []
    for member in FAMILY["members"]:
        if member["role"] == "child":
            metrics = get_engagement_metrics(member["id"])
            if isinstance(metrics, dict):
                results.append(metrics)
    return results

def get_at_risk_members(threshold=70):
    all_metrics = analyze_engagement()
    return [m for m in all_metrics if m["completion_rate"] < threshold]

def get_top_performers(threshold=90):
    all_metrics = analyze_engagement()
    return [m for m in all_metrics if m["completion_rate"] >= threshold]
