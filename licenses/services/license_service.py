# licenses/services/license_service.py
import json
from pathlib import Path
from datetime import datetime, timedelta
from django.utils import timezone

LICENSE_PATH = Path("/app/license.json")

class LicenseService:
    _cached = None

    @classmethod
    def get_valid_until(cls):
        if cls._cached:
            return cls._cached

        if not LICENSE_PATH.exists():
            return None

        try:
            with open(LICENSE_PATH) as f:
                data = json.load(f)
            date = datetime.strptime(data["valid_until"], "%Y-%m-%d").date()
            cls._cached = date
            return date
        except Exception as e:
            print(f"[LICENSE ERROR] {e}")
            return None

    @classmethod
    def get_status(cls):
        """
        Возвращает: 'ok' | 'warning' | 'grace' | 'expired'
        """
        valid_until = cls.get_valid_until()
        if not valid_until:
            return 'expired'

        today = timezone.localdate()
        if today <= valid_until:
            days_left = (valid_until - today).days
            if days_left <= 5:
                return 'warning'
            return 'ok'
        elif today <= valid_until + timedelta(days=3):
            return 'grace'
        return 'expired'

    @classmethod
    def get_days_left(cls):
        valid_until = cls.get_valid_until()
        if not valid_until:
            return 0
        today = timezone.localdate()
        return (valid_until - today).days