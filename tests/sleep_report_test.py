import unittest
from unittest.mock import MagicMock, patch
from main import SleepRecScreen, SleepReportScreen, MDApp
import sqlite3

class TestSleepRecScreen(unittest.TestCase):

    def setUp(self):
        self.screen = SleepRecScreen()

    def test_on_enter(self):
        self.screen.on_enter()
        self.assertIsNotNone(self.screen.data_table)
        self.assertEqual(self.screen.data_table.row_data[0], ("Babies (<4 months)", "16+ hours"))

class TestSleepReportScreen(unittest.TestCase):

    def setUp(self):
        self.screen = SleepReportScreen()
        self.screen.ids = MagicMock()

    @patch('sqlite3.connect')
    @patch('main.MDApp.get_running_app')
    def test_load_data_no_babies(self, mock_get_running_app, mock_connect):
        mock_get_running_app.return_value.current_user_id = 1
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = []

        self.screen.load_data()
        self.screen.ids.cards_container.clear_widgets.assert_called_once()

    @patch('sqlite3.connect')
    @patch('main.MDApp.get_running_app')
    def test_load_data_with_babies(self, mock_get_running_app, mock_connect):
        mock_get_running_app.return_value.current_user_id = 1
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = [
            (1, 'Baby1', '2021-01-01', '08:00', '10:00'),
            (1, 'Baby1', '2021-01-01', '13:00', '15:00'),
            (2, 'Baby2', '2022-01-01', None, None)
        ]

        self.screen.load_data()
        self.assertEqual(len(self.screen.ids.cards_container.mock_calls), 1)
        self.assertEqual(len(self.screen.ids.cards_container.add_widget.mock_calls), 2)

    @patch('sqlite3.connect')
    def test_create_card(self, mock_connect):
        card = self.screen.create_card(1, "Baby1", 8, 12)
        self.assertIsNotNone(card)
        self.assertEqual(card.children[1].children[0].text, "Baby1: 8.0/12 hours")

    @patch('sqlite3.connect')
    def test_show_sleep_chart(self, mock_connect):
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = [
            ('2024-07-01', '08:00', '10:00'),
            ('2024-07-02', '09:00', '11:00')
        ]
        self.screen.ids.chart_container = MagicMock()
        self.screen.ids.close_button = MagicMock()

        self.screen.show_sleep_chart(1, 16)

        self.screen.ids.chart_container.clear_widgets.assert_called_once()
        self.screen.ids.close_button.opacity = 1
        self.screen.ids.close_button.disabled = False

    @patch('sqlite3.connect')
    @patch('main.MDApp.get_running_app')
    def test_load_data_calculate_sleep(self, mock_get_running_app, mock_connect):
        mock_get_running_app.return_value.current_user_id = 1
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = [
            (1, 'Baby1', '2021-01-01', '22:00', '06:00'),
        ]

        self.screen.load_data()
        self.assertEqual(len(self.screen.ids.cards_container.mock_calls), 1)
        self.assertEqual(len(self.screen.ids.cards_container.add_widget.mock_calls), 1)

if __name__ == '__main__':
    unittest.main()
