import platform

def print_startup_info(data: list[tuple[str, str]]) -> None:
    # Determine the length of the longest line for proper box size
    longest_line_length = max(len(f'{label}: {value}') for label, value in data)
    box_width = longest_line_length + 4  # Add some padding for the box

    # Top border
    print('+' + '-' * (box_width + 2) + '+')

    # Print each variable from the array
    for label, value in data:
        line = f'{label}: {value}'
        print(f'| {line.ljust(box_width)} |')

    # Mid border
    print('+' + '-' * (box_width + 2) + '+')

    # Print the platform information
    for label, value in [
        # ('Platform', platform.platform()),
        ('Python Version', platform.python_version()),
    ]:
        line = f'{label}: {value}'
        print(f'| {line: <{box_width}} |')
    line = f'Python Version: {platform.python_version()}'

    # Bottom border
    print('+' + '-' * (box_width + 2) + '+')
