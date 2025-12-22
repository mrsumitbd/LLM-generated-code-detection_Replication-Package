import dynamixel_sdk as dxl
import tests.mock_dynamixel_sdk as dxl
import dynamixel_sdk as dxl
import dynamixel_sdk as dxl
import tests.mock_dynamixel_sdk as dxl
import dynamixel_sdk as dxl
import tests.mock_dynamixel_sdk as dxl
import dynamixel_sdk as dxl
import tests.mock_dynamixel_sdk as dxl
import tests.mock_dynamixel_sdk as dxl
import tests.mock_dynamixel_sdk as dxl
import dynamixel_sdk as dxl
import dynamixel_sdk as dxl

def convert_to_bytes(value, bytes, mock=False):
    if mock:
        return value

    import dynamixel_sdk as dxl

    # Note: No need to convert back into unsigned int, since this byte preprocessing
    # already handles it for us.
    if bytes == 1:
        data = [
            dxl.DXL_LOBYTE(dxl.DXL_LOWORD(value)),
        ]
    elif bytes == 2:
        data = [
            dxl.DXL_LOBYTE(dxl.DXL_LOWORD(value)),
            dxl.DXL_HIBYTE(dxl.DXL_LOWORD(value)),
        ]
    elif bytes == 4:
        data = [
            dxl.DXL_LOBYTE(dxl.DXL_LOWORD(value)),
            dxl.DXL_HIBYTE(dxl.DXL_LOWORD(value)),
            dxl.DXL_LOBYTE(dxl.DXL_HIWORD(value)),
            dxl.DXL_HIBYTE(dxl.DXL_HIWORD(value)),
        ]
    else:
        raise NotImplementedError(
            f"Value of the number of bytes to be sent is expected to be in [1, 2, 4], but "
            f"{bytes} is provided instead."
        )
    return data