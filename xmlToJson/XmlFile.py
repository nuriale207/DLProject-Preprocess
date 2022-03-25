import xml.etree.ElementTree as ET
import json




class XmlFile():
    def __init__(self, file_path,file_name):
        self.tree=ET.parse(file_path)
        self.root = self.tree.getroot()
        self.event_dict=dict()
        self.tLink=dict()
        self.aLink = dict()
        self.timexLink=dict()
        self.file_name=file_name
        self.entity_types=set()
        self.relation_types = set()

    def getFullText(self):
        for text in self.root.iter('{http:///uima/cas.ecore}Sofa'):
            self.text=text.attrib['sofaString']

    def getSentences(self):
        self.sentences=[]
        for sentence in self.root.iter('{http:///de/tudarmstadt/ukp/dkpro/core/api/segmentation/type.ecore}Sentence'):
            begin=sentence.attrib['begin']
            end=sentence.attrib['end']
            self.sentences.append({"sentence":self.text[int(begin):int(end)],"begin":int(begin),"end":int(end)})

    def getSentenceTokens(self):
        self.tokens=[]
        self.tokensID=[]
        all_tokens=self.getTokens()
        i=0
        for sentence in self.sentences:
            tokens=[]
            tokensID=[]
            if(i<len(all_tokens)-1):
                while(int(all_tokens[i]['end'])<=sentence['end'] and i<len(all_tokens)-1):
                    tokenText=self.text[int(all_tokens[i]["begin"]):int(all_tokens[i]["end"])]
                    tokens.append(tokenText)

                    tokensID.append({"token":tokenText,"id":tokens.index(tokenText),"begin":(int(all_tokens[i]["begin"])),"end":(int(all_tokens[i]["end"]))})
                    i+=1
                self.tokens.append({'tokens':tokens})
                self.tokensID.append(tokensID)

    def getTokens(self):
        tokens=[]
        for token in self.root.iter('{http:///de/tudarmstadt/ukp/dkpro/core/api/segmentation/type.ecore}Token'):
            begin = token.attrib['begin']
            end = token.attrib['end']
            tokens.append({"begin": begin, "end": end})
        return tokens

    def getEntities(self):
        self.entities=[]


    def getSentenceEvents(self):
        self.events=[]
        i=0
        all_events=self.getEvents()
        for sentence in self.sentences:
            events=[]
            if(i<=len(all_events)-1):
                eventStart=int(all_events[i]['end'])
            else:
                eventStart = sentence['end']+100

            while eventStart<=sentence['end'] and i<=len(all_events)-1:

                start=int(all_events[i]['begin'])-int(sentence["begin"])
                end=int(all_events[i]['end'])-int(sentence["begin"])
                # if(end>sentence['end']):
                #     end=sentence["end"]

                events.append({"type":all_events[i]['type'],"start":start,"end":end})

                self.event_dict[all_events[i]["id"]]={"sentenceIndex":self.sentences.index(sentence),"eventIndex":len(events)-1}
                self.entity_types.add(all_events[i]['type'])
                if(all_events[i]["TLINK"]!=None):
                    self.addTlinks(all_events[i])

                if (all_events[i]["ALINK"] != None):
                    self.addAlinks(all_events[i])
                i+=1
                if (i <= len(all_events) - 1):
                    eventStart = int(all_events[i]['end'])
                else:
                    eventStart = sentence['end'] + 100
            self.events.append(events)

    def addTlinks(self, event):
        tlinks=event["TLINK"]
        tlinks=tlinks.split(" ")
        for link in tlinks:
            self.tLink[link]=event["id"]

    def addAlinks(self, event):
        tlinks=event["ALINK"]
        tlinks=tlinks.split(" ")
        for link in tlinks:
            self.aLink[link]=event["id"]

    def getEvents(self):
        events=[]

        for event in self.root.iter('{http:///webanno/custom.ecore}EVENT'):
            # print(event.attrib)
            type=event.attrib['docTimeRel']

            begin = event.attrib['begin']
            end = event.attrib['end']
            id=event.attrib["{http://www.omg.org/XMI}id"]
            if("TLINK" in event.attrib.keys() ):
                tlink=event.attrib['TLINK']
            else:
                tlink=None

            if("ALINK" in event.attrib.keys()):
                alink = event.attrib['ALINK']
            else:
                alink = None
            events.append({'type':type, 'begin':begin, 'end':end,"id":id,"TLINK":tlink,"ALINK":alink})
        return events

    def getSentenceExpressions(self):
        self.expressions=[]
        i=0
        all_expressions=self.getExpressions()
        for sentence in self.sentences:
            expressions=[]
            if (i <= len(all_expressions) - 1):
                eventStart = int(all_expressions[i]['end'])
            else:
                eventStart = sentence['end'] + 100

            while eventStart <= sentence['end'] and i <= len(all_expressions) - 1:
                start=int(all_expressions[i]['begin'])-int(sentence["begin"])
                end=int(all_expressions[i]['end'])-int(sentence["begin"])
                expressions.append({"type":all_expressions[i]['type'],"start":start,"end":end})
                self.event_dict[all_expressions[i]['id']]={"sentenceIndex":self.sentences.index(sentence),"eventIndex":len(expressions)-1}
                self.entity_types.add(all_expressions[i]['type'])
                if(all_expressions[i]["timexlink"]!=None):
                    self.addTxlinks(all_expressions[i])
                i+=1
                if (i <= len(all_expressions) - 1):
                    eventStart = int(all_expressions[i]['end'])
                else:
                    eventStart = sentence['end'] + 100
            self.expressions.append(expressions)

    def addTxlinks(self, event):
        tXlinks=event["timexlink"]
        tXlinks=tXlinks.split(" ")
        for link in tXlinks:
            self.timexLink[link]=event["id"]

    def getExpressions(self):
        expressions=[]
        for expression in self.root.iter('{http:///webanno/custom.ecore}TIMEX3'):
            type=expression.attrib['timex3Class']
            begin = expression.attrib['begin']
            end = expression.attrib['end']

            id=expression.attrib["{http://www.omg.org/XMI}id"]
            if ("timexLink" in expression.attrib.keys()):
                timexLink = expression.attrib['timexLink']
            else:
                timexLink = None
            expressions.append({'type':type, 'begin':begin, 'end':end,"id":id,"timexlink":timexLink})
        return expressions

    def getSentenceActors(self):
        self.actors=[]
        i=0
        all_actors=self.getActors()
        for sentence in self.sentences:
            actors=[]
            if (i <= len(all_actors) - 1):
                eventStart = int(all_actors[i]['end'])
            else:
                eventStart = sentence['end'] + 100

            while eventStart<=sentence['end'] and i<=len(all_actors)-1:
                start=int(all_actors[i]['begin'])-int(sentence["begin"])
                end=int(all_actors[i]['end'])-int(sentence["begin"])
                actors.append({"type":all_actors[i]['type'],"start":start,"end":end})
                self.event_dict[all_actors[i]['id']]={"sentenceIndex":self.sentences.index(sentence),"eventIndex":len(actors)-1}
                self.entity_types.add(all_actors[i]['type'])
                i+=1

                if (i <= len(all_actors) - 1):
                    eventStart = int(all_actors[i]['end'])
                else:
                    eventStart = sentence['end'] + 100
            self.actors.append(actors)

    def getActors(self):
        actors=[]
        for actor in self.root.iter('{http:///webanno/custom.ecore}ACTOR'):
            type=actor.attrib['role']
            begin = actor.attrib['begin']
            end = actor.attrib['end']
            id = actor.attrib["{http://www.omg.org/XMI}id"]
            actors.append({'type':type, 'begin':begin, 'end':end,"id":id})
        return actors

    def getSentenceBodyParts(self):
        self.body_parts=[]
        i=0
        all_body_parts=self.getBodyParts()
        for sentence in self.sentences:
            body_parts=[]
            if (i <= len(all_body_parts) - 1):
                eventStart = int(all_body_parts[i]['end'])
            else:
                eventStart = sentence['end'] + 100
            while eventStart<=sentence['end'] and i<=len(all_body_parts)-1:
                start = int(all_body_parts[i]['begin']) - int(sentence["begin"])
                end = int(all_body_parts[i]['end']) - int(sentence["begin"])
                body_parts.append({"type": all_body_parts[i]['type'], "start": start, "end": end})
                self.event_dict[all_body_parts[i]['id']]={"sentenceIndex":self.sentences.index(sentence),"eventIndex":len(body_parts)-1}
                self.entity_types.add(all_body_parts[i]['type'])
                i+=1

                if (i <= len(all_body_parts) - 1):
                    eventStart = int(all_body_parts[i]['end'])
                else:
                    eventStart = sentence['end'] + 100
            self.body_parts.append(body_parts)

    def getBodyParts(self):
        body_parts=[]
        for body_part in self.root.iter('{http:///webanno/custom.ecore}BODYPART'):
            type="Body_part"
            begin = body_part.attrib['begin']
            end = body_part.attrib['end']
            id = body_part.attrib["{http://www.omg.org/XMI}id"]
            body_parts.append({'type':type, 'begin':begin, 'end':end,"id":id})
        return body_parts

    def getSentenceRML(self):
        self.rml=[]
        i=0
        all_rml=self.getRML()
        for sentence in self.sentences:
            rml=[]
            if (i <= len(all_rml) - 1):
                eventStart = int(all_rml[i]['end'])
            else:
                eventStart = sentence['end'] + 100
            while eventStart<=sentence['end'] and i<=len(all_rml)-1:
                start = int(all_rml[i]['begin']) - int(sentence["begin"])
                end = int(all_rml[i]['end']) - int(sentence["begin"])
                rml.append({"type": all_rml[i]['type'], "start": start, "end": end})
                self.event_dict[all_rml[i]['id']]={"sentenceIndex":self.sentences.index(sentence),"eventIndex":len(rml)-1}
                self.entity_types.add(all_rml[i]['type'])
                i+=1

                if (i <= len(all_rml) - 1):
                    eventStart = int(all_rml[i]['end'])
                else:
                    eventStart = sentence['end'] + 100
            self.rml.append(rml)

    def getRML(self):
        rmls=[]
        for rml in self.root.iter('{http:///webanno/custom.ecore}RML'):
            type="RML"
            begin = rml.attrib['begin']
            end = rml.attrib['end']
            id = rml.attrib["{http://www.omg.org/XMI}id"]
            rmls.append({'type':type, 'begin':begin, 'end':end,"id":id})
        return rmls

    def getRelations(self):
        self.relations=[[] for i in range(len(self.sentences))]


        for event in self.root.iter('{http:///webanno/custom.ecore}EVENTTLINKLink'):
            head=event.attrib["{http://www.omg.org/XMI}id"]
            tail=event.attrib['target']
            role=event.attrib['role']
            self.relation_types.add(role)
            sentence=self.event_dict[tail]["sentenceIndex"]
            tailIndex=self.event_dict[tail]["eventIndex"]
            eventID=self.tLink[head]
            if(eventID==None):
                eventID=self.timexLink[tail]
            headIndex=self.event_dict[eventID]["eventIndex"]
            if(self.relations[sentence]==None):
                self.relations[sentence]=[{"type":role,"head":headIndex,"tail":tailIndex}]
            else:
                self.relations[sentence].append({"type":role,"head":headIndex,"tail":tailIndex})

        for event in self.root.iter('{http:///webanno/custom.ecore}EVENTALINKLink'):
            head=event.attrib["{http://www.omg.org/XMI}id"]
            tail=event.attrib['target']
            role=event.attrib['role']
            self.relation_types.add(role)
            sentence=self.event_dict[tail]["sentenceIndex"]
            tailIndex=self.event_dict[tail]["eventIndex"]
            eventID=self.aLink[head]
            if(eventID==None):
                eventID=self.timexLink[tail]
            headIndex=self.event_dict[eventID]["eventIndex"]
            if(self.relations[sentence]==None):
                self.relations[sentence]=[{"type":role,"head":headIndex,"tail":tailIndex}]
            else:
                self.relations[sentence].append({"type":role,"head":headIndex,"tail":tailIndex})

        for event in self.root.iter('{http:///webanno/custom.ecore}TIMEX3TimexLinkLink'):
            head=event.attrib["{http://www.omg.org/XMI}id"]
            tail=event.attrib['target']
            role=event.attrib['role']
            self.relation_types.add(role)
            sentence=self.event_dict[tail]["sentenceIndex"]
            tailIndex=self.event_dict[tail]["eventIndex"]
            eventID=self.timexLink[head]
            if(eventID==None):
                eventID=self.timexLink[tail]
            headIndex=self.event_dict[eventID]["eventIndex"]
            if(self.relations[sentence]==None):
                self.relations[sentence]=[{"type":role,"head":headIndex,"tail":tailIndex}]
            else:
                self.relations[sentence].append({"type":role,"head":headIndex,"tail":tailIndex})
            #self.relations[sentence].append({"type": role, "head": headIndex, "tail": tailIndex})
        self.addNoRelations()

    def addNoRelations(self):

        for sentence in range(len(self.sentences)):
            entities = self.mergeEntities(sentence)
            for entity1 in range(len(entities)):
                for entity2 in range(entity1+1,len(entities)-1):
                    if(self.isRelation(entity1,entity2,sentence)==False):
                        self.relations[sentence].append({"type":"NO-RELATION","head":entity1,"tail":entity2})

    def isRelation(self, idEntity1,idEntity2,idSentence):
        relations=self.relations[idSentence]
        isRelation=False
        for relation in relations:
            if(relation["head"]==idEntity1 and relation["tail"]==idEntity2):
                isRelation=True
                break
        return isRelation

    def mergeEntities(self,sentence):
        return self.events[sentence] + self.expressions[sentence] + self.actors[sentence] + self.body_parts[sentence] + \
               self.rml[sentence]
    def mergeTokensEntitiesRelations(self):
        all_info=[]
        for sentence in range(len(self.sentences)):
            info={"tokens":self.tokens[sentence]["tokens"],
                  "entities":self.mergeEntities(sentence),
                  "relations":self.relations[sentence],
                  "orig_id":self.file_name}
            all_info.append(info)

        #all_info=json.dumps(all_info)
        #print(len(all_info))
        return all_info

    def getRelationTypes(self):
        return self.relation_types

    def getEntityTypes(self):
        return self.entity_types

    def correctIDs(self,all_info):
        i=0
        for sentence in all_info:
            entities=sentence["entities"]
            for entity in entities:
                self.correctEntityIDs(i,entity)
            i+=1

    def correctEntityIDs(self,sentenceID,entity):

        sentenceStart = self.sentences[sentenceID]["begin"]
        sentenceEnd = self.sentences[sentenceID]["end"]
        # if(entity["type"]=="PATIENT" or entity["type"]=="RML" or entity["type"]=="Body_part" or entity["type"]=="H-PROFESSIONAL"):
        #     entityStart=entity["start"]-sentenceStart
        #     entityEnd=entity["end"]-sentenceEnd
        # else:
        entityStart = entity["start"]
        entityEnd = entity["end"]
        i=0
        start=False
        startID =entityStart
        endID=entityEnd
        tokens=self.tokensID[sentenceID]

        while i<len(tokens):
            # tokenBegin=tokens[i]["begin"]-sentenceStart
            # tokenEnd=tokens[i]["end"]-sentenceStart
            tokenBegin = tokens[i]["begin"] - sentenceStart
            tokenEnd = tokens[i]["end"] - sentenceStart
            if tokenBegin>=entityEnd:
                # startID = tokens[i]["id"]
                # endID = tokens[i]["id"]
                endID = tokens[i-1]["id"]+1
                break
            elif tokenEnd>=entityStart:
                if not start:
                    startID=tokens[i]["id"]
                    start=True
                else:
                    endID=tokens[i]["id"]+1
            i+=1
        if(endID==entityEnd):
            endID=startID
        entity["start"]=startID
        entity["end"]=endID

    def xmlToJson(self):
        self.getFullText()
        self.getSentences()
        self.getSentenceTokens()
        self.getSentenceEvents()
        self.getSentenceExpressions()
        self.getSentenceRML()
        self.getSentenceActors()
        self.getSentenceBodyParts()
        # print(self.tLink)
        # print(self.event_dict)
        # print("8925" in self.event_dict)
        # print(self.sentences)
        self.getRelations()
        all_info=self.mergeTokensEntitiesRelations()
        self.correctIDs(all_info)
        return all_info