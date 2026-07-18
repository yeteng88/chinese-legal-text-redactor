import unittest

from cn_legal_redactor import available_types, redact_text, redact_with_report


class RedactorTests(unittest.TestCase):
    def test_redacts_supported_identifiers(self):
        source = (
            "身份证：11010519491231002X；手机：+86 13800138000；"
            "电话：010-12345678；邮箱：person@example.com；"
            "银行卡：6222 0201 1234 5678 901。"
        )

        result = redact_with_report(source)

        self.assertEqual(
            result.text,
            "身份证：[ID_CARD]；手机：[MOBILE]；电话：[PHONE]；"
            "邮箱：[EMAIL]；银行卡：[BANK_CARD]。",
        )
        self.assertEqual(result.total, 5)
        self.assertTrue(all(count == 1 for count in result.counts.values()))

    def test_can_select_specific_types(self):
        source = "手机：13800138000，邮箱：person@example.com"
        result = redact_with_report(source, ["email"])

        self.assertEqual(result.text, "手机：13800138000，邮箱：[EMAIL]")
        self.assertEqual(result.counts, {"email": 1})

    def test_does_not_change_ordinary_case_numbers(self):
        source = "案号：（2026）皖01民初123号，金额844万元。"
        self.assertEqual(redact_text(source), source)

    def test_rejects_unknown_type(self):
        with self.assertRaisesRegex(ValueError, "Unsupported redaction type"):
            redact_text("text", ["name"])

    def test_available_types_are_stable(self):
        self.assertEqual(
            available_types(),
            ("email", "id_card", "mobile", "phone", "bank_card"),
        )


if __name__ == "__main__":
    unittest.main()
