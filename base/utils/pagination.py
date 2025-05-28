import math


def get_page_info(total_count: int, page_no: int, page_size: int) -> dict:
    """
    Request:
        total_count (int): The total number of items available.
        page_no (int): The current page number (1-based index).
        page_size (int): The number of items to display per page.

    Response:
        dict: A dictionary containing pagination metadata with the following keys:
            - total_page (int): Total number of pages calculated.
            - pre_page (int | None): The previous page number or None if current page is the first.
            - next_page (int | None): The next page number or None if current page is the last.
            - page_size (int): The number of items per page as provided.
            - total_count (int): The total number of items as provided.
            - page_number (int): The current page number as provided.

    Purpose:
        To compute and provide structured pagination information for navigating
        through paged data results effectively.

    Company Name: Softvan Pvt Ltd
    """

    return {
        "total_page": math.ceil(total_count / page_size),
        "pre_page": page_no - 1 if page_no - 1 != 0 else None,
        "next_page": (
            page_no + 1 if page_no + 1 <= math.ceil(total_count / page_size) else None
        ),
        "page_size": page_size,
        "total_count": total_count,
        "page_number": page_no,
    }
