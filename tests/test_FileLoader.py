import pytest
import requests
from pgpy.fileloader import FileLoader

import os.path

try:
    e = FileNotFoundError
except NameError:
    e = IOError

skipurls = False
try:
    test_request = requests.get("https://www.google.com/robots.txt")
except ConnectionError:
    skipurls = True


@pytest.fixture(
    params=[
        None,
        pytest.mark.skipif(skipurls, "http://www.dancewithgrenades.com/robots.txt", reason="No Internet"),
        pytest.mark.skipif(skipurls, "https://www.google.com/robots.txt", reason="No Internet"),
        "tests/testdata/unsigned_message",
        "tests/testdata/sym_to_unsigned_message",
        open("tests/testdata/unsigned_message", 'rb'),
        open("tests/testdata/unsigned_message", 'rb').read(),
        open("tests/testdata/testkeys.gpg", 'rb').read(),
        "tests/testdata/newfile",
    ],
    ids=[
        "None",
        "http",
        "https",
        "path",
        "symlink",
        "fileobj",
        "unsigned-text-bytes",
        "gpg-keyring-bytes",
        "newfile",
    ]
)
def load(request):
    return request.param


class TestFileLoader:
    def test_load(self, load):
        FileLoader(load)

    @pytest.mark.parametrize("fload", ["/this/path/is/not/valid", "http://www.google.com/404"],
                             ids=["invalid-path", "invalid-url"])
    def test_load_fail(self, fload):
        with pytest.raises(e):
            FileLoader(fload)