import sys

#sys.argv[1] - path_of_input_corpus
#sys.argv[2] - path_of_output_result
#sys.argv[3] - path_of_input_queries

# print(sys.argv[0])
# print(sys.argv[1])
# print(sys.argv[2])
# print(sys.argv[3])

file1 = open(sys.argv[1], "r")
file2 = open(sys.argv[2], "w")
file3 = open(sys.argv[3], "r")


def AND(posting1, posting2):
    p1 = 0
    p2 = 0
    num_comp = 0
    result = list()
    while p1 < len(posting1) and p2 < len(posting2):
        if posting1[p1] == posting2[p2]:
            num_comp = num_comp + 1
            result.append(posting1[p1])
            p1 = p1 + 1
            p2 = p2 + 1
        elif posting1[p1] > posting2[p2]:
            num_comp = num_comp + 1
            p2 = p2 + 1
        else:
            num_comp = num_comp + 1
            p1 = p1 + 1
    return (result,num_comp)

def OR(posting1, posting2):
    p1 = 0
    p2 = 0
    num_comp = 0
    result = list()
    # print('line 43, p1 : [{}] p2 : [{}]'.format(p1,p2))
    while p1 < len(posting1) and p2 < len(posting2):
        if posting1[p1] == posting2[p2]:
            num_comp = num_comp + 1
            result.append(posting1[p1])
            # print(result)
            p1 = p1 + 1
            p2 = p2 + 1
            # print('line 50, p1 : [{}] p2 : [{}]'.format(p1,p2))
        elif posting1[p1] > posting2[p2]:
            num_comp = num_comp + 1
            result.append(posting2[p2])
            # print(result)
            p2 = p2 + 1
            # print('line 55, p1 : [{}] p2 : [{}]'.format(p1,p2))
        else:
            num_comp = num_comp + 1
            result.append(posting1[p1])
            # print(result)
            p1 = p1 + 1
            # print('line 60, p1 : [{}] p2 : [{}]'.format(p1,p2))
    # print('line 61, p1 : [{}] p2 : [{}]'.format(p1,p2))
    while p1 < len(posting1):
        result.append(posting1[p1])
        # print(result)
        p1 = p1 + 1
        # print('line 66, p1 : [{}] p2 : [{}]'.format(p1,p2))
    # print('line 67, p1 : [{}] p2 : [{}]'.format(p1,p2))
    while p2 < len(posting2):
        result.append(posting2[p2])
        # print(result)
        p2 = p2 + 1
        # print('line 72, p1 : [{}] p2 : [{}]'.format(p1,p2))
    return (result,num_comp)



doc_dict = {}
total_terms_in_doc = {}
freq = 1
total_docs = 0
tf_idf = 0

while True:
    line_text = file1.readline()
    if not line_text :  #If line is empty then end of file reached
        break;
    else:
        total_docs = total_docs + 1 
        #removing \n from end of line
        line_text = line_text.strip('\n')
        
        #splitting doc id and sentence
        doc_id_line = line_text.split("\t")
        # print(doc_id_line)
        
        doc_id = doc_id_line[0]
        # print(doc_id)
        
        doc_text = doc_id_line[1]
        # print(doc_text)
        
        doc_text_words = doc_text.split()
        # print(doc_text_words)
        
        term_count = 1

        #creating the postings list
        for k in doc_text_words: 
            # print('doc_id : '+doc_id+'=====word : '+k)
            total_terms_in_doc[doc_id] = term_count
            term_count = term_count + 1
            if k not in doc_dict:
                doc_dict[k] = {}    
                # print(k,doc_dict[k])
                freq = 1
                doc_dict[k]['doc_freq'] = freq
                # print(k,doc_dict[k]['doc_freq'])
                doc_dict[k]['doc_id'] = list()
                # print(k,doc_dict[k]['doc_id'])
                doc_dict[k]['doc_id'].append(doc_id)
                # print(k,doc_dict[k]['doc_id'])
                doc_dict[k]['tf_in_doc'] = list()
                # print(k,doc_dict[k]['tf_in_doc'])
                doc_dict[k]['tf_in_doc'].append(freq)
                # print(k,doc_dict[k]['tf_in_doc'])
            else:
                # print('current doc_id is: '+doc_id)
                if(doc_id == doc_dict[k]['doc_id'][-1]):
                    # print('multiple occ of word in same doc')
                    # print('current tf : {}'.format(doc_dict[k]['tf_in_doc'][-1]))
                    new_freq = doc_dict[k]['tf_in_doc'][-1]
                    new_freq = new_freq + 1
                    doc_dict[k]['tf_in_doc'][-1] = new_freq
                    # print('new tf : {}'.format(doc_dict[k]['tf_in_doc'][-1]))
                if(doc_id != doc_dict[k]['doc_id'][-1]):
                    # print('==word found in diff doc==')
                    # print('current doc freq for ['+k+'] is {}'.format(doc_dict[k]['doc_freq']))
                    doc_dict[k]['doc_freq'] = doc_dict[k]['doc_freq'] + 1
                    # print('new doc freq for ['+k+'] is {}'.format(doc_dict[k]['doc_freq']))
                    doc_dict[k]['doc_id'].append(doc_id)
                    doc_dict[k]['tf_in_doc'].append(freq)
                    # print('new doc id list is ', end = '')
                    # print(doc_dict[k]['doc_id'])
                    # print('tf of ['+k+'] is ', end = '')
                    # print(doc_dict[k]['tf_in_doc'])
        # print('no of terms in doc with doc id ['+doc_id+'] is {}'.format(total_terms_in_doc[doc_id]))
# print('total docs : {}'.format(total_docs))
# print('=====Postings list created=====')
# for x,y in doc_dict.items(): 
    # print(x, y)

postings_list_t1 = list()
postings_list_t2 = list()
result_list = list()
j = 0
comparisons_count = 0
comp_count_1 = 0
tf_dict = {}
doc_tf_idf = {}
doc_tf = []
doc_tf = [list()]
list1 = []
result_tf_idf = []
while True:
    line_text_1 = file3.readline()
    if not line_text_1 :  
        break;
    else:
        queryline_text = line_text_1.strip('\n')
        query_terms = queryline_text.split()
        # print('query_terms : ', end = '')
        # print(query_terms)
        # print(type(query_terms))
        for i in query_terms:
            file2.write("GetPostings\n")
            file2.write(i+"\n")
            
            space_cnt = 0
            file2.write("Postings list: ")
            for x in doc_dict[i]['doc_id']:
                file2.write(x)
                space_cnt = space_cnt + 1
                if(space_cnt < len(doc_dict[i]['doc_id'])):
                    file2.write(" ")
            
            file2.write("\n")
        file2.write("DaatAnd\n")
        
        space_cnt = 0
        for i in query_terms:
            file2.write(i)
            space_cnt = space_cnt + 1
            if(space_cnt < len(query_terms)):
                file2.write(" ")
        
        # print("count of query terms : {}".format(len(query_terms)))
        file2.write("\n")
        file2.write("Results: ")
        # print('len of query_terms list : {}'.format(len(query_terms)))
        result_list = list()
        for i in range(len(query_terms)-1):
            if (len(query_terms) == 2):
                postings_list_t1 = doc_dict[query_terms[0]]['doc_id']
                postings_list_t2 = doc_dict[query_terms[1]]['doc_id']
                # print('p1 : ', end = '')
                # print(postings_list_t1)
                # print('p2 : ', end = '')
                # print(postings_list_t2)
                result_list, comparisons_count = AND(postings_list_t1, postings_list_t2)
                # print('in loop line 163, result of AND : ', end = '')
                # print(result_list)
            elif(len(query_terms) > 2):
                if(len(result_list)==0):
                    postings_list_t1 = doc_dict[query_terms[0]]['doc_id']
                    postings_list_t2 = doc_dict[query_terms[1]]['doc_id']
                    # print('p1 : ', end = '')
                    # print(postings_list_t1)
                    # print('p2 : ', end = '')
                    # print(postings_list_t2)
                    result_list, comp_count_1 = AND(postings_list_t1, postings_list_t2)
                    comparisons_count = comp_count_1 
                    # print('line 175, result of AND : ', end = '')
                    # print(result_list)
                elif(len(result_list)>0):
                    for j in range(2, len(query_terms)):
                        # print('result_list > 0, j = {}'.format(j))
                        postings_list_t1 = result_list
                        postings_list_t2 = doc_dict[query_terms[j]]['doc_id']
                        # print('p1 : ', end = '')
                        # print(postings_list_t1)
                        # print('p2 : ', end = '')
                        # print(postings_list_t2)
                        result_list, comp_count_1 = AND(postings_list_t1, postings_list_t2)
                        comparisons_count = comparisons_count + comp_count_1
                        # print('line 187, at iteration {}, result of AND : '.format(j), end = '')
                        # print(result_list)
        if(len(result_list) == 0):
            file2.write("empty")
            # print('line 190')
        else:
            # print('line 193, result of AND : ', end = '')
            # print(result_list)
            space_cnt = 0
            for i in result_list:
                file2.write(i)
                space_cnt = space_cnt + 1
                if(space_cnt < len(result_list)):
                    file2.write(" ")
        # print('comparisons_count : {}'.format(comparisons_count))
        
        file2.write("\nNumber of documents in results: ")
        file2.write(str(len(result_list)))
        
        file2.write("\nNumber of comparisons: ")
        file2.write(str(comparisons_count))
        
        file2.write("\nTF-IDF")
        file2.write("\nResults: ")
        
        #tf_idf calculation begins
        if(len(result_list) == 0):
            file2.write("empty")
        elif(len(result_list) == 1):
            for x in result_list:
                file2.write(x)
        elif(len(result_list) > 1):
            result_tf_idf = []
            doc_tf_idf = {}
            for x in result_list:
                # print('result list term : ',end='')
                # print(x)
                for i in query_terms:
                    # print('\t query term : ',end='')
                    # print(i)
                    position_cntr = 0
                    for j in doc_dict[i]['doc_id']:
                        # print('\t   doc ids list : ',end='')
                        # print(j,end='')
                        # print('  position_cntr :{}'.format(position_cntr))
                        if( x == j):
                            # print('\t       loc of doc id found')
                            # if x not in doc_tf_idf:
                            loc_ctr = position_cntr
                            tf = doc_dict[i]['tf_in_doc'][loc_ctr]/total_terms_in_doc[x]
                            # print('\t        tf : ', tf)
                            # print('\t        total docs : {}'.format(total_docs))
                            # print('\t        num of docs with term in it : {}'.format(len(doc_dict[i]['doc_id'])))
                            idf = total_docs/len(doc_dict[i]['doc_id'])
                            # print('\t       idf : ', idf)
                            tf_idf = tf * idf 
                            # print('\t        tf_idf : {}'.format(tf_idf))
                            break;
                        position_cntr = position_cntr + 1
                    if x not in doc_tf_idf:                    
                        # print('\t   adding to doc_tf_idf for-----',end='')
                        # print(x)
                        doc_tf_idf[x] = tf_idf
                    else:
                        # print('\t   updating values in doc_tf_idf  for ++++++',end='')
                        # print(x)
                        new_tf_idf = doc_tf_idf[x] + tf_idf
                        doc_tf_idf[x] = new_tf_idf
                        # print(doc_tf_idf[x])
                # print('tf_idf score final for terms in doc[',end='')
                # print(x,end='')
                # print('] is : ',end='')
                # print(doc_tf_idf[x])
            # print('doc_tf_idf : ')
            # for x,y in doc_tf_idf.items(): 
                # print(x, y)
            
            list1 = list()
            list1=list(doc_tf_idf.values())
            # print('getting tf_idf values to list : ',end='')
            # print(list1)
            list1.sort(reverse = True)
            # print('list in desc order : ',end='')
            # print(list1)
            prev = float(0)
            # print('prev var value : {}'.format(prev))
            for i in list1:
                # print('parsing in list1 for : ',end='')
                # print(i)
                curr = float(i)
                for x in doc_tf_idf:
                    # print('\t parsing in doc_tf_idf for : ',end='')
                    # print(x)
                    if (doc_tf_idf[x] == i):
                        # print('\t   found match : ',end='')
                        # print(i,end='')
                        # print(' = ',end='')
                        # print(doc_tf_idf[x])
                        # print('len(result_tf_idf) : {}'.format(len(result_tf_idf)))
                        if(len(result_tf_idf)==0):
                            result_tf_idf.append(x)
                        else:
                            if x not in result_tf_idf:
                                result_tf_idf.append(x)
                        # print('\t   result_tf_idf at this stage : ',end='')
                        # print(result_tf_idf)
                prev = curr
            # print('doc ids in desc order of tf_idf scores : ',end='')
            # print(result_tf_idf)
            space_cnt = 0
            for x in result_tf_idf:
                file2.write(x)
                space_cnt = space_cnt + 1
                if(space_cnt < len(result_tf_idf)):
                    file2.write(" ")
        #tf_idf calculation ends
        
        file2.write("\nDaatOr\n")
        
        space_cnt = 0
        for i in query_terms:
            file2.write(i)
            space_cnt = space_cnt + 1
            if(space_cnt < len(query_terms)):
                file2.write(" ")
        
        file2.write("\nResults: ")
        
        result_list = list()
        for i in range(len(query_terms)-1):
            if (len(query_terms) == 2):
                postings_list_t1 = doc_dict[query_terms[0]]['doc_id']
                postings_list_t2 = doc_dict[query_terms[1]]['doc_id']
                # print('p1 : ', end = '')
                # print(postings_list_t1)
                # print('p2 : ', end = '')
                # print(postings_list_t2)
                result_list, comparisons_count = OR(postings_list_t1, postings_list_t2)
                # print('in loop line 163, result of OR : ', end = '')
                # print(result_list)
            elif(len(query_terms) > 2):
                if(len(result_list)==0):
                    # print('====len(query_terms) > 2 & len(result_list)==0====')
                    postings_list_t1 = doc_dict[query_terms[0]]['doc_id']
                    postings_list_t2 = doc_dict[query_terms[1]]['doc_id']
                    # print('p1 : ', end = '')
                    # print(postings_list_t1)
                    # print('p2 : ', end = '')
                    # print(postings_list_t2)
                    result_list, comp_count_1 = OR(postings_list_t1, postings_list_t2)
                    comparisons_count = comp_count_1 
                    # print('line 175, result of OR : ', end = '')
                    # print(result_list)
                elif(len(result_list)>0):
                    for j in range(2, len(query_terms)):
                        # print('result_list > 0, j = {}'.format(j))
                        postings_list_t1 = result_list
                        postings_list_t2 = doc_dict[query_terms[j]]['doc_id']
                        # print('p1 : ', end = '')
                        # print(postings_list_t1)
                        # print('p2 : ', end = '')
                        # print(postings_list_t2)
                        result_list, comp_count_1 = OR(postings_list_t1, postings_list_t2)
                        comparisons_count = comparisons_count + comp_count_1
                        # print('line 187, at iteration {}, result of OR : '.format(j), end = '')
                        # print(result_list)
        if(len(result_list) == 0):
            file2.write("empty")
            # print('line 190')
        else:
            # print('line 193, result of OR : ', end = '')
            # print(result_list)
            space_cnt = 0
            for i in result_list:
                file2.write(i)
                space_cnt = space_cnt + 1
                if(space_cnt < len(result_list)):
                    file2.write(" ")
        
        file2.write("\nNumber of documents in results: ")
        file2.write(str(len(result_list)))
        
        file2.write("\nNumber of comparisons: ")
        file2.write(str(comparisons_count))
        
        file2.write("\nTF-IDF")
        file2.write("\nResults: ")
        
        #tf_idf calculation begins
        if(len(result_list) == 0):
            file2.write("empty")
        elif(len(result_list) == 1):
            for x in result_list:
                file2.write(x)
        elif(len(result_list) > 1):
            result_tf_idf = []
            doc_tf_idf = {}
            for x in result_list:
                # print('result list term : ',end='')
                # print(x)
                for i in query_terms:
                    # print('\t query term : ',end='')
                    # print(i)
                    position_cntr = 0
                    for j in doc_dict[i]['doc_id']:
                        # print('\t   doc ids list : ',end='')
                        # print(j,end='')
                        # print('  position_cntr :{}'.format(position_cntr))
                        if( x == j):
                            # print('\t       loc of doc id found')
                            # if x not in doc_tf_idf:
                            loc_ctr = position_cntr
                            tf = doc_dict[i]['tf_in_doc'][loc_ctr]/total_terms_in_doc[x]
                            # print('\t        tf : ', tf)
                            # print('\t        total docs : {}'.format(total_docs))
                            # print('\t        num of docs with term in it : {}'.format(len(doc_dict[i]['doc_id'])))
                            idf = total_docs/len(doc_dict[i]['doc_id'])
                            # print('\t       idf : ', idf)
                            tf_idf = tf * idf 
                            # print('\t        tf_idf : {}'.format(tf_idf))
                            break;
                        position_cntr = position_cntr + 1
                    if x not in doc_tf_idf:                    
                        # print('\t   adding to doc_tf_idf for-----',end='')
                        # print(x)
                        doc_tf_idf[x] = tf_idf
                    else:
                        # print('\t   updating values in doc_tf_idf  for ++++++',end='')
                        # print(x)
                        new_tf_idf = doc_tf_idf[x] + tf_idf
                        doc_tf_idf[x] = new_tf_idf
                        # print(doc_tf_idf[x])
                # print('tf_idf score final for terms in doc[',end='')
                # print(x,end='')
                # print('] is : ',end='')
                # print(doc_tf_idf[x])
            # print('doc_tf_idf : ')
            # for x,y in doc_tf_idf.items(): 
                # print(x, y)
            
            list1 = list()
            list1=list(doc_tf_idf.values())
            # print('getting tf_idf values to list : ',end='')
            # print(list1)
            list1.sort(reverse = True)
            # print('list in desc order : ',end='')
            # print(list1)
            prev = float(0)
            # print('prev var value : {}'.format(prev))
            for i in list1:
                # print('parsing in list1 for : ',end='')
                # print(i)
                curr = float(i)
                for x in doc_tf_idf:
                    # print('\t parsing in doc_tf_idf for : ',end='')
                    # print(x)
                    if (doc_tf_idf[x] == i):
                        # print('\t   found match : ',end='')
                        # print(i,end='')
                        # print(' = ',end='')
                        # print(doc_tf_idf[x])
                        # print('len(result_tf_idf) : {}'.format(len(result_tf_idf)))
                        if(len(result_tf_idf)==0):
                            result_tf_idf.append(x)
                        else:
                            if x not in result_tf_idf:
                                result_tf_idf.append(x)
                        # print('\t   result_tf_idf at this stage : ',end='')
                        # print(result_tf_idf)
                prev = curr
            # print('doc ids in desc order of tf_idf scores : ',end='')
            # print(result_tf_idf)
            space_cnt = 0
            for x in result_tf_idf:
                file2.write(x)
                space_cnt = space_cnt + 1
                if(space_cnt < len(result_tf_idf)):
                    file2.write(" ")
        #tf_idf calculation ends

        file2.write("\n")
    file2.write("\n")




file1.close() 
file2.close() 
file3.close()