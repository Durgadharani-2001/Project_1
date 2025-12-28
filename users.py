from authentication import register_user

# ---------------- Create Users ----------------
# Clients
register_user("Meena", "meena123", "Client")
register_user("Arun", "arun123", "Client")
register_user("Kavya", "kavya123", "Client")

# Support
register_user("Rahul", "rahul123", "Support")
register_user("Anita", "anita123", "Support")

print("Users inserted successfully!")


