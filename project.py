import deepl
import sys
import csv
import os
from tabulate import tabulate

client = deepl.DeepLClient("18e8255e-5299-4c46-b844-bf3a75308eb1:fx")
subjects = {"math", "biology", "chemistry", "physics", "literature"}
deepl_langs = {
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


def main():
    try:
        while True:
            table()
    except KeyboardInterrupt:
        sys.exit("\nGoodbye....")


def table():
    table = [["1", "Translate Term"], ["2", "Quiz"], ["3", "Exit"]]
    choice = input(f"{tabulate(table, tablefmt="double_outline")}\nChoose an option: ")
    if choice in ["1", "2", "3"]:
        if choice == "1":
            info = get_term_info()
            new_term = Term(*info)
            new_term.translate()
            new_term.send_term()
        elif choice == "2":
            subject = validate(
                "Please choose from the following: Math, Biology, Physics, Chemistry, Literature\n",
                subjects,
                lower=True,
            )
            oglang = deepl_langs[
                validate("Provide a language to translate from: ", deepl_langs)
            ]
            translang = validate("Provide a language to translate to: ", deepl_langs)
            if translang == "english":
                translang = deepl_langs["english (us)"]
            else:
                translang = deepl_langs[translang]
            quiz(subject, oglang, translang)
        else:
            sys.exit("Goodbye!")


def get_term_info():
    term = input("Term: ")
    subject = validate(
        "Please choose from the following: Math, Biology, Physics, Chemistry, Literature\n",
        subjects,
        lower=True,
    )
    oglang = deepl_langs[
        validate("Provide a language to translate from: ", deepl_langs)
    ]
    translang = validate("Provide a language to translate to: ", deepl_langs)
    if translang == "english":
        translang = deepl_langs["english (us)"]
    else:
        translang = deepl_langs[translang]

    return [term, subject, oglang, translang]


def validate(msg, data2, lower=False):
    while True:
        if not lower:
            data1 = input(msg).strip()
        else:
            data1 = input(msg).lower().strip()
        if data1 in data2:
            return data1


class Term:

    def __init__(self, term, subject, og_lang, trans_lang):
        self.ogterm = term
        self.subject = subject
        self.og_lang = og_lang
        self.trans_lang = trans_lang

        return self._trans_lang

    def translate(self):
        self.trns_term = client.translate_text(
            self._ogterm,
            source_lang=self.og_lang,
            target_lang=self.trans_lang,
            context=self._subject,
        ).text
        return self.trns_term

    def send_term(self):
        file_name = f"{self.subject}_{self.og_lang}_{self.trans_lang}.csv"
        file_exists = os.path.exists(file_name)
        file_is_empty = not file_exists or os.path.getsize(file_name) == 0
        fieldnames = ["Original", "Translated"]
        stored = {"Original": self.ogterm, "Translated": self.trns_term}
        with open(
            file_name,
            "a",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=",")
            if file_is_empty:
                writer.writeheader()

            writer.writerow(stored)


def quiz(subject, oglang, translang):
    file_name = f"{subject}_{oglang}_{translang}.csv"
    if not os.path.exists(file_name):
        print("File does not exist!")
        return
    elif os.path.getsize(file_name) == 0:
        print("File is empty!")
        return
    with open(file_name, encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            og_term, trans_term = row["Original"], row["Translated"]
            correct = f"{og_term}--> {trans_term}"
            for attempt in range(3):
                answer = input(f"{og_term}--> \n").strip()

                if answer == trans_term.strip():
                    print("correct")
                    break
                else:
                    if attempt == 2:
                        print("Wrong final")
                        print(correct)
                    else:
                        print("wrong")

if __name__ == "__main__":
    main()
