from sourcecode import TfIdf

tf = TfIdf()
tf.add_file('サンプル文章', "database.txt")
tf.create()
print(tf.top_words())
print(tf.word_count())