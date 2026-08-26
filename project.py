import deepl
from langdetect import detect
import sys
import csv

client = deepl.DeepLClient("18e8255e-5299-4c46-b844-bf3a75308eb1:fx")


class Term:
    subjects = {"math", "biology", "chemistry", "physics", "literature"}
    langs = {
        "arabic": "AR",
        "bulgarian": "BG",
        "czech": "CS",
        "danish": "DA",
        "german": "DE",
        "greek": "EL",
        "english": "EN",
        "english (uk)": "EN-GB",
        "english (us)": "EN-US",
        "spanish": "ES",
        "spanish (latin america)": "ES-419",
        "estonian": "ET",
        "finnish": "FI",
        "french": "FR",
        "hebrew": "HE",
        "hungarian": "HU",
        "indonesian": "ID",
        "italian": "IT",
        "japanese": "JA",
        "korean": "KO",
        "lithuanian": "LT",
        "latvian": "LV",
        "norwegian bokmål": "NB",
        "dutch": "NL",
        "polish": "PL",
        "portuguese": "PT",
        "portuguese (brazil)": "PT-BR",
        "portuguese (portugal)": "PT-PT",
        "romanian": "RO",
        "russian": "RU",
        "slovak": "SK",
        "slovenian": "SL",
        "swedish": "SV",
        "thai": "TH",
        "turkish": "TR",
        "ukrainian": "UK",
        "vietnamese": "VI",
        "chinese": "ZH",
        "chinese (simplified)": "ZH-HANS",
        "chinese (traditional)": "ZH-HANT",
    }

    def __init__(self, term, subject, og_lang, trans_lang):
        self._ogterm = term
        if subject.lower() not in Term.subjects:
            sys.exit(
                "Please Choose Between The Following Subjects: Math, Biology, Chemistry, Physics, Literature"
            )
        self._subject = subject
        if og_lang.lower() and trans_lang.lower() not in Term.langs:
            sys.exit("Please Choose a Supported Language")
        self._og_lang = Term.langs[og_lang]
        self._trans_lang = Term.langs[trans_lang]

    @property
    def ogterm(self):
        return self._ogterm

    @property
    def trans_lang(self):
        return self._trans_lang

    @property
    def subject(self):
        return self._subject

    @property
    def og_lang(self):
        return self._og_lang

    @property
    def trans_lang(self):
        return self._trans_lang

    def translate(self):
        self._trns_term = client.translate_text(
            self._ogterm,
            source_lang=self._og_lang,
            target_lang=self._trans_lang,
            context=self._subject,
        ).text
        return self._trns_term

    def send_term(self):
        with open(
            f"{self._subject}_{self._og_lang}.csv", "a", encoding="utf-8"
        ) as file:
            writer = csv.writer(file, delimiter="-")
            writer.writerow((self._ogterm, self._trns_term))


def quiz(subject, oglang):
    with open(f"{subject}_{oglang}.csv", encoding="utf-8") as file:
        lines = file.readlines()
        for line in map(str.strip, lines):
            print(line)
            og_term, trans_term = line.split("-")
            for attempt in range(3):
                correct = f"{og_term}--> {trans_term} "
                answer = input(f"{og_term}--> \n")

                if answer == trans_term:
                    print("correct")
                    break
                else:

                    if attempt == 2:
                        print("Wrong final")
                        print(correct)
                    else:
                        print("wrong")


new_term = Term("قانون الاحتكاك", "physics", "arabic", "english (us)")
new_term.translate()
new_term.send_term()

quiz(new_term._subject, new_term._og_lang)
