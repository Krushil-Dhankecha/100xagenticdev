"""Unit tests for build_preset_tasks. Run from pipeline/:

    python3 -m unittest test_task_templates -v
"""

import unittest

from task_templates import PRESETS, build_preset_tasks

# Total tasks across all phases with a large agent count, per the README
# "Available presets" table (Max agents column).
EXPECTED_TOTALS = {
    "crypto_research": 23,
    "market_scan": 20,
    "competitive_intel": 10,
    "sec_audit_recon": 10,
    "code_review": 5,
    "seo_research": 10,
    "domain_research": 5,
    "tech_deep_dive": 10,
    "llm_model_intel": 30,
}


class BuildPresetTasksTests(unittest.TestCase):
    def test_unknown_preset_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            build_preset_tasks("not_a_preset")
        self.assertIn("not_a_preset", str(ctx.exception))

    def test_expected_totals_covers_every_preset(self):
        self.assertEqual(set(EXPECTED_TOTALS), set(PRESETS))

    def test_total_tasks_match_readme_table(self):
        for preset, expected in EXPECTED_TOTALS.items():
            with self.subTest(preset=preset):
                phases = build_preset_tasks(preset, num_agents=100)
                total = sum(len(tasks) for tasks, _ in phases)
                self.assertEqual(total, expected)

    def test_single_agent_first_phase_has_one_task(self):
        for preset in PRESETS:
            with self.subTest(preset=preset):
                phases = build_preset_tasks(preset, num_agents=1)
                first_phase_tasks, _ = phases[0]
                self.assertEqual(len(first_phase_tasks), 1)

    def test_task_ids_unique_within_preset(self):
        for preset in PRESETS:
            with self.subTest(preset=preset):
                phases = build_preset_tasks(preset, num_agents=100)
                task_ids = [
                    task.task_id for tasks, _ in phases for task in tasks
                ]
                self.assertEqual(len(task_ids), len(set(task_ids)))

    def test_market_scan_topic_reaches_every_prompt(self):
        topic = "underwater basket weaving kits"
        phases = build_preset_tasks("market_scan", num_agents=100, topic=topic)
        for tasks, _ in phases:
            for task in tasks:
                self.assertIn(topic, task.prompt)


if __name__ == "__main__":
    unittest.main()
