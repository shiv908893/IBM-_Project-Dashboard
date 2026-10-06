from __future__ import annotations

import json
from typing import Any


class AIAnalyst:
    """Produce verified executive language from Python-calculated metrics and structured business intelligence."""

    @staticmethod
    def validate_response(payload: dict[str, Any]) -> bool:
        required = ["executive_summary", "key_findings", "risks", "opportunities", "recommended_actions"]
        if not isinstance(payload, dict):
            return False
        if not all(key in payload for key in required):
            return False
        for key in required:
            if key not in payload:
                return False
            if key in ["key_findings", "risks", "opportunities", "recommended_actions"] and not isinstance(payload[key], list):
                return False
        return True

    @staticmethod
    def generate(*args) -> dict[str, Any]:
        if len(args) == 3:
            metrics, risks, opportunities = args
        elif len(args) == 6:
            metrics, _, _, _, risks, opportunities = args
        else:
            raise TypeError("AIAnalyst.generate expects either (metrics, risks, opportunities) or (metrics, segments, churn, forecast, risks, opportunities).")

        revenue = metrics.get("revenue", 0)
        profit = metrics.get("profit", 0)
        growth = metrics.get("growth_pct", 0)
        top_category = metrics.get("top_category", "N/A")
        top_region = metrics.get("top_region", "N/A")

        risk_items = risks or []
        opportunity_items = opportunities or []

        summary = (
            f"FACT: Revenue is ${revenue:,.2f} with profit of ${profit:,.2f}. "
            f"INSIGHT: Growth is {growth:.2f}% and the strongest revenue contribution comes from {top_category} in {top_region}. "
            f"OPPORTUNITY: Additional investment should focus on the highest-contributing category and region while containing the most material operating risks. "
            f"ACTION: Prioritize targeted commercial actions on the highest-return segments and retention programs for at-risk customers."
        )

        key_findings = [
            f"FACT: Revenue totals ${revenue:,.2f} and top category is {top_category}.",
            f"INSIGHT: Profit stands at ${profit:,.2f} with a growth rate of {growth:.2f}% compared with the previous period.",
            f"OPPORTUNITY: {top_region} is the strongest region for customer demand and expansion investment.",
            f"ACTION: Focus actions on the category and customer segments that maximize margin and retention.",
        ]

        risk_lines = [
            f"RISK: {risk['title']} — {risk['evidence']}"
            for risk in risk_items[:3]
        ]
        opportunity_lines = [
            f"OPPORTUNITY: {opp['title']} — {opp['evidence']}"
            for opp in opportunity_items[:3]
        ]
        actions = [
            "ACTION: Launch a targeted retention campaign for high-risk customers.",
            "ACTION: Increase investment in the top growth category and region with a defined ROI review.",
            "ACTION: Tighten pricing or discount control for low-margin categories.",
            "ACTION: Prioritize customer reactivation and loyalty offers for inactive segments.",
            "ACTION: Review demand signals and operational capacity before expanding inventory.",
        ]

        payload = {
            "executive_summary": summary,
            "key_findings": key_findings,
            "risks": risk_lines,
            "opportunities": opportunity_lines,
            "recommended_actions": actions,
        }
        if not AIAnalyst.validate_response(payload):
            raise ValueError("Malformed AI executive response generated.")
        return payload
