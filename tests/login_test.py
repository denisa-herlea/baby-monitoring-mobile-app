import unittest
from unittest.mock import MagicMock, patch
from main import DemoApp

class TestLoginFunction(unittest.TestCase):

    def setUp(self):
        self.app = DemoApp()
        self.app.theme_cls = MagicMock()
        self.app.theme_cls.primary_color = [1, 0, 0, 1]
        self.app.theme_cls.error_color = [1, 0, 0, 1]
        self.app.theme_cls.primary_palette = 'Blue'
        self.app.theme_cls.accent_palette = 'Amber'
        self.app.theme_cls.background_palette = 'Primary'

        self.app.theme_cls.font_styles = {
            "H1": ["RobotoLight", 96, False, -1.5],
            "H2": ["RobotoLight", 60, False, -0.5],
            "H3": ["Roboto", 48, False, 0],
            "H4": ["Roboto", 34, False, 0.25],
            "H5": ["Roboto", 24, False, 0],
            "H6": ["RobotoMedium", 20, False, 0.15],
            "Subtitle1": ["Roboto", 16, False, 0.15],
            "Subtitle2": ["RobotoMedium", 14, False, 0.1],
            "Body1": ["Roboto", 16, False, 0.5],
            "Body2": ["Roboto", 14, False, 0.25],
            "Button": ["RobotoMedium", 14, True, 1.25],
            "Caption": ["Roboto", 12, False, 0.4],
            "Overline": ["Roboto", 10, True, 1.5],
        }
        self.app.root = MagicMock()

    @patch('sqlite3.connect')
    def test_login_success(self, mock_connect):
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchone.return_value = (19, 'denisa')

        self.app.login('denisa', 'denisa')

        self.assertEqual(self.app.root.current, 'Home')
        self.assertEqual(self.app.current_user_id, 19)

    @patch('sqlite3.connect')
    def test_login_missing_password(self, mock_connect):
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchone.return_value = None

        self.app.login('denisa', '')

        login_screen = self.app.root.get_screen('Login')
        self.assertEqual(login_screen.ids['login_password'].line_color_normal, self.app.theme_cls.error_color)

if __name__ == '__main__':
    unittest.main()
