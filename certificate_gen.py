import smtplib
import ssl
import email
import os
import csv
import sys

from PIL import Image, ImageDraw, ImageFont


from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Certificates:
    def __init__(self):
        self.totals = []
        self.emails = []
        self.names = []

        self.email_loaction = 0
        self.name_location = 0

        self.path = ''

        self.text_x = 0
        self.text_y = 0
        self.size = 30

        self.sample = False
        self.satisfied = 0

        self.msg = MIMEMultipart()
        self.counts = 0
        self.counts_1 = 0

        self.font_path = 'C:/Windows/Fonts/Arial/ariblk.ttf'

    def _draw(self, certificate_file, name):
        try:
            self.font_path = 'C:/Windows/Fonts/Arial/ariblk.ttf'
            completePath = os.path.join(self.path, name)
            img = Image.open(certificate_file, mode='r')
            image_width = img.width
            image_height = img.height
            draw = ImageDraw.Draw(img)

            font = ImageFont.truetype(self.font_path, size=self.size)
            text_width, _ = draw.textsize(name, font=font)
            draw.text(
                (
                    (image_width - (text_width - self.text_x)) / 2,
                    self.text_y
                ),
                name,
                fill='rgb(0, 0, 0)',
                font=font)
            self.counts += 1
            img.save("{}.png".format(completePath))
            print(f'{name} --------> {self.counts}')

        except FileNotFoundError:
            print('\nPlease check your filename!!!')
            sys.exit(0)

    def _createPath(self):
        try:
            if self.path == '':
                self.path = os.path.join(os.getcwd(), 'certificates')
                os.mkdir(self.path)
        except FileExistsError:
            return

    def _send_mails(self, username, password, subject, body):
        if self.emails == []:
            print('\nNo mail Ids are provided to send the mails')
            return False
        else:
            port = 587
            totals = len(self.emails)
            try:
                server = smtplib.SMTP('smtp.gmail.com', port)
                server.starttls()
                server.login(username, password)
                addImages = (int(input(
                    '\nDo you want to attach Certificates to the mails (1 for yes | 0 for no) : ')))

                for i in range(len(self.emails)):

                    self.msg['From'] = username
                    self.msg['To'] = self.emails[i]
                    self.msg['Subject'] = subject

                    self.msg.attach(MIMEText(body, 'plain'))

                    if(addImages == 1):
                        filename = os.path.join(
                            self.path, self.names[i]+'.png')
                        attachment = open(filename, 'rb')
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload((attachment).read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition',
                                        "attachment; filename= "+filename)

                        self.msg.attach(part)

                    text = self.msg.as_string()
                    server.sendmail(username, self.emails[i], text)

                    self.counts_1 += 1
                    print(
                        f'{self.counts_1} / {totals} --------- {self.emails[i]}')

                    return True
            except smtplib.SMTPAuthenticationError:
                print('Please Check your username and Password, \n\n And make sure you have turned on the allow less secure apps for your account')
                return False
            except:
                return False
            finally:
                server.quit()

    def renderCertificate(self, certificate_file):
        if len(self.names) > 0 and ('.png' in certificate_file or '.jpeg' in certificate_file):
            self._createPath()
            while(not self.sample):
                print('\n**************************')
                try:
                    self.text_x = int(input(
                        "\nEnter the x position (default = 0 | to continue with default press Enter) : "))
                except ValueError:
                    self.text_x = 0

                try:
                    self.text_y = int(
                        input('\nPlease enter a Text y position : (300-500) - please experiment it : '))
                except ValueError:
                    self.text_y = 300

                try:
                    self.size = int(input(
                        '\nPlease provide a text size (default value is 30), press enter to Continue : '))
                except:
                    self.size = 30

                self._draw(certificate_file, self.names[0])

                print(
                    '\nPlease preview your certificate sample in the images folder in the root directory of the program')
                print('\n**************************')
                try:
                    self.satisfied = int(input(
                        '\n Press (1 to proceed to all files) else (0 to re render the certificate) [ 1 - proceed || 0 - re-render ] : '))
                    if(self.satisfied):
                        self.sample = True
                except ValueError:
                    self.satisfied = 0

            for name in self.names:
                self._draw(certificate_file, name)
        print('Please check your certificate filename!!')
        return

    def read_csv(self, filename, getEmails=True, getNames=True, encoding_f='utf-8'):
        try:
            with open(filename, encoding=encoding_f) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')

                for i in csv_reader:
                    self.totals.append(i)

                for i in self.totals[0]:
                    x = ''.join(i.split())
                    x = x.lower()
                    if x == 'emailaddress' or x == 'email' or x == 'emailid':
                        self.email_loaction = self.totals[0].index(i)
                    elif x == 'name' or x == 'fullname' or x == 'full-name':
                        self.name_location = self.totals[0].index(i)

                self.totals.pop(0)
                if getNames and getEmails:
                    for i in self.totals:
                        if i[self.name_location] != '':
                            self.names.append(i[self.name_location])
                            self.emails.append(i[self.email_loaction])
                elif getEmails:
                    for i in self.totals:
                        self.emails.append(i[self.email_loaction])
                else:
                    for i in self.totals:
                        self.names.append(i[self.name_location])
                csv_file.close()
                print('\n******************')
                print('\nFile Read Successful')
                return True
        except UnicodeDecodeError:
            print(
                '\nplease try passing this parameter to the read_csv\n\n self.read_csv(filename, \'latin-1\')')
            return False
        except:
            print(
                '\nPlease check your filename, make sure it is in the root folder of the program !!')
            return False


class Mailer(Certificates):
    def __init__(self):
        self.username = ''
        self.password = ''
        self.subject = ''
        self.body = ''
        Certificates.__init__(self)

    def send_mail(self):
        if(self.username and self.password and self.subject and self.body):
            if self._send_mails(self.username, self.password, self.subject, self.body):
                print('\nCompleted Sending all Mails !!')
                return
        print('\nSome Error has occured')
        return
