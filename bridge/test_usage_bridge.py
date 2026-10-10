import unittest
import tempfile
from pathlib import Path
from usage_bridge import usage_packet, Status, Singleton


class UsageTests(unittest.TestCase):
    def test_duration_not_position(self):
        result = usage_packet({"rateLimits": {"primary": {"usedPercent": 60, "windowDurationMins": 10080}, "secondary": {"usedPercent": 20, "windowDurationMins": 300}}}, 100)
        self.assertEqual([w["label"] for w in result["windows"]], ["5H", "WEEK"])
        self.assertEqual(result["updated"], 100)

    def test_missing_is_not_zero(self):
        self.assertEqual(usage_packet({})["windows"], [])
        self.assertEqual(usage_packet({"rateLimits": {"primary": {"usedPercent": None}}})["windows"], [])

    def test_unknown_duration_and_reset(self):
        result = usage_packet({"rateLimits": {"primary": {"usedPercent": 0}}})["windows"][0]
        self.assertEqual(result, {"label": "OTHER", "used": 0, "minutes": None, "reset": None})

    def test_clamp(self):
        result = usage_packet({"rateLimits": {"primary": {"usedPercent": -4}, "secondary": {"usedPercent": 120}}})
        self.assertEqual([w["used"] for w in result["windows"]], [0, 100])

    def test_codex_bucket_preferred(self):
        result = usage_packet({"rateLimits": {"primary": {"usedPercent": 99}}, "rateLimitsByLimitId": {"codex": {"primary": {"usedPercent": 12}}}})
        self.assertEqual(result["windows"][0]["used"], 12)

    def test_never_substitute_other_bucket(self):
        result = usage_packet({"rateLimitsByLimitId": {"other": {"primary": {"usedPercent": 12}}}})
        self.assertEqual(result["windows"], [])

    def test_nonfinite_and_boolean_rejected(self):
        for value in [True, float("nan"), float("inf"), "3"]:
            self.assertEqual(usage_packet({"rateLimits": {"primary": {"usedPercent": value}}})["windows"], [])

    def test_ack_does_not_refresh_sample(self):
        status = Status(Path("unused"))
        packet = usage_packet({}, 100)
        status.sample(packet)
        status.ack(b'{"type":"ack","updated":100,"sd":true,"secret":"discard"}', 150)
        status.ack(b'{"type":"ack","updated":100,"sd":true}', 200)
        self.assertEqual(status.data["last_api_sample"]["updated"], 100)
        self.assertEqual(status.data["ack_received"], 200)
        self.assertEqual(status.data["ack_updated"], 100)
        self.assertTrue(status.data["sd"])
        self.assertNotIn("secret", status.data)

    def test_serial_noise_not_ack(self):
        status = Status(Path("unused"))
        for line in [b'booting', b'[]', b'{"type":"ack","updated":null}', b'{"type":"status","updated":4}']:
            status.ack(line)
        self.assertIsNone(status.data["ack_received"])

    def test_singleton_blocks_duplicate_then_releases(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bridge.lock"
            first = Singleton(path)
            try:
                with self.assertRaises(RuntimeError):
                    Singleton(path)
            finally:
                first.close()
            second = Singleton(path)
            second.close()


if __name__ == "__main__":
    unittest.main()
