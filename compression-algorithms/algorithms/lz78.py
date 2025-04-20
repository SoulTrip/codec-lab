from typing import List, Tuple, Union, Dict


class LZ78Compression:
    def __init__(self):
        pass

    def compress(self, data: Union[str, bytes], binary: bool = False) -> List[Tuple[int, Union[str, int]]]:
        """
        Compresses input data using LZ78.
        :param data: Input string or bytes
        :param binary: Set True if input is bytes
        :return: List of (prefix_id, next_symbol) pairs
        """
        if not binary:
            data = data.encode("utf-8")

        d: Dict[bytes, int] = {b"": 0}
        phrase_id = 1
        prefix = b""
        result: List[Tuple[int, int]] = []

        for byte in data:
            prefix += bytes([byte])
            if prefix in d:
                continue
            result.append((d[prefix[:-1]], prefix[-1]))
            d[prefix] = phrase_id
            phrase_id += 1
            prefix = b""

        if prefix:
            result.append((d[prefix[:-1]], prefix[-1]))

        return result

    def decompress(self, encoded: List[Tuple[int, Union[str, int]]], binary: bool = False) -> Union[str, bytes]:
        """
        Decompresses encoded data using LZ78.
        :param encoded: List of (prefix_id, next_symbol)
        :param binary: Set True to return bytes
        :return: Original string or bytes
        """
        d: Dict[int, bytes] = {0: b""}
        result = bytearray()
        phrase_id = 1

        for idx, symbol in encoded:
            if not isinstance(symbol, int):
                symbol = ord(symbol)  # For str mode fallback
            entry = d[idx] + bytes([symbol])
            result.extend(entry)
            d[phrase_id] = entry
            phrase_id += 1

        return result if binary else result.decode("utf-8")