import unittest
from pprint import pprint
from res_maker import parse_http_req, make_response

test_header = """GET /index.html HTTP/1.1
Host: localhost:8000
Connection: keep-alive
Content-Length: 6

Yes man!
"""

class TestRequest(unittest.TestCase):

    def test_req(self):
        result = parse_http_req(test_header)

        pprint(result)
        self.assertEqual(result["verb"], "GET")
        self.assertEqual(result["path"], "/index.html")
        self.assertEqual(result["body"], "Yes ma")

    def test_res(self):
        pprint(make_response(test_header))

if __name__ == '__main__':
    unittest.main()
