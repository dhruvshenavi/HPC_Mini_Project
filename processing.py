def run_parallel(lines, keyword):
    processed = []
    count = 0

    keyword = keyword.lower()

    for line in lines:
        cleaned = ''.join(c.lower() for c in line if c.isalnum() or c == ' ')

        # exact match check
        if f" {keyword} " in f" {cleaned} ":
            processed.append(cleaned)
            count += 1

    return processed, count