import asyncio
import struct


class IntNStringReceiverProtocol(asyncio.Protocol):
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
                                   self._buf[cur_offset:payload_offset])
            payload_end_offset = payload_offset + length

            # If the whole payload didn't arrive in the buffer yet, nothing to
            # report.
            if payload_end_offset > len(self._buf):
                break

            payload = self._buf[payload_offset:payload_end_offset]
            cur_offset = payload_end_offset
            self.string_received(payload)

        # Discart the parts of the buffer that have been processed.
        self._buf = self.buf[cur_offset:]

    def string_received(self, s):
        raise NotImplementedError

    def send_string(self, s):
        self.transport.write(struct.pack(self.prefix_format, len(s)) + s)


class MyStringReceiver(IntNStringReceiverProtocol):
    prefix_format = "<L"

    def string_received(self, s):
        print('received string: {}'.format(s.decode()))

