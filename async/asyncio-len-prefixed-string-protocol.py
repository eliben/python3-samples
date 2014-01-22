# Mimics the IntNStringReceiverProtocol protocol from Twisted.
# Encapsulates length-prefixed strings of binary data.
import asyncio
import struct


class IntNStringReceiverProtocol(asyncio.Protocol):
    """Protocol for exchanging length-prefixed data packets.

    This class is meant to be subclassed. The subclass should define
    prefix_format to be a format usable by the 'struct' module to encode and
    decode packet lengths.

    string_received will be called on the subclass when a whole string is
    received. send_string can be used to wrap a string for transmission.
    """
    _buf = b''

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        prefix_length = struct.calcsize(self.prefix_format)
        self._buf += data
        cur_offset = 0

        while len(self._buf) >= (cur_offset + prefix_length):
            # Expect the length to be encoded in the beginning of the buffer.
            payload_offset = cur_offset + prefix_length
            length = struct.unpack(self.prefix_format,
                                   self._buf[cur_offset:payload_offset])[0]
            payload_end_offset = payload_offset + length

            # If the whole payload didn't arrive in the buffer yet, nothing to
            # report.
            if payload_end_offset > len(self._buf):
                break

            payload = self._buf[payload_offset:payload_end_offset]
            cur_offset = payload_end_offset
            self.string_received(payload)

        # Discart the parts of the buffer that have been processed.
        self._buf = self._buf[cur_offset:]

    def string_received(self, s):
        raise NotImplementedError

    def send_string(self, s):
        self.transport.write(struct.pack(self.prefix_format, len(s)) + s)


# This is a sample client
class MyStringReceiver(IntNStringReceiverProtocol):
    prefix_format = "<L"

    def string_received(self, s):
        print('received string: {}'.format(s.decode()))
        self.send_string(b'ok')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    coro = loop.create_server(MyStringReceiver, '127.0.0.1', 5566)
    server = loop.run_until_complete(coro)
    print('serving on {}'.format(server.sockets[0].getsockname()))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("exit")
    finally:
        server.close()
        loop.close()
