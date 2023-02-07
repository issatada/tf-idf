from sklearn.feature_extraction.text import TfidfVectorizer
from janome.tokenizer import Tokenizer
import re
import pandas as pd
import codecs
from collections import Counter


class TfIdf:
    def __init__(self) -> object:
        """
        コンストラクタ
        """

        # 分かち書きの文書を保持する変数
        self.separation_docs = {}
        self.df = None

    def create(self):
        """
        TF-IDFの実行
        """

        # TF-IDFの実行
        names, values = self.create_model(self.separation_docs.values())
        # 結果をDataFrameに格納
        self.df = pd.DataFrame(values, columns=names, index=self.separation_docs.keys())

        return self.df

    def word_separation(self, text):

        """
       形態素解析により一般名詞と固有名詞のリストを作成

       ---------------
       Parameters:
           text : str         テキスト
       """

        token = Tokenizer().tokenize(text)
        words = []


        _proper_noun = ""

        for line in token:
            tkn = re.split('\t|,', str(line))

            if tkn[1] == '名詞' and tkn[2] != '非自立' and tkn[2] != '代名詞' and tkn[2] != '接尾':
                _proper_noun += tkn[0]


            else:
                if _proper_noun:
                    words.append(_proper_noun)
                _proper_noun = ""
        print(words)

        return ' '.join(words)


    def create_model(self, separating_docs):
        """
        TF-IDFの計算を行う

        ---------------
        Parameters:
            documents : [str]  分かち書きされた文書のリスト
        """
        # モデルの生成
        vectorizer = TfidfVectorizer(smooth_idf=False)
        # TF-IDF行列の計算
        values = vectorizer.fit_transform(separating_docs).toarray()
        # 特徴量ラベルの取得
        feature_names = vectorizer.get_feature_names_out()

        return feature_names, values

    def add_file(self, title, filename, encoding='utf-8'):
        """
        ファイルの読み込み

        Parameters:
        --------
            filename : str   TF-IDFしたい文書が書かれたファイル名
        """
        with codecs.open(filename, 'r') as f:
            self.add_document(title, f.read())

    def add_document(self, title, document):
        '''
        テキストの読み込み

        Parameters:
        --------
            document : str   TF-IDFしたい文書
        '''
        # 形態素解析で分かち書きした文書をインスタンス変数に格納
        self.separation_docs[title] = self.word_separation(document)

    def top_words(self, cnt=10):
        '''
        TF-IDF 上位ｎの取得

        Parameters:
        --------
            cnt : int   上位からの取得件数
        '''
        res = {}
        for num, title in enumerate(self.separation_docs.keys()):
            res[title] = (self.df[num:num + 1].T.sort_values(by=title, ascending=False).head(cnt)).rename(
                columns={title: 'TFIDF'})
        return res

    def word_count(self, cnt=10):
        '''
        出現回数上位ｎの取得

        Parameters:
        --------
            cnt : int   上位からの取得件数
        '''
        res = {}
        for key, value in self.separation_docs.items():
            data = Counter(value.split(' ')).most_common(cnt)
            res[key] = pd.DataFrame([v for k, v in data], columns=['Count'], index=[k for k, v in data])
        return res
