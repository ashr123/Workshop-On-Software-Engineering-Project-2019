# from spellchecker import Spellchecker
#
# spell = Spellchecker()
#
# # find those words that may be misspelled
# misspelled = spell.unknown(['Let', 'us', 'wlak', 'on', 'the', 'groun'])
#
#
#
#
#
#
#
# def get_correct_word(word):
# 	misspelled = spell.unknown([word])
# 	for word in misspelled:
# 		coorect = spell.correction(word)
# 	return coorect[0]
#
#
# print(get_correct_word('yuu'))

from spellchecker import Spellchecker

spell = Spellchecker

# find those words that may be misspelled
misspelled = spell.unknown(['let', 'us', 'wlak','on','the','groun'])

for word in misspelled:
    # Get the one `most likely` answer
    print(spell.correction(word))

    # Get a list of `likely` options
    print(spell.candidates(word))