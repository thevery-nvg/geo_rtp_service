def format_size(size_in_bytes):
    units = ['Б', 'КБ', 'МБ', 'ГБ', 'ТБ']
    unit_index = 0
    while size_in_bytes >= 1024 and unit_index < len(units) - 1:
        size_in_bytes /= 1024
        unit_index += 1
    return f"{size_in_bytes:.2f} {units[unit_index]}"