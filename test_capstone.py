import unittest
from unittest.mock import patch

from agent import run_agent
from mcp_client import MCPError
from utils.data_loader import get_example_wardrobe


class TestCapstoneFailureHandling(unittest.TestCase):

    def test_mcp_failure_returns_helpful_error(self):
        with patch("agent.call_tool", side_effect=MCPError("Server unavailable")):
            result = run_agent(
                "vintage graphic tee under $30",
                get_example_wardrobe(),
            )

        self.assertIn("temporarily unavailable", result["error"])
        self.assertIsNone(result["fit_card"])
        self.assertIsNone(result["outfit_suggestion"])

    def test_empty_results_still_work(self):
        with patch("agent.call_tool", return_value=[]):
            result = run_agent(
                "designer ballgown size XXS under $5",
                get_example_wardrobe(),
            )

        self.assertIn("No matching listings", result["error"])
        self.assertIsNone(result["fit_card"])


if __name__ == "__main__":
    unittest.main()
