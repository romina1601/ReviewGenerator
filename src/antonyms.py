from sentimentAnalyzer import sentimentAnalyzer as sa 
import requests

class antonyms:

        fakeReviews = []                        #list containing all valid fake reviews

        def __init__(self):
                pass
        
        @staticmethod
        def getAdjAnt(initSentence):
                listaAdj = []                          #list with all adjectives in initial phrase 
                antonyms = []                          #list of synonyms extracted from ConceptNet
                responseList= []                       #list of ConceptNet API responses
                fakeReview = initSentence[:]           #nitially, the fake review is the same with the initial sentence

                #sa.analyzeSentence(sentence)
                posList = sa.identifyPOS(initSentence)

                #if word to be changed is simple adjective, put it in the adjectives list
                for (word, pos) in posList:
                        if pos == 'JJ':
                                listaAdj.append(word)
                                
                #get the json response from ConceptNet for every adjective in the initial phrase
                #we look only for terms in English and their synonyms in English as well
                for adj in listaAdj:
                        #print(adj)
                        response = requests.get('http://api.conceptnet.io/query?start=/c/en/'+adj+'&rel=/r/Antonym&end=/c/en').json()
                        responseList.append(response)

                ###########parse json from ConceptNet to get just the synonym word
                for resp in responseList:
                        try: 
                                temp = resp['edges'][0]['@id']
                                temp = temp.split("/en/")
                                temp = temp[2].split("/")
                                antonym = temp[0]
                                antonyms.append(antonym)
                        except IndexError:                      #no synonym was found by ConceptNet
                                antonyms.append("exceptie")      #when an exception is found, we do not want to replace the original word

                #replace every adjective with its antonym
                for i in range(0, len(antonyms)):
                        if antonyms[i] == "exceptie":
                                continue
                        else:
                                #sometimes, the ConceptNet response is an expression and it contains "_", so we want to replace it with a space
                                if antonyms[i].find("_") != -1:
                                        antonyms[i] = antonyms[i].replace("_", " ")
                                fakeReview = fakeReview.replace(listaAdj[i], antonyms[i])
                
                # print(initSentence)
                # print(fakeReview)

                return fakeReview
        

        @staticmethod
        def getVbAnt(initSentence):
                listaVb = []                                            #list with all verbs in initial phrase 
                listaVbFlag = []                                        #list with all verbs and associated flags, to see if they follow a modal verb
                negVerbs = []
                negationWords = ["not", "don't", "doesn't", "n't"]      #list with negation words to look for in order to delete them    
                negationFlag = 0                                        #flag to see if there are negative words in sentence do the correct replacement
                fakeReview = initSentence[:]


                posList = sa.identifyPOS(initSentence)

                #if word to be changed is verb in base form, put it in the verbs list
                for (word, pos) in posList:
                        #print(word, pos)

                        #if it is a negative review, remove the negation words such as not, don't, etc
                        if word in negationWords:
                                negationFlag = 1
                        
                        if negationFlag == 1 and word in negationWords:
                                fakeReview = fakeReview.replace(word, "")

                        if negationFlag == 0:
                                #need to see if there is any modal verb before the actual verb
                                #if so, set a flag to 1, so when we negate the verb, we add "not" instead of "don't"
                                if pos == 'MD':
                                        listaVbFlag.append((word, 1))
                                        listaVb.append(word)
                                #to negate is, we add not after it, just like we do with a modal verb; that's why the flag is the same
                                elif word == "is":
                                        listaVbFlag.append((word, 1))
                                        listaVb.append(word)
                                elif pos == 'VBP':
                                        listaVbFlag.append((word, 0))
                                        listaVb.append(word)
                

                #if there were no negative words, we should add them in the sentence
                if negationFlag == 0:
                        for (verb, flag) in listaVbFlag:
                                if flag == 1:
                                        newVerb = verb + " not"
                                elif flag == 0:
                                        newVerb = "don't " + verb
                                negVerbs.append(newVerb)

                elif negationFlag == 1:
                        for (word, pos) in posList:
                                if word == "wo":
                                        newVerb = "will"
                                        fakeReview = fakeReview.replace(word, newVerb)
                                elif word == "ca":
                                        newVerb = "can"
                                        fakeReview = fakeReview.replace(word, newVerb)
                                elif word == "sha":
                                        newVerb = "shall"
                                        fakeReview = fakeReview.replace(word, newVerb)
                                        

                for i in range(0, len(negVerbs)):
                        fakeReview = fakeReview.replace(listaVb[i], negVerbs[i])

                # print(initSentence)
                # print(fakeReview)

                return fakeReview
                        
        
        @staticmethod
        def validateReview(sentences, choice):
                for sentence in sentences:
                        if choice == "adj":
                                review = antonyms.getAdjAnt(sentence)
                                initScore = sa.analyzeSentence(sentence)['compound']
                                fakeScore = sa.analyzeSentence(review)['compound']
                                # print(initScore)
                                # print(fakeScore)
                                delta = initScore - fakeScore

                                if delta > -0.1 and delta < 0.1:
                                        print("The generated review is not valid")
                                else:
                                        #print("The review: '" + review + "' is a valid review")
                                        print("Review created")
                                        antonyms.fakeReviews.append(review)

                        elif choice == "vb":
                                review = antonyms.getVbAnt(sentence)
                                initScore = sa.analyzeSentence(sentence)['compound']
                                fakeScore = sa.analyzeSentence(review)['compound']
                                # print(initScore)
                                # print(fakeScore)
                                delta = initScore - fakeScore

                                if delta > -0.1 and delta < 0.1:
                                        print("The generated review is not valid")
                                else:
                                        #print("The review: '" + review + "' is a valid review")
                                        print("Review created")
                                        antonyms.fakeReviews.append(review)

                        else:
                                print("Your choice is invalid.")
                                return []

                return antonyms.fakeReviews