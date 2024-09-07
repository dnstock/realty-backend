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