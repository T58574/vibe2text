from unittest import mock
from injector import TextInjector

def test_text_injector():
    mock_controller = mock.MagicMock()
    with mock.patch("injector.Controller", return_value=mock_controller), \
         mock.patch("time.sleep") as mock_sleep:
        
        injector = TextInjector()
        injector.inject("hello world")
        
        mock_sleep.assert_called_once_with(0.1)
        mock_controller.type.assert_called_once_with("hello world")
