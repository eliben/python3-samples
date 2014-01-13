#-------------------------------------------------------------------------------
# Basic echo server using the selectors module.
#
# Based on the example provided in the documentation.
#
# Eli Bendersky (eliben@gmail.com)
# This code is in hte public domain
#-------------------------------------------------------------------------------
import logging
import selectors
import socket
import time

HOST = 'localhost'
PORT = 40404

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')


class SelectorServer:
    def __init__(self, host, port):
        # Create the main socket that accepts incoming connections and start
        # listening. The socket is nonblocking.
        self.main_socket = socket.socket()
        self.main_socket.bind((host, port))
        self.main_socket.listen(100)
        self.main_socket.setblocking(False)

        # Create the selector object that will dispatch events. Register
        # interest in read events, that include incoming connections.
        # The handler method is passed in data so we can fetch it in
        # serve_forever.
        self.selector = selectors.DefaultSelector()
        self.selector.register(fileobj=self.main_socket,
                               events=selectors.EVENT_READ,
                               data=self.on_accept)

        self.current_peers = set()

    def on_accept(self, sock, mask):
        # This is a handler for the main_socket which is now listening, so we
        # know it's ready to accept a new connection.
        conn, addr = self.main_socket.accept()
        logging.info('accepted connection from {0}'.format(addr))
        conn.setblocking(False)

        self.current_peers.add(conn.getpeername())
        # Register interest in read events on the new socket, dispatching to
        # self.on_read
        self.selector.register(fileobj=conn, events=selectors.EVENT_READ,
                               data=self.on_read)

    def on_read(self, conn, mask):
        # This is a handler for peer sockets - it's called when there's new
        # data.
        data = conn.recv(1000)
        peername = conn.getpeername()

        if data:
            logging.info('got data from {}: {!r}'.format(peername, data))
            # Assume for simplicity that send won't block
            conn.send(data)
        else:
            # No data on recv: the client closed its connection. Close our side
            # too.
            logging.info('closing connection to {0}'.format(peername))
            self.current_peers.remove(peername)
            self.selector.unregister(conn)
            conn.close()

    def serve_forever(self):
        last_report_time = time.time()

        while True:
            # Wait until some registered socket becomes ready. This will block
            # for 200 ms.
            events = self.selector.select(timeout=0.2)

            # For each new event, dispatch to its handler
            for key, mask in events:
                handler = key.data
                handler(key.fileobj, mask)

            # This part happens roughly every second.
            cur_time = time.time()
            if cur_time - last_report_time > 1:
                logging.info('Running report...')
                logging.info('Have {0} peers'.format(len(self.current_peers)))
                last_report_time = cur_time


if __name__ == '__main__':
    logging.info('starting')
    server = SelectorServer(host=HOST, port=PORT)
    server.serve_forever()
