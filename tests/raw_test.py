import pytest

from rawphoto import raw
from rawphoto.raw import Raw
from tests.cr2_test import cr2_bytes


@pytest.fixture
def cr2_file(tmpdir):
    tmpdir.join("file.cr2").write_binary(cr2_bytes)
    return tmpdir.strpath + '/file.cr2'


def test_discover_must_be_recursive(tmpdir):
    tmpdir.join("file1.CR2").write("")
    tmpdir.mkdir("sub").join("file2.CR2").write("")
    assert len(raw.discover(tmpdir.strpath)) == 2


def test_discover_must_be_case_insensitive(tmpdir):
    tmpdir.join("file1.CR2").write("")
    tmpdir.join("file2.Cr2").write("")
    tmpdir.join("file3.cR2").write("")
    tmpdir.join("file4.cr2").write("")
    assert len(raw.discover(tmpdir.strpath)) == 4


def test_discover_must_ignore_unsupported_extensions(tmpdir):
    tmpdir.join("file.abc").write("")
    assert len(raw.discover(tmpdir.strpath)) == 0


def test_default_endianness(cr2_file):
    r = Raw(file=cr2_file)
    assert r.endianness == "@"
