import asyncio
import unittest

from fastapi.testclient import TestClient

from app import app
from db import get_all_sessions, delete_all_sessions


class TestApp(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        delete_all_sessions()


    def test_read_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    async def test_websocket(self):
        with self.client.websocket_connect('/ws') as websocket:
            websocket.send_json({"action": "connect", "user_agent": "navigator.userAgent"})
            data = websocket.receive_json()
            await asyncio.sleep(1)
            self.assertEqual(1, len(get_all_sessions()))

            websocket.send_json({"action": "disconnect", "session_id": data['session_id']})
            await asyncio.sleep(1)
            self.assertEqual(0, len(get_all_sessions()))


if __name__ == '__main__':
    unittest.main()
