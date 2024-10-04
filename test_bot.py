import unittest
from db import init_db, user_exists, add_user
from gpt import generate_content
from report import generate_report
import os


class TestDatabaseFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()

    def test_add_and_check_user(self):
        telegram_id = 123456
        university = "Test University"
        student_name = "Test Student"
        group_name = "Test Group"
        course = "1"
        department = "Test Department"

        add_user(telegram_id, university, student_name, group_name, course, department)
        user = user_exists(telegram_id)

        self.assertIsNotNone(user)
        self.assertEqual(user[1], telegram_id)


class TestGPTFunctions(unittest.TestCase):
    def test_generate_content(self):
        prompt = "Generate a simple report"
        content = generate_content(prompt)
        self.assertIsInstance(content, str)
        self.assertGreater(len(content), 0)


class TestReportGeneration(unittest.TestCase):
    def test_generate_report(self):
        user_data = {
            'student_name': "Test Student",
            'university': "Test University",
            'group_name': "Test Group",
            'course': "1",
            'department': "Test Department"
        }
        content = "This is a test content"
        report_type = "lab_report"

        file_path = generate_report(report_type, content, user_data)
        self.assertTrue(os.path.exists(file_path))
        os.remove(file_path)  # Clean up after test


if __name__ == '__main__':
    unittest.main()
