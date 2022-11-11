import unittest

from gojyuon_danmaku_game import initdata


class MyTestCase(unittest.TestCase):
    def test_get_roumaji(self):
        a = initdata.get_roumaji("a")
        self.assertEqual("a", a)
        a = initdata.get_roumaji("あ")
        self.assertEqual("a", a)
        a = initdata.get_roumaji("ア")
        self.assertEqual("a", a)
        with self.assertRaises(Exception):
            a = initdata.get_roumaji("⁂")





if __name__ == '__main__':
    unittest.main()
