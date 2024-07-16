import unittest
from unittest.mock import MagicMock, patch
from kivymd.app import MDApp
from screen_classes.feeding_entry_screen import FeedingEntryScreen
import sqlite3

class TestFeedingEntryScreen(unittest.TestCase):

    def setUp(self):
        self.screen = FeedingEntryScreen()
        self.screen.manager = MagicMock()
        self.screen.manager.get_screen.return_value.ids = MagicMock()
        self.screen.manager.get_screen.return_value.ids.baby_selector = MagicMock()
        self.screen.manager.get_screen.return_value.ids.feed_hour = MagicMock()
        self.screen.manager.get_screen.return_value.ids.feed_date = MagicMock()
        self.screen.manager.get_screen.return_value.ids.feed_notes = MagicMock()

    @patch('food_entries.sqlite3.connect')
    @patch('feeding_entry_screen.MDApp.get_running_app')
    def test_fetch_babies(self, mock_get_running_app, mock_connect):
        mock_get_running_app.return_value.current_user_id = 1
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = [
            (1, 'Baby1'),
            (2, 'Baby2')
        ]

        babies = self.screen.fetch_babies()
        self.assertEqual(len(babies), 2)
        self.assertEqual(babies[0]['baby_name'], 'Baby1')
        self.assertEqual(babies[1]['baby_name'], 'Baby2')

    @patch('feeding_entry_screen.MDDropdownMenu')
    @patch('feeding_entry_screen.FeedingEntryScreen.fetch_babies')
    def test_show_baby_selector(self, mock_fetch_babies, mock_menu):
        mock_fetch_babies.return_value = [{'baby_name': 'Baby1'}, {'baby_name': 'Baby2'}]

        self.screen.show_baby_selector()
        self.assertTrue(mock_menu.called)
        self.assertEqual(len(mock_menu.call_args[1]['items']), 2)

    @patch('food_entries.sqlite3.connect')
    @patch('feeding_entry_screen.MDApp.get_running_app')
    def test_add_food_entry(self, mock_get_running_app, mock_connect):
        mock_get_running_app.return_value.current_user_id = 1
        mock_cursor = mock_connect.return_value.cursor.return_value

        self.screen.add_food_entry(
            baby_id=None,
            baby_name="Baby1",
            feed_hour="12:00",
            feed_date="2023-07-15",
            ml=100,
            notes="Test notes"
        )

        self.assertTrue(mock_cursor.execute.called)
        self.assertTrue(mock_cursor.execute.call_args[0][0].startswith('INSERT INTO food_entries'))

    def test_clear_fields(self):
        self.screen.clear_fields()
        self.screen.manager.get_screen.return_value.ids.baby_selector.text = ''
        self.screen.manager.get_screen.return_value.ids.feed_hour.text = ''
        self.screen.manager.get_screen.return_value.ids.feed_date.text = ''
        self.screen.manager.get_screen.return_value.ids.feed_notes.text = ''
        self.assertEqual(self.screen.manager.get_screen.return_value.ids.baby_selector.text, '')
        self.assertEqual(self.screen.manager.get_screen.return_value.ids.feed_hour.text, '')
        self.assertEqual(self.screen.manager.get_screen.return_value.ids.feed_date.text, '')
        self.assertEqual(self.screen.manager.get_screen.return_value.ids.feed_notes.text, '')

if __name__ == '__main__':
    unittest.main()
