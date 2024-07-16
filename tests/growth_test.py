import unittest
from unittest.mock import MagicMock, patch
import sqlite3
from main import LogMeasurementScreen, MeasurementReportScreen, MDApp

class TestLogMeasurementScreen(unittest.TestCase):

    def setUp(self):
        self.screen = LogMeasurementScreen()
        self.screen.manager = MagicMock()
        self.screen.manager.get_screen.return_value.ids = MagicMock()
        self.screen.manager.get_screen.return_value.ids.baby_selector = MagicMock()
        self.screen.manager.get_screen.return_value.ids.height_field = MagicMock()
        self.screen.manager.get_screen.return_value.ids.weight_field = MagicMock()
        self.screen.manager.get_screen.return_value.ids.head_circ_field = MagicMock()
        self.screen.manager.get_screen.return_value.ids.measurement_date = MagicMock()

    @patch('baby-v.sqlite3.connect')
    @patch('main.MDApp.get_running_app')
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

    @patch('main.MDDropdownMenu')
    @patch('main.LogMeasurementScreen.fetch_babies')
    def test_show_baby_selector(self, mock_fetch_babies, mock_menu):
        mock_fetch_babies.return_value = [{'baby_name': 'Baby1'}, {'baby_name': 'Baby2'}]

        self.screen.show_baby_selector()
        self.assertTrue(mock_menu.called)
        self.assertEqual(len(mock_menu.call_args[1]['items']), 2)

    @patch('baby-v.sqlite3.connect')
    @patch('main.MDApp.get_running_app')
    def test_save_measurement(self, mock_get_running_app, mock_connect):
        mock_get_running_app.return_value.current_user_id = 1
        mock_cursor = mock_connect.return_value.cursor.return_value

        self.screen.save_measurement(
            baby_id=None,
            baby_name="Baby1",
            measurement_date="2023-07-15",
            height_field="50",
            weight_field="3.5",
            head_circ_field="35"
        )

        self.assertTrue(mock_cursor.execute.called)
        self.assertTrue(mock_cursor.execute.call_args[0][0].startswith('INSERT INTO measurement_entries'))

    def test_clear_fields(self):
        self.screen.clear_fields()
        self.assertEqual(self.screen.manager.get_screen.return_value.ids.baby_selector.text, '')
        self.assertEqual(self.screen.manager.get_screen.return_value.ids.height_field.text, '')
        self.assertEqual(self.screen.manager.get_screen.return_value.ids.weight_field.text, '')
        self.assertEqual(self.screen.manager.get_screen.return_value.ids.head_circ_field.text, '')
        self.assertEqual(self.screen.manager.get_screen.return_value.ids.measurement_date.text, '')

class TestMeasurementReportScreen(unittest.TestCase):

    def setUp(self):
        self.screen = MeasurementReportScreen()
        self.screen.ids = MagicMock()

    @patch('baby-v.sqlite3.connect')
    @patch('main.MDApp.get_running_app')
    def test_load_data_no_babies(self, mock_get_running_app, mock_connect):
        mock_get_running_app.return_value.current_user_id = 1
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = []

        self.screen.load_data()
        self.screen.ids.cards_container.clear_widgets.assert_called_once()

    @patch('baby-v.sqlite3.connect')
    @patch('main.MDApp.get_running_app')
    def test_load_data_with_babies(self, mock_get_running_app, mock_connect):
        mock_get_running_app.return_value.current_user_id = 1
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = [
            (1, 'Baby1'),
            (2, 'Baby2')
        ]

        self.screen.load_data()
        self.assertEqual(len(self.screen.ids.cards_container.mock_calls), 1)
        self.assertEqual(len(self.screen.ids.cards_container.add_widget.mock_calls), 2)

    @patch('baby-v.sqlite3.connect')
    def test_create_card(self, mock_connect):
        card = self.screen.create_card(1, "Baby1")
        self.assertIsNotNone(card)
        self.assertEqual(card.children[0].children[0].text, "Baby1")

    @patch('baby-v.sqlite3.connect')
    def test_show_growth_chart(self, mock_connect):
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = [
            ('2024-07-01', 50, 3.5, 35),
            ('2024-07-02', 51, 3.6, 36)
        ]
        self.screen.ids.chart_container = MagicMock()
        self.screen.ids.close_button = MagicMock()

        self.screen.show_growth_chart(1)

        self.screen.ids.chart_container.clear_widgets.assert_called_once()
        self.screen.ids.close_button.opacity = 1
        self.screen.ids.close_button.disabled = False

    @patch('baby-v.sqlite3.connect')
    def test_show_measurement_table(self, mock_connect):
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = [
            ('2024-07-01', 50, 3.5, 35),
            ('2024-07-02', 51, 3.6, 36)
        ]
        self.screen.ids.chart_container = MagicMock()
        self.screen.ids.close_button = MagicMock()

        self.screen.show_measurement_table(1)

        self.screen.ids.chart_container.clear_widgets.assert_called_once()
        self.screen.ids.close_button.opacity = 1
        self.screen.ids.close_button.disabled = False

if __name__ == '__main__':
    unittest.main()
