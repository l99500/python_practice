import subprocess
import socket
import time
import pytest


@pytest.fixture(scope="session")
def echo_server(request):
    p = subprocess.Popen(
            ['python', 'socket_server.py'])
    time.sleep(1)
    request.addfinalizer(lambda: p.terminate())
    return p


@pytest.fixture(scope="function")
def client_socket(request):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 1028))
    request.addfinalizer(lambda: s.close())
    return s


def test_echo(echo_server, client_socket):
    client_socket.send(b"abc")
    assert client_socket.recv(3) == b"abc"


def test_echo2(echo_server, client_socket):
    client_socket.send(b"def")
    assert client_socket.recv(3) == b"def"
