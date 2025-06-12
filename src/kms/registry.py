from src.kms.local_kms import LocalKMS

# Singleton KMS instance shared across modules
kms = LocalKMS()
# generate a default key on startup
kms.generate_key("default")
