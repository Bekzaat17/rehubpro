from licenses.services.license_notifier import LicenseNotifier

def check_license_expiration():
    LicenseNotifier().run()