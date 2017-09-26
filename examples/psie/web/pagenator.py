import math


class Pagenator:

    def pagenation(self, total, size, current):
        max_page = int(math.ceil(total / size))
        current_page = int(math.ceil(current / size))
        result = []
        no = 0
        for page in range(current_page - 5, current_page + 1, 1):
            if page >= 0:
                result.append(
                    {"page": page + 1, "current": current_page == page})
            else:
                no += 1
        no2 = 0
        for page in range(current_page + 1, current_page + 5 + no + 1, 1):
            if page < max_page:
                result.append(
                    {"page": page + 1, "current": current_page == page})
            else:
                no2 += 1
        if not result:
            first = result[0]["page"] - 1
            for i in range(0, no2, 1):
                if first - 1 > 0:
                    result.insert(0, {"page": first - i, "current": False})
        return result
