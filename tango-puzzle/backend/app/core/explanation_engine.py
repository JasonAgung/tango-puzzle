"""
Explanation engine for Tango puzzle
Generates human-readable explanations for solving steps
"""
from typing import List, Dict, Optional, Tuple
from app.api.models.solution import ExplanationStep


class ExplanationEngine:
    """Generates detailed explanations for puzzle solving steps"""
    
    def __init__(self):
        self.explanation_templates = {
            "row_count": {
                "title": "Row Count Rule",
                "template": "Row {row} already has {count} {symbol}s, so the remaining cells must be {opposite}s.",
                "hint": "Count the symbols in each row. Each row needs exactly 3 suns and 3 moons."
            },
            "column_count": {
                "title": "Column Count Rule",
                "template": "Column {col} already has {count} {symbol}s, so the remaining cells must be {opposite}s.",
                "hint": "Count the symbols in each column. Each column needs exactly 3 suns and 3 moons."
            },
            "consecutive_prevention": {
                "title": "No Three Consecutive Rule",
                "template": "Placing a {symbol} at ({row}, {col}) would create three consecutive {symbol}s, so it must be a {opposite}.",
                "hint": "Look for patterns where placing a symbol would create three in a row."
            },
            "equal_constraint": {
                "title": "Equal Constraint Rule",
                "template": "Cell ({row}, {col}) must be {value} because it has an equal constraint with cell ({ref_row}, {ref_col}) which is {value}.",
                "hint": "Cells connected by '=' must have the same symbol."
            },
            "opposite_constraint": {
                "title": "Opposite Constraint Rule",
                "template": "Cell ({row}, {col}) must be {value} because it has an opposite constraint with cell ({ref_row}, {ref_col}) which is {opposite}.",
                "hint": "Cells connected by '×' must have opposite symbols."
            },
            "advanced_deduction": {
                "title": "Advanced Deduction",
                "template": "Through constraint propagation and elimination, cell ({row}, {col}) must be {value}.",
                "hint": "Sometimes you need to consider multiple constraints together."
            }
        }
    
    def generate_step_explanation(self, step: Dict) -> Dict:
        """Generate detailed explanation for a single step"""
        rule = step.get("rule_applied", "unknown")
        template_info = self.explanation_templates.get(rule, {})
        
        # Create detailed explanation
        detailed_explanation = self._create_detailed_explanation(step, template_info)
        
        # Add visual hints
        visual_hints = self._generate_visual_hints(step)
        
        return {
            "step_number": step.get("step_number", 0),
            "row": step["row"],
            "col": step["col"],
            "value": step["value"],
            "rule_applied": rule,
            "rule_title": template_info.get("title", "Unknown Rule"),
            "explanation": step["explanation"],
            "detailed_explanation": detailed_explanation,
            "hint": template_info.get("hint", ""),
            "visual_hints": visual_hints
        }
    
    def _create_detailed_explanation(self, step: Dict, template_info: Dict) -> str:
        """Create a detailed explanation based on the rule applied"""
        rule = step.get("rule_applied", "")
        
        if rule == "row_count":
            return self._explain_row_count(step)
        elif rule == "column_count":
            return self._explain_column_count(step)
        elif rule == "consecutive_prevention":
            return self._explain_consecutive_prevention(step)
        elif rule in ["equal_constraint", "opposite_constraint"]:
            return self._explain_constraint(step)
        else:
            return step.get("explanation", "")
    
    def _explain_row_count(self, step: Dict) -> str:
        """Detailed explanation for row count rule"""
        row = step["row"]
        value = step["value"]
        opposite = "sun" if value == "moon" else "moon"
        
        explanation = f"Let's look at row {row}:\n"
        explanation += f"- Each row must have exactly 3 suns and 3 moons\n"
        explanation += f"- This row already has 3 {opposite}s\n"
        explanation += f"- Therefore, all remaining empty cells must be {value}s\n"
        explanation += f"- Cell ({row}, {step['col']}) is empty, so it must be a {value}"
        
        return explanation
    
    def _explain_column_count(self, step: Dict) -> str:
        """Detailed explanation for column count rule"""
        col = step["col"]
        value = step["value"]
        opposite = "sun" if value == "moon" else "moon"
        
        explanation = f"Let's look at column {col}:\n"
        explanation += f"- Each column must have exactly 3 suns and 3 moons\n"
        explanation += f"- This column already has 3 {opposite}s\n"
        explanation += f"- Therefore, all remaining empty cells must be {value}s\n"
        explanation += f"- Cell ({step['row']}, {col}) is empty, so it must be a {value}"
        
        return explanation
    
    def _explain_consecutive_prevention(self, step: Dict) -> str:
        """Detailed explanation for consecutive prevention rule"""
        row, col = step["row"], step["col"]
        value = step["value"]
        opposite = "sun" if value == "moon" else "moon"
        
        explanation = f"Looking at position ({row}, {col}):\n"
        explanation += f"- No more than 2 consecutive symbols are allowed\n"
        explanation += f"- If we place a {opposite} here, it would create 3 consecutive {opposite}s\n"
        explanation += f"- Therefore, this cell must be a {value}"
        
        return explanation
    
    def _explain_constraint(self, step: Dict) -> str:
        """Detailed explanation for equal/opposite constraints"""
        rule = step.get("rule_applied", "")
        
        if rule == "equal_constraint":
            explanation = "Equal Constraint (=):\n"
            explanation += "- Two cells connected by '=' must have the same symbol\n"
        else:
            explanation = "Opposite Constraint (×):\n"
            explanation += "- Two cells connected by '×' must have opposite symbols\n"
        
        explanation += step.get("explanation", "")
        
        return explanation
    
    def _generate_visual_hints(self, step: Dict) -> Dict:
        """Generate visual hints for highlighting relevant cells"""
        rule = step.get("rule_applied", "")
        highlighted_cells = []
        highlighted_regions = []
        
        if rule == "row_count":
            # Highlight the entire row
            highlighted_regions.append({
                "type": "row",
                "index": step["row"],
                "color": "info"
            })
        
        elif rule == "column_count":
            # Highlight the entire column
            highlighted_regions.append({
                "type": "column",
                "index": step["col"],
                "color": "info"
            })
        
        elif rule == "consecutive_prevention":
            # Highlight the potential three consecutive cells
            # This would need more context from the step
            highlighted_cells.append({
                "row": step["row"],
                "col": step["col"],
                "color": "warning"
            })
        
        elif rule in ["equal_constraint", "opposite_constraint"]:
            # Highlight both cells involved in the constraint
            # This would need the reference cell from the step
            highlighted_cells.append({
                "row": step["row"],
                "col": step["col"],
                "color": "success"
            })
        
        return {
            "highlighted_cells": highlighted_cells,
            "highlighted_regions": highlighted_regions,
            "target_cell": {
                "row": step["row"],
                "col": step["col"],
                "color": "primary"
            }
        }
    
    def generate_solution_summary(self, steps: List[ExplanationStep]) -> Dict:
        """Generate a summary of the solution process"""
        rule_counts = {}
        for step in steps:
            rule = step.rule_applied
            rule_counts[rule] = rule_counts.get(rule, 0) + 1
        
        # Sort rules by frequency
        sorted_rules = sorted(rule_counts.items(), key=lambda x: x[1], reverse=True)
        
        summary = {
            "total_steps": len(steps),
            "rules_used": [
                {
                    "rule": rule,
                    "title": self.explanation_templates.get(rule, {}).get("title", rule),
                    "count": count,
                    "percentage": (count / len(steps)) * 100
                }
                for rule, count in sorted_rules
            ],
            "difficulty_indicators": self._assess_difficulty_indicators(steps)
        }
        
        return summary
    
    def _assess_difficulty_indicators(self, steps: List[ExplanationStep]) -> List[str]:
        """Assess difficulty based on solving steps"""
        indicators = []
        
        # Check for advanced deductions
        advanced_count = sum(1 for step in steps if step.rule_applied == "advanced_deduction")
        if advanced_count > 2:
            indicators.append("Required multiple advanced deductions")
        
        # Check for long solution
        if len(steps) > 25:
            indicators.append("Long solution path required")
        
        # Check for constraint-heavy solution
        constraint_steps = sum(1 for step in steps 
                             if step.rule_applied in ["equal_constraint", "opposite_constraint"])
        if constraint_steps > len(steps) * 0.3:
            indicators.append("Heavy reliance on constraint rules")
        
        return indicators