from sentimentAnalyzer import sentimentAnalyzer as sa 
import requests


class related:
        fakeReviews = []                        #list containing all valid fake reviews

        def __init__(self):
                pass
        
        @staticmethod
        def getAdjRelated(initSentence):
                listaAdj = []                          #list with all adjectives in initial phrase 
                relatedWords = []                      #list of related words extracted from ConceptNet
                responseList= []                       #list of ConceptNet API responses
                fakeReview = initSentence[:]           #initially, the fake review is the same with the original review

                posList = sa.identifyPOS(initSentence)

                #if word to be changed is simple adjective, put it in the adjectives list
                for (word, pos) in posList:
                        if pos == 'JJ':
                                listaAdj.append(word)
                                
                #get the json response from ConceptNet for every adjective in the initial phrase
                #we look only for terms in English and their synonyms in English as well
                for adj in listaAdj:
                        #print(adj)
                        response = requests.get('http://api.conceptnet.io/query?start=/c/en/'+adj+'&rel=/r/RelatedTo&end=/c/en&limit=1').json()
                        responseList.append(response)

                ###########parse json from ConceptNet to get just the synonym word
                for resp in responseList:
                        try: 
                                temp = resp['edges'][0]['@id']
                                temp = temp.split("/en/")
                                temp = temp[2].split("/")
                                relatedW = temp[0]
                                relatedWords.append(relatedW)
                        except IndexError:                           #no related word was found by ConceptNet
                                relatedWords.append("exceptie")      #when an exception is found, we do not want to replace the original word


                #replace every adjective with its synonym
                for i in range(0, len(relatedWords)):
                        if relatedWords[i] == "exceptie":
                                continue
                        else:
                                #sometimes, the ConceptNet response is an expression and it contains "_", so we want to replace it with a space
                                if relatedWords[i].find("_") != -1:
                                        relatedWords[i] = relatedWords[i].replace("_", " ")
                                fakeReview = fakeReview.replace(listaAdj[i], relatedWords[i])
                
                # print(initSentence)
                # print(fakeReview)

                return fakeReview

        @staticmethod
        def getNounRelated(initSentence):

                listaNoun = []                          #list with all adjectives in initial phrase 
                relatedWords = []                       #list of related words extracted from ConceptNet
                responseList= []                        #list of ConceptNet API responses
                fakeReview = initSentence[:]            #initially, the fake review is the same with the original review

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
                        response = requests.get('http://api.conceptnet.io/query?start=/c/en/'+noun+'&rel=/r/RelatedTo&end=/c/en&limit=1').json()
                        responseList.append(response)

                ###########parse json from ConceptNet to get just the synonym word
                for resp in responseList:
                        try: 
                                temp = resp['edges'][0]['@id']
                                temp = temp.split("/en/")
                                temp = temp[2].split("/")
                                relatedW = temp[0]
                                relatedWords.append(relatedW)
                        except IndexError:                           #no related word was found by ConceptNet
                                relatedWords.append("exceptie")      #when an exception is found, we do not want to replace the original word

                #replace every adjective with its synonym
                for i in range(0, len(relatedWords)):
                        if relatedWords[i] == "exceptie":
                                continue
                        else:
                                #sometimes, the ConceptNet response is an expression and it contains "_", so we want to replace it with a space
                                if relatedWords[i].find("_") != -1:
                                        relatedWords[i] = relatedWords[i].replace("_", " ")
                                fakeReview = fakeReview.replace(listaNoun[i], relatedWords[i])
                
                # print(initSentence)
                # print(fakeReview)

                return fakeReview
        
        @staticmethod
        def validateReview(sentences, choice):
                for sentence in sentences:
                        if choice == "adj":
                                review = related.getAdjRelated(sentence)
                                initScore = sa.analyzeSentence(sentence)['compound']
                                fakeScore = sa.analyzeSentence(review)['compound']
                                # print(initScore)
                                # print(fakeScore)
                                delta = initScore - fakeScore

                                if delta < -0.1 or delta > 0.1:
                                        print("The generated review is not valid")
                                else:
                                        #print("The review: '" + review + "' is a valid review")
                                        print("Review created")
                                        related.fakeReviews.append(review)
                        
                        elif choice == "noun":
                                review = related.getNounRelated(sentence)
                                initScore = sa.analyzeSentence(sentence)['compound']
                                fakeScore = sa.analyzeSentence(review)['compound']
                                # print(initScore)
                                # print(fakeScore)
                                delta = initScore - fakeScore

                                if delta < -0.1 or delta > 0.1:
                                        print("The generated review is not valid")
                                else:
                                        #print("The review: '" + review + "' is a valid review")
                                        print("Review created")
                                        related.fakeReviews.append(review)
                        
                        elif choice == "all":
                                review = related.getAdjRelated(sentence)
                                review = related.getNounRelated(review)
                                initScore = sa.analyzeSentence(sentence)['compound']
                                fakeScore = sa.analyzeSentence(review)['compound']
                                # print(initScore)
                                # print(fakeScore)
                                delta = initScore - fakeScore

                                if delta < -0.1 or delta > 0.1:
                                        print("The generated review is not valid")
                                else:
                                        #print("The review: '" + review + "' is a valid review")
                                        print("Review created")
                                        related.fakeReviews.append(review)
                        
                        else:
                                print("Your choice is invalid")
                                return []
                
                return related.fakeReviews