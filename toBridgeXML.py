import sys, datetime
from BeautifulSoup import BeautifulSoup, CData, Tag
import xml.etree.ElementTree as ET 
from xml.etree import ElementTree
from xml.dom import minidom

questionTitle = []
#correctAnswer = ''
question=""
choice = ""
global sourcetext
#global qtype
sourcetext = ""
qtype = ""
qoption = ""
de = []

def getQuestionType(): # getting Question Type. DONE.
	global qtype
	qtype = ""
	tree = ET.ElementTree(file='examplemoodle.xml')
	for elem in tree.iter('question'):
		qtype = str(elem.get('type'))

	if qtype == 'multichoice':
			qtype = "multiplechoice"
	
	#print qtype
	

def getQuestionText(): #sub class for getting All Question - TEXT. DONE
	global qtext
	mustDelChar = ";:-=,\""
	mustDelWord=["<p>","</p>","<span stylefontfamily times new romantimesserif fontsize large>","<br />","</span>"]
	tree = ET.ElementTree(file='examplemoodle.xml')
	for elem in tree.iter('questiontext'):
		qtext = elem.find('text').text

		for i in range (0,len(mustDelChar)):
			qtext = qtext.replace(mustDelChar[i],"")

		for i in mustDelWord:
			qtext = qtext.replace(i,"")

		#print qtext

def getQuestionOption(): # getting Question Type. DONE.
	global qoption
	qoption = ""
	tree = ET.ElementTree(file='examplemoodle.xml')
	for elem in tree.findall('question'):
		qoption = str(elem.find('shuffleanswers').text)

	if qoption == '1':
		qoption = 'TRUE'
	else:
		qoption = 'FALSE'
	

def getAllQuestionAnswer(): #sub class for getting All Question - Answer DONE
	mustDelChar = ";:-=,\""
	mustDelWord=["<p>","</p>","<span stylefontfamily times new romantimesserif fontsize large>","<br />","</span>"]
	global de
	de = []
	global fracnumber 
	fracnumber = []
	tree = ET.ElementTree(file='examplemoodle.xml')
	listnilai=[]
	global answerID
	answerID = ""
	global konter
	konter = 0
	for elem in tree.iter('answer'):
		frac = int(elem.get('fraction'))
		txt = elem.find('text').text
		konter = konter + 1
		
		if frac == 100:
			answerID = str(konter)

		for i in range (0,len(mustDelChar)):
			txt = txt.replace(mustDelChar[i],"")

		for i in mustDelWord:
			txt = txt.replace(i,"")

		de.append(txt)
		fracnumber.append(str(frac))

def prettify(elem): #Use for writeBridgexml
    
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def writeBridgexml(): #For write to BrideXML DONE
	from xml.etree.ElementTree import Element, SubElement, Comment
	#from ElementTree_pretty import prettify

	question = Element('question')

	comment = Comment('This is bridge xml by @xunilresu')
	question.append(comment)

	questiondata = SubElement(question, 'questiondata')
	
	getQuestionType()
	questiontype = SubElement(questiondata, 'questiontype')
	questiontype.text = qtype

	getQuestionText()
	questiontext = SubElement(questiondata, 'questiontext')
	questiontext.text = qtext

	getAllQuestionAnswer()
	questionanswerlisttag = [
		SubElement(questiondata,'questionanswer', id=str(i), text=de[i-1], score=fracnumber[i-1])
		for i in xrange(1,5)
		]

	
	correctanswer = SubElement(questiondata, 'correctanswer')
    
	correctanswerid = SubElement(correctanswer, 'correctanswerid')
	correctanswerid.text = answerID
	

	getQuestionOption()
	randomoption = SubElement(questiondata, 'randomoption')
	randomoption.text = qoption
    
	skrg = str(datetime.datetime.now())

	bridgeXMLFileName = 'bridge'+skrg+'.xml'

	#start for writting to bridge.xml -->uncomment this below
	temp = sys.stdout
	sys.stdout = open(bridgeXMLFileName,'w')
	print prettify(question)
	sys.stdout.close() 
	sys.stdout = temp
	print 'Export Successfull, Filename = '+bridgeXMLFileName

	
	
#exampleGetFromCData()
#getCDatainside()
#getAllAnswerTagMoodleXML()
#getQuestionType()
#getQuestionOption()
writeBridgexml()
