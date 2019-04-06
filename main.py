import os
import genanki
import unicodedata

# one of: simplified, traditional, both
charset = 'simplified'

# exclude hsk entries that are a single character
exclude_single_character = False

# max hsk level to include in deck (inclusive)
max_hsk_level = 6

templates = []

afmt = '{{FrontSide}}<hr id="answer"><span class="pinyin">{{pinyin}}</span><div>{{englishdef}}</div></span>'
css = '''
.card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
}

.character {
    text-align: center;
    color: #000000;
    font-size: 200px;
    text-decoration: none;
    lang: zh;
}

.pinyin {
    word-wrap: break-word;
    font-family: arial;
    font-size: 28px;
    font-weight: bold;
    text-decoration: none;
}
'''

if charset == 'simplified' or charset == 'both':
    templates.append({
        'name': '简体汉字->拼音和英语定义',
        'qfmt': '<div class="character">{{simplified}}</div>',
        'afmt': afmt
    })

if charset == 'traditional' or charset == 'both':
    templates.append({
        'name': '繁体汉字->拼音和英语定义',
        'qfmt': '<div class="character">{{traditional}}</div>',
        'afmt': afmt
    })

hsk_model = genanki.Model(
    2091109748,
    'HSK model',
    fields=[
        {'name': 'simplified'},
        {'name': 'traditional'},
        {'name': 'pinyin'},
        {'name': 'englishdef'},
        {'name': 'hsklevel'},
    ],
    templates=templates,
    css=css)

deck = genanki.Deck(1551711109, 'HSK 1-6 ' + charset)

total = 0
for i in range(1, max_hsk_level + 1):
    with open('data/hsk{}.txt'.format(i)) as fp:
        for line in fp:
            zhsimp, zhtrad, _, pinyin, defn = line.split('\t')
            if sum([unicodedata.category(c) == 'Lo' for c in zhsimp]) == 1 and exclude_single_character:
                continue
            note = genanki.Note(
                model=hsk_model,
                fields=[zhsimp, zhtrad, pinyin, defn, str(i)])
            deck.add_note(note)
            total += 1

print('Created deck with {} notes'.format(total))
genanki.Package(deck).write_to_file('hsk1-6_{}.apkg'.format(charset))
