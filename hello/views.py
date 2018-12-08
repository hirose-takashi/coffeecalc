from django.shortcuts import render
from django.http.response import HttpResponse
from django.core.files.storage import default_storage
from django.core.files import File
from datetime import datetime





def hello_world(request):
    return HttpResponse('Hello World!')

# def hello_world(request):
#     return render(request, 'hello/hello_world.html', {})


def hello_template(request):
    d = {
        'hour': datetime.now().hour,
        'message': 'Sample message',
    }
    return render(request, 'hello/hello_template.html', d)

def hello_if(request):
    d = {
        'is_visible': False,
        'empty_str': '',
    }
    return render(request, 'hello/hello_if.html', d)

def hello_for(request):
    d = {
        'objects': range(10),
    }
    return render(request, 'hello/hello_for.html', d)


def hello_get_query(request):
    d = {
        'your_name': range(10),
    }
    return render(request, 'hello/hello_get_query.html', d)

#データを受け取り、リストに格納
def hello_form_post(request):
    import numpy as np
    import pandas as pd

    p = request.POST.getlist("flavor")

    ### Database
    df_in = pd.read_csv("SB.csv", names=("item", "roast", "description", "hp"), index_col=0)


    # +/-を正しい位置に入れる
    l = [ len(p[i]) for i in range(len(p)) ]
    sign_ind = np.where(np.array(l)==1)[0]

    p_corr = [p[0],p[1],p[2]]
    print(p_corr)
    try:
        p_corr[0] = df_in.loc[p[0]]["description"]
        flug = 1
    except:
        flug = 0


    def word2vec(word):
        from janome.tokenizer import Tokenizer
        from gensim.models import word2vec
        from gensim.models.keyedvectors import KeyedVectors

        mt = Tokenizer()
        #model = word2vec.Word2Vec.load("wiki.model")
        model = word2vec.KeyedVectors.load_word2vec_format("wiki.model")


        # テキストのベクトルを計算
        def get_vector(text):
            sum_vec = np.zeros(200)
            word_count = 0
            #node = mt.parseToNode(text)
            tokens = mt.tokenize(text)

            for node in tokens:
                base, fields = node.base_form, node.part_of_speech
                fields = node.part_of_speech.split(',')

                # 名詞、動詞、形容詞に限定
                if fields[0] == '名詞' or fields[0] == '動詞' or fields[0] == '形容詞':
                    sum_vec += model.wv[node.surface]
                    word_count += 1

            return sum_vec / word_count



        # cos類似度を計算
        def cos_sim(v1, v2):
            return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


        df_in = pd.read_csv("SB.csv", names=("item", "roast", "description", "hp"))
        lines = list(df_in["description"])
        items = list(df_in["item"])
        lines2 = list(df_in["hp"])

        Nl = len(lines)

        ### User request
        sign_arr = []
        for i in range(1,len(word),2):
            sign_arr.append(word[i])


        v_arr = get_vector(word[0])
        for cc, i in enumerate(range(2,len(word),2)):

            if sign_arr[cc]=="+":
                v_arr += get_vector(word[i])
            elif sign_arr[cc]=="-":
                print("-")
                v_arr -= get_vector(word[i])



        Cos = []; Descri = []; Vec = []; Item = []
        for i in range(Nl):

            try:
                reply = get_vector(lines[i])
                Cos.append( cos_sim(v_arr,reply) )
                Descri.append(lines2[i])
                Item.append(items[i])
            except:
                pass

        Cos = np.array(Cos)

        indd = np.argsort(Cos)[::-1]


        return [ [Item[i],Descri[i]] for i in indd[:3]]

    rec_item = word2vec(p_corr)


    if flug==1:
        p_corr[0] = p[0]
        d = {
            'components': p_corr,
            'objects': rec_item,
            }
    else:
        d = {
            'components': p_corr,
            'objects': rec_item,
            }

    return render(request, 'hello/hello_form_post.html', d)
