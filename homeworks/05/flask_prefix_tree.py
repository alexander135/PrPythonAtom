from flask import Flask, request, jsonify, json
import operator

app = Flask(__name__)


class PrefixTree:
    # TODO реализация класса prefix tree, методы как на лекции + метод дать топ 10 продолжений. Скажем на строку кросс выдаем кроссовки, кроссовочки итп. Как хранить топ?
    # Решать вам. Можно, конечно, обходить все ноды, но это долго. Дешевле чуток проиграть по памяти, зато отдавать быстро (скажем можно взять кучу)
    # В терминальных (конечных) нодах может лежать json с топ актерами.

    def __init__(self):
        self.root = [{}]

    def add(self, string, top):
        if self.check(string):
            return
        wrk_dict = self.root
        for i in string:
            if i in wrk_dict[0]:
                wrk_dict = wrk_dict[0][i]
            else:
                wrk_dict[0][i] = [{}]
                wrk_dict = wrk_dict[0][i]
        wrk_dict.append(top)

    def check(self, string):
        wrk_dict = self.root
        for i in string:
            if i in wrk_dict[0]:
                wrk_dict = wrk_dict[0][i]
            else:
                return False
        if len(wrk_dict) != 1:
            return True
        return False

    def check_part(self, string):
        wrk_dict = self.root
        for i in string:
            if i in wrk_dict[0]:
                wrk_dict = wrk_dict[0][i]
            else:
                return False
        return True

    def get_top(self, string):
        num = {}
        top = []
        word = string
        self.sudjest(word,num)
        sor = sorted(num.items(), key=operator.itemgetter(1))
        sor.reverse()
        return(sor[0:10])

    def sudjest(self, string,num):
        wrk_dict = self.root
        word = ''
        cur = []
        for i in string:
            wrk_dict = wrk_dict[0][i]
            word += i
        for key in wrk_dict[0].keys():
            word += key
            self.sudjest(word, num)
            word = string
        if not wrk_dict[0].keys() :
            num[word] = wrk_dict[1]
        return(num)







def init_prefix_tree(filename):
    #TODO в данном методе загружаем данные из файла. Предположим вормат файла "Строка, чтобы положить в дерево" \t "json значение для ноды" \t частота встречаемости
    tree = PrefixTree()
    with open('./freqrnc2011.csv', 'r') as f:
        for line in f.readlines()[1:]:
            l = line.split('\t')
            tree.add(l[0], float(l[2]))
    return(tree)  

tree = init_prefix_tree('')

@app.route("/get_sudgest/<string>", methods=['GET', 'POST'])
def return_sudgest(string):
    #TODO по запросу string вернуть json, c топ-10 саджестами, и значениями из нод
    if tree.check_part(string):
        return json.dumps(tree.get_top(string),ensure_ascii=False) 
    else:
        return 'nothing'
    

@app.route("/")
def hello():
    #TODO должна возвращатьс инструкция по работе с серверо
    return 'напишите русские символы, чтобы получить 10 наиболее частых слов начинающихся с этих символов '

if __name__ == "__main__":
    app.run()
