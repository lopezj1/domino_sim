"""Contract tests for API endpoints using FastAPI TestClient."""

import pytest
from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


@pytest.mark.contract
class TestHealthContract:
    def test_health_returns_200(self):
        resp = client.get("/health")
        assert resp.status_code == 200

    def test_health_has_status_field(self):
        resp = client.get("/health")
        data = resp.json()
        assert "status" in data


@pytest.mark.contract
class TestGameRunContract:
    def _valid_payload(self, **overrides):
        base = {"strategy_a": "greedy", "strategy_b": "random", "seed": 42, "include_trace": False}
        base.update(overrides)
        return base

    def test_valid_request_returns_200(self):
        resp = client.post("/game/run", json=self._valid_payload())
        assert resp.status_code == 200

    def test_response_has_required_fields(self):
        resp = client.post("/game/run", json=self._valid_payload())
        data = resp.json()
        assert "outcome" in data
        assert "trace" in data
        outcome = data["outcome"]
        for field in ("winner", "score_differential", "turns", "seed", "timestamp"):
            assert field in outcome, f"Missing field: {field}"

    def test_trace_empty_by_default(self):
        resp = client.post("/game/run", json=self._valid_payload(include_trace=False))
        assert resp.json()["trace"] == []

    def test_trace_non_empty_when_requested(self):
        resp = client.post("/game/run", json=self._valid_payload(include_trace=True))
        trace = resp.json()["trace"]
        assert len(trace) > 0
        # First event is always "deal"
        assert trace[0]["type"] == "deal"

    def test_invalid_strategy_returns_400(self):
        resp = client.post("/game/run", json=self._valid_payload(strategy_a="nonexistent"))
        assert resp.status_code == 400

    def test_turns_positive(self):
        resp = client.post("/game/run", json=self._valid_payload())
        assert resp.json()["outcome"]["turns"] > 0

    def test_all_three_strategy_combos(self):
        strategies = ["greedy", "random", "blocking"]
        for sa in strategies:
            for sb in strategies:
                resp = client.post("/game/run", json=self._valid_payload(strategy_a=sa, strategy_b=sb))
                assert resp.status_code == 200


@pytest.mark.contract
class TestMonteCarloCompareContract:
    def _valid_payload(self, **overrides):
        base = {
            "strategy_a": "greedy",
            "strategy_b": "random",
            "num_runs": 10,
            "start_seed": 1000,
        }
        base.update(overrides)
        return base

    def test_valid_request_returns_200(self):
        resp = client.post("/monte-carlo/compare", json=self._valid_payload())
        assert resp.status_code == 200

    def test_win_rates_sum_to_one(self):
        resp = client.post("/monte-carlo/compare", json=self._valid_payload())
        result = resp.json()["result"]
        total = result["win_rate_a"] + result["win_rate_b"]
        assert abs(total - 1.0) < 1e-9

    def test_wins_sum_to_total_runs(self):
        resp = client.post("/monte-carlo/compare", json=self._valid_payload())
        result = resp.json()["result"]
        assert result["runs_a_wins"] + result["runs_b_wins"] == result["total_runs"]

    def test_per_run_outcomes_count_matches_num_runs(self):
        num_runs = 10
        resp = client.post("/monte-carlo/compare", json=self._valid_payload(num_runs=num_runs))
        data = resp.json()
        assert len(data["per_run_outcomes"]) == num_runs

    def test_invalid_strategy_returns_400(self):
        resp = client.post("/monte-carlo/compare", json=self._valid_payload(strategy_b="bogus"))
        assert resp.status_code == 400

    def test_ci_lower_le_upper(self):
        resp = client.post("/monte-carlo/compare", json=self._valid_payload())
        result = resp.json()["result"]
        assert result["ci_lower"] <= result["ci_upper"]

    def test_execution_time_positive(self):
        resp = client.post("/monte-carlo/compare", json=self._valid_payload())
        assert resp.json()["result"]["execution_time_seconds"] > 0

    def test_num_runs_too_low_returns_422(self):
        resp = client.post("/monte-carlo/compare", json=self._valid_payload(num_runs=5))
        assert resp.status_code == 422
