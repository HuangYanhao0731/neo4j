import jieba
import wt

def cx(name):
    jieba.add_word(r"舰艇损管")
    jieba.add_word(r"潜水方式")
    jieba.add_word(r"类")
    if name[-1] == '？':
        name = name[::-2]
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
    if max <= 0:
        ppp = '很抱歉目前我暂时还无法回答你的问题！'
        return ppp

    return wt.wt[wz-1]

def fju(name):
    if name[-1] == '？':
        name = name[:-2]
    print(name)
    L = []
    m = ''
    for i in name:
        if i == '？':
            m = m+i
            L.append(m)
            m = ''
        else:
            m = m+i
    if m !='':
        L.append(m)
    print(L)
    return L