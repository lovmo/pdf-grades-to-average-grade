from PyPDF2 import PdfFileReader
from statistics import mean
from tkinter import filedialog
from tkinter import *
import yagmail
import collections


def send_mail(mail, text, grades):
    receiver = mail
    body = f'Du har et snitt på: {text:.2f}.\nDette tilsvarer: \nA:{grades.get(5, 0)}\nB:{grades.get(4, 0)}\nC:{grades.get(3, 0)}\nD:{grades.get(2, 0)}\nE:{grades.get(1, 0)}\nF:{grades.get(0, 0)} '

    print(receiver)
    print(body)

    yag = yagmail.SMTP("ven.uib.sv@gmail.com", 'skolen123')
    yag.send(
        to=receiver,
        subject="Ditt snitt",
        contents=body,
    )


def konvertering(inp):
    grade = inp[3]
    if grade == 'A':
        return 5
    if grade == 'B':
        return 4
    if grade == 'C':
        return 3
    if grade == 'D':
        return 2
    if grade == 'E':
        return 1
    if grade == 'F':
        return 0


class Vitnemål:

    def __init__(self, master):
        self.master = master
        self.antall = ''
        self.snitt_ut = ''

        self.output_text = StringVar()
        self.output_text_karakterer = StringVar()

        self.hent_fil_bt = Button(self.master, text='Velg fil', width=25, bg='#176db7', fg='#f3f3f3',
                                  command=lambda: self.insert_pdf())
        self.hent_fil_bt.grid(row=2, column=4)

        self.snitt = Label(self.master, textvariable=self.output_text)
        self.snitt.grid(row=3, columnspan=15)

        self.ant_karakterer = Label(self.master, textvariable=self.output_text_karakterer)
        self.ant_karakterer.grid(row=4, columnspan=15)

        self.email = Entry(self.master, width=25)
        self.email.grid(row=6, columnspan=15)

        self.send = Button(self.master, text='Send til mail', width=25,
                           command=lambda: send_mail(self.email.get(), self.snitt_ut, self.antall))
        self.send.grid(row=7, column=4)

    def insert_pdf(self):
        self.file = filedialog.askopenfilename(initialdir="/", title="Select file",
                                               filetypes=(("pdf files", "*.pdf"), ("all files", "*.*")))
        self.extract_information()

    def extract_information(self):
        with open(self.file, 'rb') as vitne_portalen:
            pdf = PdfFileReader(vitne_portalen)
            informasjon = pdf.getPage(0)
            emner = informasjon.extractText()
            emner = emner.split(' ')
            print(emner)
            fornavn = emner[0]
            start_slice = emner.index('studiepoeng/stp)Karakter-fordelingEmneTerminPoengKarakterABCDEMRK') + 1
            slutt_slice = emner[1:].index(fornavn) + 1
            emner = emner[start_slice:slutt_slice]
            # emner.extend(['201810', 'stpDGEO', '201910', 'stpEINFO'])     #En måte å sjekke om flere fagkoder funker
            karakterer = []
            for i in emner:
                if i[:3] == 'stp':  # Finner alle elementetene som starter på 'stp'

                    # BI har 7,5 og 15 stp pr fag
                    index = emner.index(i) - 1
                    if emner[index].endswith('7,5'):
                        karakterer.append(emner.pop(index + 1))
                    elif emner[index].endswith('15'):
                        karakterer.append(i)
                        karakterer.append(i)

                    # UIB operer med 10 og 20 stp pr fag
                    elif emner[index].endswith('10'):
                        karakterer.append(i)
                    elif emner[index].endswith('20'):
                        karakterer.append(i)
                        karakterer.append(i)

            karakterer_tall = [konvertering(i) for i in karakterer]
            antall = collections.Counter(karakterer_tall)
            self.antall = antall
            self.snitt_ut = mean(karakterer_tall)
            self.output_text.set(f'Ditt snitt: {mean(karakterer_tall):.3f}')
            self.output_text_karakterer.set(
                f'A:{antall.get(5, 0)}, B:{antall.get(4, 0)}, C:{antall.get(3, 0)}, D:{antall.get(2, 0)}, E{antall.get(1, 0)}, F{antall.get(0, 0)}')


vitne = Tk()
vitne.tk.call('tk', 'scaling', 4.0)
vitnemål_gui = Vitnemål(vitne)
vitne.mainloop()
