"""
Unit Test Suite for NexusAgent
"""

import unittest
import os
import sys

# Ensure root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.tools import safe_calculator, web_search, document_analyzer, report_synthesizer, get_default_registry
from core.memory import AgentMemory
from core.agent import NexusAgent, AgentConfig

class TestNexusAgentTools(unittest.TestCase):
    def test_calculator_basic(self):
        res = safe_calculator("100 + 50")
        self.assertIn("150", res)

    def test_calculator_disallowed_tokens(self):
        res = safe_calculator("__import__('os').system('dir')")
        self.assertIn("Error", res)

    def test_web_search(self):
        res = web_search("quantum computing")
        self.assertTrue(len(res) > 20)
        self.assertIn("quantum", res.lower())

    def test_document_analyzer(self):
        sample = "The market expanded by 34.5% reaching $10.2B in overall valuation."
        res = document_analyzer(sample)
        self.assertIn("34.5%", res)
        self.assertIn("$10.2B", res)

    def test_report_synthesizer(self):
        res = report_synthesizer(
            title="Test Intelligence Report",
            executive_summary="Summary of test findings.",
            sections_json='[{"heading": "Section 1", "content": "Detailed text."}]',
            recommendations_json='["Action 1", "Action 2"]'
        )
        self.assertIn("# Test Intelligence Report", res)
        self.assertIn("## Executive Summary", res)
        self.assertIn("Action 1", res)

class TestNexusAgentMemory(unittest.TestCase):
    def test_memory_scratchpad(self):
        mem = AgentMemory(goal="Investigate battery advances")
        mem.record_step(
            thought="Search web",
            tool_name="web_search",
            tool_input={"query": "battery"},
            observation="Obs 1",
            reflection="Ref 1"
        )
        scratchpad = mem.format_scratchpad()
        self.assertIn("Step 1:", scratchpad)
        self.assertIn("Action: web_search", scratchpad)
        self.assertIn("Ref 1", scratchpad)

class TestNexusAgentExecution(unittest.TestCase):
    def test_agent_simulation_run(self):
        config = AgentConfig(max_steps=2, mode="simulation")
        agent = NexusAgent(config=config)
        resp = agent.run("Explore AI agent evaluation benchmarks")
        
        self.assertEqual(len(resp.steps), 2)
        self.assertIn("Intelligence Brief", resp.final_report)
        self.assertIn("Executive Summary", resp.final_report)
        self.assertGreater(resp.duration_seconds, 0)
        self.assertEqual(resp.mode_used, "Autonomous Simulation Engine")

if __name__ == "__main__":
    unittest.main()
