from sentimentAnalyzer import sentimentAnalyzer as sa 
import requests

class synonyms:

        fakeReviews = []                        #list containing all valid fake reviews

        def __init__(self):
                pass
        
        @staticmethod
        def getAdjSyn(initSentence):
                listaAdj = []                          #list with all adjectives in initial phrase 
                synonyms = []                          #list of synonyms extracted from ConceptNet
                responseList= []                       #list of ConceptNet API responses
                fakeReview = initSentence[:]           #initially, the fake review is the same with the initial sentence

                posList = sa.identifyPOS(initSentence)

                #if word to be changed is simple adjective, put it in the adjectives list
                for (word, pos) in posList:
                        if pos == 'JJ':
                                listaAdj.append(word)
                                
                #get the json response from ConceptNet for every adjective in the initial phrase
                #we look only for terms in English and their synonyms in English as well
                for adj in listaAdj:
                        #print(adj)
                        response = requests.get('http://api.conceptnet.io/query?start=/c/en/'+adj+'&rel=/r/Synonym&end=/c/en&limit=1').json()
                        responseList.append(response)

                ###########parse json from ConceptNet to get just the synonym word
                for resp in responseList:
                        try: 
                                temp = resp['edges'][0]['@id']
                                temp = temp.split("/en/")
                                temp = temp[2].split("/")
                                synonym = temp[0]
                                synonyms.append(synonym)
                        except IndexError:                       #no synonym was found by ConceptNet
                                synonyms.append("exceptie")      #when an exception is found, we do not want to replace the original word

                #replace every adjective with its synonym
                for i in range(0, len(synonyms)):
                        if synonyms[i] == "exceptie":
                                continue
                        else:
                                #sometimes, the ConceptNet response is an expression and it contains "_", so we want to replace it with a space
                                if synonyms[i].find("_") != -1:
                                        synonyms[i] = synonyms[i].replace("_", " ")
                                fakeReview = fakeReview.replace(listaAdj[i], synonyms[i])
                
                #print(initSentence)
                #print(fakeReview)

                return fakeReview

        @staticmethod
        def getNounSyn(initSentence):
                listaNoun = []                          #list with all adjectives in initial phrase 
                synonyms = []                          #list of synonyms extracted from ConceptNet
                responseList= []                       #list of ConceptNet API responses
                fakeReview = initSentence[:]           #initially, the fake review is the same with the initial sentence

                #sa.analyzeSentence(sentence)
                posList = sa.identifyPOS(initSentence)

                #if word to be changed is simple adjective, put it in the adjectives list
                for (word, pos) in posList:
                        if pos == 'NN':
                                listaNoun.append(word)
                
                #get the json response from ConceptNet for every adjective in the initial phrase
                #we look only for terms in English and their synonyms in English as well
                for noun in listaNoun:
                        #print(noun)
                        response = requests.get('http://api.conceptnet.io/query?start=/c/en/'+noun+'&rel=/r/Synonym&end=/c/en&limit=1').json()
                        responseList.append(response)

                ###########parse json from ConceptNet to get just the synonym word
                for resp in responseList:
                        try: 
                                temp = resp['edges'][0]['@id']
                                temp = temp.split("/en/")
                                temp = temp[2].split("/")
                                synonym = temp[0]
                                synonyms.append(synonym)
                        except IndexError:                      #no synonym was found by ConceptNet
                                synonyms.append("exceptie")      #when an exception is found, we do not want to replace the original word


                #replace every adjective with its synonym
                for i in range(0, len(synonyms)):
                        if synonyms[i] == "exceptie":
                                continue
                        else:
                                #sometimes, the ConceptNet response is an expression and it contains "_", so we want to replace it with a space
                                if synonyms[i].find("_") != -1:
                                        synonyms[i] = synonyms[i].replace("_", " ")
                                fakeReview = fakeReview.replace(listaNoun[i], synonyms[i])
                
                #print(initSentence)
                #print(fakeReview)

                return fakeReview
        
        @staticmethod
        def getAdvSyn(initSentence):
                listaAdv = []                          #list with all adjectives in initial phrase 
                synonyms = []                          #list of synonyms extracted from ConceptNet
                responseList= []                       #list of ConceptNet API responses
                fakeReview = initSentence[:]           #initially, the fake review is the same with the initial sentence

                #sa.analyzeSentence(sentence)
                posList = sa.identifyPOS(initSentence)

                #if word to be changed is simple adjective, put it in the adjectives list
                for (word, pos) in posList:
                        if pos == 'RB':
                                listaAdv.append(word)
                
                #get the json response from ConceptNet for every adjective in the initial phrase
                #we look only for terms in English and their synonyms in English as well
                for adv in listaAdv:
                        #print(adv)
                        response = requests.get('http://api.conceptnet.io/query?start=/c/en/'+adv+'&rel=/r/Synonym&end=/c/en&limit=1').json()
                        responseList.append(response)

                ###########parse json from ConceptNet to get just the synonym word
                for resp in responseList:
                        try: 
                                temp = resp['edges'][0]['@id']
                                temp = temp.split("/en/")
                                temp = temp[2].split("/")
                                synonym = temp[0]
                                synonyms.append(synonym)
                        except IndexError:                      #no synonym was found by ConceptNet
                                synonyms.append("exceptie")      #when an exception is found, we do not want to replace the original word


                #replace every adjective with its synonym
                for i in range(0, len(synonyms)):
                        if synonyms[i] == "exceptie":
                                continue
                        else:
                                #sometimes, the ConceptNet response is an expression and it contains "_", so we want to replace it with a space
                                if synonyms[i].find("_") != -1:
                                        synonyms[i] = synonyms[i].replace("_", " ")
                                fakeReview = fakeReview.replace(listaAdv[i], synonyms[i])
                
                #print(initSentence)
                #print(fakeReview)

                return fakeReview

        
        @staticmethod
        def validateReview(sentences, choice):
                for sentence in sentences:
                        if choice == "adv":
                                review = synonyms.getAdvSyn(sentence)
                                initScore = sa.analyzeSentence(sentence)['compound']
                                fakeScore = sa.analyzeSentence(review)['compound']
                                #print(initScore)
                                #print(fakeScore)
                                delta = initScore - fakeScore

                                if delta < -0.1 or delta > 0.1:
                                        print("The generated review is not valid")
                                else:
                                        #print("The review: '" + review + "' is a valid review")
                                        print("Review created")
                                        synonyms.fakeReviews.append(review)

                        elif choice == "noun":
                                review = synonyms.getNounSyn(sentence)
                                initScore = sa.analyzeSentence(sentence)['compound']
                                fakeScore = sa.analyzeSentence(review)['compound']
                                #print(initScore)
                                #print(fakeScore)
                                delta = initScore - fakeScore

                                if delta < -0.1 or delta > 0.1:
                                        print("The generated review is not valid")
                                else:
                                        #print("The review: '" + review + "' is a valid review")
                                        print("Review created")
                                        synonyms.fakeReviews.append(review)
                        
                        elif choice == "adj":
                                review = synonyms.getAdjSyn(sentence)
                                initScore = sa.analyzeSentence(sentence)['compound']
                                fakeScore = sa.analyzeSentence(review)['compound']
                                #print(initScore)
                                #print(fakeScore)
                                delta = initScore - fakeScore

                                if delta < -0.1 or delta > 0.1:
                                        print("The generated review is not valid")
                                else:
                                        #print("The review: '" + review + "' is a valid review")
                                        print("Review created")
                                        synonyms.fakeReviews.append(review)
                        
                        elif choice == "all":
                                review = synonyms.getAdjSyn(sentence)
                                review = synonyms.getNounSyn(review)
                                review = synonyms.getAdvSyn(review)
                                initScore = sa.analyzeSentence(sentence)['compound']
                                fakeScore = sa.analyzeSentence(review)['compound']
                                #print(initScore)
                                #print(fakeScore)
                                delta = initScore - fakeScore

                                if delta < -0.1 or delta > 0.1:
                                        print("The generated review is not valid")
                                else:
                                        #print("The review: '" + review + "' is a valid review")
                                        print("Review created")
                                        synonyms.fakeReviews.append(review)
                        
                        else:
                                print("Your choice is invalid.")
                                return []

                return synonyms.fakeReviews