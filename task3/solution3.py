def make_tuples(lst: list) -> list:
    return [(lst[i], lst[i + 1]) for i in range(0, len(lst), 2)]


def merge_intervals(intervals):
    if not intervals:
        return []
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


def appearance(intervals: dict[str, list[int]]) -> int:
    lesson_interval = intervals["lesson"]
    pupil_intervals = merge_intervals(make_tuples(intervals["pupil"]))
    tutor_intervals = merge_intervals(make_tuples(intervals["tutor"]))

    # clip pupil_intervals to lesson_intervals
    start_lesson, end_lesson = lesson_interval
    clipped_pupil_intervals = []
    for start, end in pupil_intervals:
        clipped_start = max(start, start_lesson)
        clipped_end = min(end, end_lesson)
        if clipped_start < clipped_end:
            clipped_pupil_intervals.append((clipped_start, clipped_end))

    # intersect clipped_pupil_intervals and tutor_intervals
    result_intervals = []
    i, j = 0, 0
    while i < len(clipped_pupil_intervals) and j < len(tutor_intervals):
        start1, end1 = clipped_pupil_intervals[i]
        start2, end2 = tutor_intervals[j]
        start = max(start1, start2)
        end = min(end1, end2)
        if start < end:
            result_intervals.append((start, end))
        if end1 < end2:
            i += 1
        else:
            j += 1

    total_time = sum(end - start for start, end in result_intervals)
    return total_time
