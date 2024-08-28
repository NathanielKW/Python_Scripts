import base64
import sys

argLen = len(sys.argv)

if argLen < 2:
    print("No string to decode was provided")
else:
    b64String = sys.argv[1]
    b64Bytes = b64String.encode("ascii")
    decodeBytes = base64.b64decode(b64Bytes)
    decodeString = decodeBytes.decode("ascii")

    print(f"Decoded string: {decodeString}")