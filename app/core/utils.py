def print_boxed_sections(*sections: list[tuple[str, str]], title: str | None = None) -> None:
    """
    Prints multiple sections in boxed format with a single border between sections.

    Args:
        sections: A list of sections where each section is a list of key-value pairs (label and value).
        title: (Optional) A title that will be displayed at the top of the output with a unique style.
    """
    # Determine the maximum length across all sections
    longest_line_length = max(len(f'{label}: {value}') for section in sections for label, value in section)
    box_width = longest_line_length + 4  # Add some padding for the box
    # Iterate over each section
    for index, section in enumerate(sections):
        if index == 0:
            # Print title, if provided
            if title:
                # Update the box width if the title is longer or uncentered
                box_width = max(box_width, len(title) + 4)
                box_width += len(title) % 2
                print('+' + '-' * box_width + '+')
                title_line = f' {title} '
                print(f'+{title_line.center(box_width, '=')}+')
            # Top border
            print('+' + '-' * box_width + '+')
        # Print each variable in the current section
        for label, value in section:
            line = f'{label}: {value}'
            print(f'| {line.ljust(box_width-2)} |')
        # Bottom or separating border
        print('+' + '-' * box_width + '+')


## Notifications

# def send_notification(email: str, tenant: schemas.Tenant):
#     # Logic to send email notification
#     print(f"Notification sent to {email} regarding tenant {tenant.name}'s insurance policy expiration.")

# @app.on_event("startup")
# @repeat_every(seconds=86400)  # Runs once a day
# def check_insurance_policies():
#     with database.SessionLocal() as db:
#         today = datetime.today().date()
#         tenants = crud.get_tenants(db)
#         for tenant in tenants:
#             if tenant.insurance_expiration_date < today:
#                 manager = crud.get_user(user_id=tenant.manager_id)
#                 utils.send_notification(manager.email, tenant)
