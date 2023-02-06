import spacy


def text2propns(text: object, min_nouns_length: object = 2) -> object:
    """文章から固有名詞を抽出する。
    :rtype: object
    """
    nouns = []  # 一般名詞のリスト
    propns = []  # 固有名詞のリスト
    # print(text)

    for token in generate_tokens(text):
        # print(token,token.pos_)
        pos = token.pos_  # 単語の品詞

        # 一般名詞のとき
        if pos == "NOUN":
            nouns.append(token.orth_)

        # 固有名詞のとき
        elif pos == "PROPN":
            propns.append(token.orth_)
            commit_nouns(propns, nouns, min_nouns_length)

        # 上記以外のとき
        else:
            commit_nouns(propns, nouns, min_nouns_length)

    commit_nouns(propns, nouns, min_nouns_length)
    propns = format_list(propns)
    return propns


def generate_tokens(text):
    """文章から抽出した単語のイテレータを生成する。
    """
    ginza = spacy.load("ja_ginza")  # GiNZA
    doc = ginza(text)

    for sent in doc.sents:
        for token in sent:
            yield token


def commit_nouns(propns, nouns, min_nouns_length=2):
    """条件を満たす一般名詞を固有名詞に登録する。
    """
    # 名詞が一定数連続しているとき
    if len(nouns) >= min_nouns_length:
        propn = "".join(nouns)  # 連続した一般名詞を結合して固有名詞とする
        propns.append(propn)

    nouns.clear()  # 登録した一般名詞を削除


def format_list(array):
    """リストの要素を一意にしてソートする。
    """
    array = set(array)  # リストの要素を一意にする
    array = list(array)
    array = sorted(array)
    return array



# text = "Python × GiNZAで固有名詞を抽出してみる"
# text2propns(text, min_nouns_length=2)

# chiVe
# from gensim.models import KeyedVectors
#
# nlp = spacy.load('ja_ginza')
# chive_vectors = KeyedVectors.load_word2vec_format("./database.txt", binary=False)  # モデル読み込み
# # ベクトル入れ替え
# nlp.vocab.reset_vectors(width=chive_vectors.vectors.shape[1])
# for word in chive_vectors.vocab.keys():
#     nlp.vocab[word]
#     nlp.vocab.set_vector(word, chive_vectors[word])
#
# print(text2propns("./database2.txt"))


#chive_vectors = KeyedVectors.load_word2vec_format('./chive-1.1-mc5-20200318.txt', binary=False)  # モデル読み込み