from django.apps import AppConfig


class TicketsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tickets"

    # Needed for the signal to work
    def ready(self):
        import tickets.signals 
        
        # The tickets are gonna be updated from the inbox using a background threat
        import os
        if os.environ.get('RUN_MAIN') == 'true':
            
            import threading
            from mailing.fetch_tickets import start_email_fetcher
            fetch_thread = threading.Thread(target=start_email_fetcher, daemon=True)
            fetch_thread.start()
