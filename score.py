#coding:utf_8
import sys
import gensim,os
import codecs

def read_line(f):
    '''
        读取一行，并清洗空格和换行 
    '''
    line = f.readline()
    line = line.strip('\n').strip('\r').strip(' ')
    while (line.find('  ') >= 0):
        line = line.replace('  ', ' ')
    return line


def prf_score(real_text_file,pred_text_file,prf_file):
    file_gold = codecs.open(real_text_file, 'r', 'utf8')
    # file_gold = codecs.open(r'../corpus/msr_test_gold.utf8', 'r', 'utf8')
    # file_tag = codecs.open(r'pred_standard.txt', 'r', 'utf8')
    file_tag = codecs.open(pred_text_file, 'r', 'utf8')

    line1 = read_line(file_gold)
    N_count = 0   #将正类分为正或者将正类分为负 TP+FN
    e_count = 0   #将负类分为正 FP
    c_count = 0   #正类分为正 TP
    e_line_count = 0
    c_line_count = 0
                                                                                                                                                                                                                           
    while line1:
        line2 = read_line(file_tag)

        list1 = line1.split(' ')
        list2 = line2.split(' ')

        count1 = len(list1)   # 标准分词数
        N_count += count1
        if line1 == line2:
            c_line_count += 1#分对的行数
            c_count += count1#分对的词数
        else:
            e_line_count += 1
            count2 = len(list2)

            arr1 = []
            arr2 = []

            pos = 0
            for w in list1:
                arr1.append(tuple([pos, pos + len(w)]))#list1中各个单词的起始位置
                pos += len(w)

            pos = 0
            for w in list2:
                arr2.append(tuple([pos, pos + len(w)]))#list2中各个单词的起始位置
                pos += len(w)

            for tp in arr2:
                if tp in arr1:
                    c_count += 1
                else:
                    e_count += 1

        line1 = read_line(file_gold)

    R = float(c_count) / N_count
    P = float(c_count) / (c_count + e_count)
    F = 2. * P * R / (P + R)
    ER = 1. * e_count / N_count

    #print '  标准词数：{} 个，正确词数：{} 个，错误词数：{} 个'.format(N_count, c_count, e_count).decode('utf8')
    # print '  标准行数：{}，正确行数：{} ，错误行数：{}'.format(c_line_count+e_line_count, c_line_count, e_line_count).decode('utf8')
    # print '  Recall: {}%'.format(R)
    # print '  Precision: {}%'.format(P)
    # print '  F MEASURE: {}%'.format(F)
    # print '  ERR RATE: {}%'.format(ER)
    print("result:")
    print('标准词数：%d个，正确词数：%d个，错误词数：%d个' %(N_count, c_count, e_count))
    print('标准行数：%d，正确行数：%d，错误行数：%d'%(c_line_count+e_line_count, c_line_count, e_line_count))
    print('Recall: %f'%(R))
    print('Precision: %f'%(P))
    print('F MEASURE: %f'%(F))
    print('ERR RATE: %f'%(ER))

    #print P,R,F

    # f=codecs.open(prf_file,'a','utf-8')
    # f.write('标准词数：%d个，正确词数：%d个，错误词数：%d个\n' %(N_count, c_count, e_count))
    # f.write('标准行数：%d，正确行数：%d，错误行数：%d\n'%(c_line_count+e_line_count, c_line_count, e_line_count))
    # f.write('Recall: %f\n'%(R))
    # f.write('Precision: %f\n'%(P))
    # f.write('F MEASURE: %f\n'%(F))
    # f.write('ERR RATE: %f\n'%(ER))
    # f.write('====================================\n')

    return R,P,F,ER

def main():
    # prf_score('real_text.txt','corpus/test_p0.19999999999999996_11110.utf8','prf_tmp.txt',1111)
    pred_file_dir = 'test_results/bc5'
    gold_file_dir = 'test_results/origin'
    num = 0.0
    RSum = 0.0
    PSum = 0.0
    FSum = 0.0
    ERSum = 0.0
    for fname in os.listdir(pred_file_dir):
        pred_file=pred_file_dir + os.sep + fname
        gold_file=gold_file_dir + os.sep + fname
        R,P,F,ER=prf_score(pred_file,gold_file,'test_results/prf_tmp_bc5/'+ fname)
        RSum += R
        PSum += P
        FSum += F
        ERSum += ER
        num += 1
    # out_file=codecs.open('test_results/prf_tmp_bc5/average.txt','a','utf-8')
    # out_file.write('Recall: %f\n'%(RSum/num))
    # out_file.write('Precision: %f\n'%(PSum/num))
    # out_file.write('F MEASURE: %f\n'%(FSum/num))
    # out_file.write('ERR RATE: %f\n'%(ERSum/num))
    # out_file.write('====================================\n')

    print('Average Recall: %f'%(RSum/num))
    print('Average Precision: %f'%(PSum/num))
    print('Average F MEASURE: %f'%(FSum/num))
    print('Average ERR RATE: %f'%(ERSum/num))

if __name__ == '__main__':
    main()
    