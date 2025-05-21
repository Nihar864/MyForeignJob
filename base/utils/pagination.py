import math


def get_page_info(total_count: int, page_no: int, page_size: int) -> dict:
    return {
        "total_page": math.ceil(total_count / page_size),
        "pre_page": page_no - 1 if page_no - 1 != 0 else None,
        "next_page": (
            page_no + 1 if page_no + 1 <= math.ceil(
                total_count / page_size) else None
        ),
        "page_size": page_size,
        "total_count": total_count,
        "page_number": page_no,
    }
