import email as email_module
import email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import datetime
import csv
import datetime
import email as email_module
import time
import schedule

#Dosya adını belirliyor
def generate_file_path():
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    file_path = f'{current_date}.csv'
    print(f"Required File Name:{file_path}")
    
        # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Warning:{file_path} does not exist. File path has to be named as the current date value.")
    
    return file_path

def get_items_from_csv(file_path):
    items = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip header row 
        for row in reader:
            if row:
                items.append(row)
    return items

def process_items(items):
    for item in items:
        email_address = item[0]
        clock_in_time = item[1]
        
        if not email_address or not email_address.strip():  # E-posta adresi boş veya geçersizse atla
            print("Geçersiz veya boş e-posta adresi. İşlem atlandı.")
            continue
        
        #Çıkış zamanı hesaplama
        clock_out_datetime = calculate_clock_out_time(clock_in_time)
        today = datetime.datetime.now()
            
    return clock_out_datetime, email_address

def calculate_clock_out_time(clock_in_time):
    try:
        # Giriş saatinin çıkış saati olarak işlenmesi
        clock_in_datetime = datetime.datetime.strptime(clock_in_time, '%I:%M:%S %p')
        clock_out_datetime = clock_in_datetime + datetime.timedelta(hours=9, minutes=45)
        clock_out_datetime = clock_out_datetime.replace(year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day)
        print(f"Calculated Clock Out Time: {clock_out_datetime}")
        print(type(clock_out_datetime))
        return clock_out_datetime
    except ValueError:
        print("Geçersiz saat formatı. Saati kontrol ediniz.")
        return clock_out_datetime
    

def create_event(email_address, clock_out_datetime):
    CRLF = "\r\n"

    # SMTP server configuration
    sender = " "
    smtp_server = " "
    smtp_port = 
    username = " "
    password = " "

    # Meeting details
    organizer = "ORGANIZER;CN=:mailto: mailBody" + CRLF + "mail domain" #mailBody and mail domain is your sender mails parsed version
    fro = "Bilgilendirme <fixed-term.mert.dogan2@tr.bosch.com>"

    ddtstart = clock_out_datetime #event saati
    ddtstart = ddtstart + datetime.timedelta(hours = -3) ############### Bu NE Lannnn
    dtend = ddtstart + datetime.timedelta(hours=0.25) #event süresi
    dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S") #davetiyenin oluşturulduğu tarih
    dtstart = ddtstart.strftime("%Y%m%dT%H%M%S") #toplantı başlangıç tarihi ve saati
    dtend = dtend.strftime("%Y%m%dT%H%M%S") #toplantı bitiş tarihi ve saati

    description = "DESCRIPTION: test invitation from pyICSParser" + CRLF
    attendee = "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE" + CRLF + ";CN=" + str(email_address) + ";X-NUM-GUESTS=0:" + CRLF + " mailto:" + str(email_address) + CRLF
    ical = "BEGIN:VCALENDAR" + CRLF + "PRODID:pyICSParser" + CRLF + "VERSION:2.0" + CRLF + "CALSCALE:GREGORIAN" + CRLF
    ical += "METHOD:REQUEST" + CRLF + "BEGIN:VEVENT" + CRLF + "DTSTART:" + dtstart + CRLF + "DTEND:" + dtend + CRLF + "DTSTAMP:" + dtstamp + CRLF + organizer + CRLF
    ical += "UID:FIXMEUID" + dtstamp + CRLF
    ical += attendee + "CREATED:" + dtstamp + CRLF + description + "LAST-MODIFIED:" + dtstamp + CRLF + "LOCATION:" + CRLF + "SEQUENCE:0" + CRLF + "STATUS:CONFIRMED" + CRLF
    ical += "SUMMARY:Yasal Çalışma Süresi Hatırlatmaaa " + CRLF + "TRANSP:OPAQUE" + CRLF + "END:VEVENT" + CRLF + "END:VCALENDAR" + CRLF

    eml_body = f"Değerli çalışanımız,\nYasal Çıkış Saatiniz: {clock_out_datetime.strftime('%H:%M:%S')}" # Write your message here
    eml_body_bin = "This is the email body in binary - two steps"
    msg = MIMEMultipart('mixed')
    msg['Reply-To'] = " " #Write your sender mail address
    msg['Date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg['Subject'] = "Yasal Çalışma Süresi Hatırlatma" # Mail Konusu
    msg['From'] = fro
    msg['To'] = email_address

    part_email = MIMEText(eml_body, "plain")
    part_cal = MIMEText(ical, 'calendar;method=REQUEST')

    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)

    ical_atch = MIMEBase('application/ics', ' ;name="%s"' % ("invite.ics"))
    ical_atch.set_payload(ical)
    encoders.encode_base64(ical_atch)
    ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"' % ("invite.ics"))

    eml_atch = MIMEText('', 'plain')
    encoders.encode_base64(eml_atch)
    eml_atch.add_header('Content-Transfer-Encoding', "")

    msgAlternative.attach(part_email)
    msgAlternative.attach(part_cal)
    msg.attach(ical_atch)

    # SMTP server connection and email sending
    mailServer = smtplib.SMTP(smtp_server, smtp_port)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(username, password)
    mailServer.sendmail(fro, [email_address], msg.as_string())
    mailServer.close()

    print("Event and Email Sent")
    print(f"clock_out_datetime is: {clock_out_datetime}")
    print(f"dtsatrt is :{dtstart}")
    print(f"email_address Type is :{email_address}")
    print(type(email_address))
    print(f"Email Address: {email_address}")
    return dtstart

def start_event_at_a_time(create_event):
    # Verilen dosya yoluyla işlenen verileri al
    file_path = generate_file_path()
    items = get_items_from_csv(file_path)
    
    # Verilen verileri işle ve gerekli bilgileri al
    clock_out_datetime, email_address = process_items(items)
    
    # Dışarıdan alınan create_event_func fonksiyonunu çağır ve gerekli bilgileri geçir
    create_event(email_address, clock_out_datetime)
    
# Example usage
def main():
    schedule.every().day.at("09:10").do(start_event_at_a_time, create_event)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
