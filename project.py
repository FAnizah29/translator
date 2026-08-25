import deepl
client = deepl.DeepLClient("18e8255e-5299-4c46-b844-bf3a75308eb1:fx")


#translators
def translate_ar(term):
    return client.translate_text(
        term,
        source_lang="AR",
        target_lang="EN-US"
    ).text
def translate_en(term):
    return client.translate_text(
        term,
        source_lang="EN",
        target_lang="AR"
    ).text 

