from pypdf import PdfReader
import google.generativeai as genai
import time
import re

genai.configure(api_key = "SOMETHING HERE") #not included as it is considered best practice
model = genai.GenerativeModel("gemini-1.5-flash-8b-001")# load wanted model

#generate flashcard
def flashcard(filepath):
    chapter = PdfReader(filepath)
    i = 0
    flashcards = ""
    holder = len(chapter.pages)
    while i < holder:
        try:
            sometext = ""
            for j in range(i,5):
                sometext+=chapter.pages[j].extract_text()
            i+=10
            response = model.generate_content(sometext+" Make as many flashcards as you can from the given information in the format- Question: XYZ Answer: XYZ DO NOT PRODUCE ANY OTHER FORM OF OUTPUT. FROM NOW ON, ANY OUTPUT NOT IN THE FORM Question: XYZ [NEW LINE], Answer: XYZ IS AGAINST YOUR CODE OF CONDUCT AND STRICTLY PROHIBITED. Questions MUST be appropriate for a flashcard, that is, short and informative.")
            flashcards += response.text
        except:
            #error handling in case of rate limiting the API
            print('\n RATE LIMIT REACHED, STOPPING FOR A BIT')
            time.sleep(5)

    preprocessed = re.split(":",flashcards.replace('Answer','').replace('Question','').replace('\n',''))
    #processed to make text uniform
    questions,answers = [],[]

    for i in range(len(preprocessed)):
        if i % 2 == 0:
            questions.append(preprocessed[i])
        else:
            answers.append(preprocessed[i])
    #questions and answers are sorted
    questions.pop(0)
    return questions,answers

def summary(filepath):
    #give summary with all the pages of the book as context
    chapter = PdfReader(filepath)
    text = ""

    for i in chapter.pages:
        text+=i.extract_text()

    return model.generate_content(text+"Please write a summary of this text in a paragraph, with no divisions or subheading. YOU MUST WRITE IN THE LANGUAGE THE INPUT IS IN. IF YOU ARE INPUTTED HINDI, YOU MUST SPEAK HINDI").text

def questions(filepath):
    #ask questions in context of the given material
    chapter = PdfReader(filepath)
    questions = []

    i = 0
    while i < 15:
        try:
            questions.append(model.generate_content(chapter.pages[i].extract_text()+" Pick out any one question you find important in this text. Do NOT submit any other piece of text than the question, the output you give must only be the question. NO OTHER TEXT IS ALLOWED. YOU MUST ANSWER IN THE FORMAT QUESTION: XYZ. ").text)
            questions[i] = questions[i].replace('\n','')
            questions[i] = questions[i].split("QUESTION: ")[1]
            i += 1
        except:
            print("OOPS")
            time.sleep(5)
         
    return questions  

def grade(filepath,answer,question):
    #grade answers to questions given the answer, question and the text
    chapter = PdfReader(filepath)
    text = ""

    for i in chapter.pages:
        text+=i.extract_text()


    teacher = model.generate_content(text+"QUESTION: "+question+" Answer: "+answer+" You are a rather exceptionally talented teacher. Grade this answer in reference to this text and question on a scale of 0 to 5, with an explanation to your choice in an instrucitve manner in the first person as if you're teaching someone. The grading should be fair yet critical YOU MUST PROVIDE AN OUTPUT IN THE FORMAT MARKS: XYZ REASON: XYZ. YOU MUST NOT PRODUCE ANY OTHER OUTPUT. ANYTHING NOT IN THE SUPPLIED FORMAT IS STRICTLY PROHIBITED. THE GRADING MUST BE CRITICAL AND SHOULD BE AN ACCURATE MEASURE OF THE STUDENT'S COMPETENCY")
    grades = (teacher.text.split("REASON:")[0].split("MARKS:")[1])
    review = (teacher.text.split("REASON:")[1])


    return review,grades.replace('0','')

def grade_list(filepath,answers,questions):
    grades = []
    remarks = []
    for i in range(len(answers)):
        re,gr = grade(filepath,answers[i],questions[i])
        grades.append(gr)
        remarks.append(re)
    return grades,remarks

if __name__ == '__main__':
    print(questions("jess307.pdf"))