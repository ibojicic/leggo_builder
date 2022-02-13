import os
import traceback

import MontagePy.main as montage_new


def cutout(in_image: str, out_image: str, x_coord: float, y_coord: float, box_x_coord: float,
           box_y_coord: float = False) -> bool:
    x_coord = float(x_coord)
    y_coord = float(y_coord)

    box_x_coord = float(box_x_coord)

    if not box_y_coord:
        box_y_coord = box_x_coord

    box_y_coord = float(box_y_coord)

    try:
        results = montage_new.mSubimage(in_image, out_image, x_coord, y_coord, box_x_coord / 3600., box_y_coord / 3600.)
        if results['status'] == '1':
            if os.path.exists(out_image):
                os.remove(out_image)
            return False
    except RuntimeError:
        print("Montage cutout failed:")
        traceback.print_exc()  # print full exception
        return False
    return True
