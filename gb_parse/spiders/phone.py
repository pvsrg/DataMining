import base64
from PIL import Image
import numpy as np


def define_phone(str_base64):
    def define_symbol(symbol):
        if symbol.shape[1] < 12:
            return ('1' if sum(symbol[4, :]) > 0 else '')
        else:
            if symbol[20, 2] > 0:
                if symbol[13, 1] > 0:
                    return ('0' if symbol[7, 17] > 0 else '6')
                else:
                    return ('4' if symbol[20, 10] > 0 else '8')
            else:
                if sum(symbol[0, :]) > 10:
                    return ('5' if sum(symbol[symbol.shape[0] - 3, :]) > 9 else '7')
                else:
                    if symbol[9, 2] > 0:
                        return ('9')
                    else:
                        return ('2' if sum(symbol[symbol.shape[0] - 1, :]) > 10 else '3')

    class MyFile:
        def __init__(self, str_base64):
            self.buf = base64.b64decode(str_base64)
            self.n = 0

        def read(self, nmb):
            b = self.n
            self.n += nmb
            return self.buf[b:(b + nmb)]

        def seek(self, n):
            self.n = n

        def tell(self):
            return self.n

    img = Image.open(MyFile(str_base64))
    pix = np.array(img)
    pix_array = np.array(
        [[(1 if sum(pix[row, col, :]) > 200 else 0) for col in range(pix.shape[1])] for row in range(12, 42)])

    phone = ''
    end_col = 0
    while True:
        for beg_col in range(end_col, pix_array.shape[1]):
            if sum(pix_array[:, beg_col: beg_col + 1]) > 0:
                break

        for end_col in range(beg_col, pix_array.shape[1]):
            if sum(pix_array[:, end_col: end_col + 1]) == 0:
                break

        if end_col + 1 == pix_array.shape[1]:
            break

        phone += define_symbol(pix_array[:, beg_col: end_col])

    return (phone)


if __name__ == "__main__":
    png_base64 = "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"
    print(define_phone(png_base64))
