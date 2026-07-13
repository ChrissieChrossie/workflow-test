import requests
from bs4 import BeautifulSoup
import time
import sys
from datetime import datetime
import json

#Ein altes Skript von mir, dass nach Discord sachen schicken kann, wenn ein Ticket vorhanden war
#
def check_tickets(url):
    """Prüft ob Tickets verfügbar sind"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        

        tickets = soup.find_all('div', class_='item')
        
        if not tickets:

            tickets = soup.find_all('tr', class_='product')
        
        available_tickets = []
        for ticket in tickets:

            title = ticket.find(['h3', 'td', 'span'], class_=['title', 'product-name'])
            price = ticket.find(['span', 'td'], class_=['price', 'product-price'])
            
            if title:
                ticket_info = {
                    'title': title.get_text(strip=True),
                    'price': price.get_text(strip=True) if price else 'Preis unbekannt'
                }
                available_tickets.append(ticket_info)
        
        return available_tickets, response.text
        
    except Exception as e:
        print(f"Fehler beim Abrufen der Seite: {e}")
        return None, None

def send_discord_notification(tickets, webhook_url):
    """Sendet eine Discord-Benachrichtigung via Webhook"""
    if not webhook_url:
        return
    
    try:
        embed = {
            "title": "🎫 39C3 Tickets verfügbar!",
            "color": 3447003,  # Blau
            "timestamp": datetime.utcnow().isoformat(),
            "fields": [],
            "footer": {
                "text": "39C3 Ticket Checker"
            }
        }
        
        for i, ticket in enumerate(tickets, 1):
            embed["fields"].append({
                "name": f"Ticket {i}",
                "value": f"**{ticket['title']}**\nPreis: {ticket['price']}",
                "inline": False
            })
        
        embed["fields"].append({
            "name": "Link",
            "value": f"[Zum Ticketshop]({URL})",
            "inline": False
        })
        
        payload = {
            "embeds": [embed],
            "username": "39C3 Ticket Bot"
        }
        
        response = requests.post(webhook_url, json=payload)
        
        if response.status_code == 204:
            print("✓ Discord-Benachrichtigung gesendet")
        else:
            print(f"✗ Discord-Fehler: {response.status_code}")
            
    except Exception as e:
        print(f"Fehler beim Senden der Discord-Nachricht: {e}")

def send_notification(tickets):
    """Gibt eine Benachrichtigung aus"""
    print("\n" + "="*60)
    print(f"🎫 TICKETS VERFÜGBAR! ({datetime.now().strftime('%H:%M:%S')})")
    print("="*60)
    for i, ticket in enumerate(tickets, 1):
        print(f"\n{i}. {ticket['title']}")
        print(f"   Preis: {ticket['price']}")
    print("\n" + "="*60)
    print(f"Link: {URL}")
    print("="*60 + "\n")
    
    try:
        import os
        if sys.platform == 'darwin':  # macOS
            os.system(f'osascript -e \'display notification "Tickets verfügbar!" with title "39C3 Ticket Alert"\'')
        elif sys.platform == 'linux':  # Linux
            os.system(f'notify-send "39C3 Ticket Alert" "Tickets verfügbar!"')
    except:
        pass  # Benachrichtigung optional

def send_test_notification(webhook_url):
    """Sendet eine Test-Benachrichtigung"""
    test_tickets = [
        {
            'title': 'Test-Ticket 39C3',
            'price': '150,00 €'
        }
    ]
    
    print("\n📨 Sende Test-Benachrichtigung...")
    send_notification(test_tickets)
    
    if webhook_url:
        send_discord_notification(test_tickets, webhook_url)
        print("✓ Test abgeschlossen! Prüfe Discord für die Nachricht.\n")
    else:
        print("⚠ Kein Discord-Webhook konfiguriert.\n")

def main():
    global URL
    URL = "https://tickets.events.ccc.de/39c3/secondhand/?item=&sort=price_asc"
    CHECK_INTERVAL = 60 
    
    DISCORD_WEBHOOK ="https://discordapp.com/api/webhooks/1450019238457905236/w1NTyvir1axOcKckYUrRrVVT5Pl9cZT3wQM1jaRu83mF2sI3ZmkOk9B2EikdjPGuOwOM" 
    

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        send_test_notification(DISCORD_WEBHOOK)
        return
    
    print("39C3 Ticket Checker gestartet")
    print(f"URL: {URL}")
    print(f"Prüfintervall: {CHECK_INTERVAL} Sekunden")
    if DISCORD_WEBHOOK:
        print("Discord-Benachrichtigungen: Aktiviert ✓")
    else:
        print("Discord-Benachrichtigungen: Deaktiviert (Webhook fehlt)")
    print("\n💡 Tipp: Starte mit 'python ticket_checker.py --test' für eine Test-Nachricht")
    print("Drücke Ctrl+C zum Beenden\n")
    
    last_count = 0
    
    try:
        while True:
            tickets, html = check_tickets(URL)
            
            if tickets is not None:
                current_count = len(tickets)
                
                if current_count > 0:
                    if current_count != last_count:
                        send_notification(tickets)
                        send_discord_notification(tickets, DISCORD_WEBHOOK)
                        last_count = current_count
                    else:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] {current_count} Ticket(s) verfügbar (keine Änderung)")
                else:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Keine Tickets verfügbar")
                    last_count = 0
            
            time.sleep(CHECK_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n\nChecker beendet.")

if __name__ == "__main__":
    main()