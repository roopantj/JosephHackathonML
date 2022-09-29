from fastapi import FastAPI, File, UploadFile
from pdf2image import convert_from_path
import cv2
import shutil
import pytesseract
pytesseract.pytesseract.tesseract_cmd=r"C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"
app = FastAPI()


@app.post("/files/")
async def create_file(file: UploadFile):
    async def writePdf():
        with open("form.pdf","wb") as buffer:
           shutil.copyfileobj(file.file,buffer)
    await writePdf()        
    # Pdf to Image
    async def imgToPdf(): 
        pages = convert_from_path(pdf_path="form.pdf",poppler_path="C:\\Program Files\\poppler-0.68.0\\bin")
        for i in range(len(pages)):
            pages[i].save('img 1.jpg', 'JPEG')
    await imgToPdf()
    # Reading and resizing image
    try:
        image1 = cv2.imread("D:\Joseph Hackathom\ML Model\\img 1.jpg")
        image1_rs = cv2.resize(image1, (800, 800)) 
        cv2.imwrite("D:\Joseph Hackathom\ML Model\\img rsed.jpg",image1_rs)
        img = cv2.imread("img rsed.jpg")
        def getFields(img):
            crop_name = img[110:150, 227:600]  
            crop_age = img[150:190,227:375]
            crop_gender = img[150:190,520:665]
            crop_city = img[190:230,227:375]
            crop_state = img[190:230,520:665]
            crop_phone = img[230:270,227:665]
            crop_email = img[270:310,227:665]
            cv2.imwrite("D:\Joseph Hackathom\ML Model\\name.jpeg",crop_name)
            cv2.imwrite("D:\Joseph Hackathom\ML Model\\age.jpeg",crop_age)
            cv2.imwrite("D:\Joseph Hackathom\ML Model\\gender.jpeg",crop_gender)
            cv2.imwrite("D:\Joseph Hackathom\ML Model\\city.jpeg",crop_city)
            cv2.imwrite("D:\Joseph Hackathom\ML Model\\state.jpeg",crop_state)
            cv2.imwrite("D:\Joseph Hackathom\ML Model\\phone.jpeg",crop_phone)
            cv2.imwrite("D:\Joseph Hackathom\ML Model\\email.jpeg",crop_email)
        getFields(img)    
    except Exception as e:
        print(str(e))   
         
    
    
    cv2.waitKey(0) 
    cv2.destroyAllWindows()
    
    return {"file_name": file.filename}  

@app.get("/")
def welcome():
    return {"message":"Welcome"}