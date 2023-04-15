import jieba
import wt

def cx(name):
    jieba.add_word(r"舰艇损管")
    jieba.add_word(r"潜水方式")
    jieba.add_word(r"类")
    name_c = jieba.lcut(name)
    k = []
    p = 0
    for jz in wt.wt:
        jz_jieba = jieba.lcut(jz)
        q = 0
        for name_z in name_c:
            if name_z in jz_jieba:
                q = q+1
        p = p+1
        k.append((p,q))
    max = 0
    wz = 0
    for i in k:
        if i[1] > max:
            max = i[1]
            wz = i[0]
    if max == 0:
        ppp = '暂无此内容'
        return ppp

    return wt.wt[wz-1]



