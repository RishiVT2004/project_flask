from PIL import Image
from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import cv2
import os

app = Flask(__name__)

UPLOAD_FOLDER = r'C:\Users\DELL\Desktop\image_uploaded' #r -> raw string path
ALLOWED_EXTENSIONS = {'png','jpeg','jpg','webp'} 

app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename): #allowing given extentions 
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 
           

def process_Image(filename,option):
    print(f'filename : {filename}')
    print(f'opeartion to perform : {option}')
    img = cv2.imread(f"{UPLOAD_FOLDER}/{filename}") #cv2 reads file uploaded *** upload using f"" strings..
    
    match option: #like switch case in java...  
        case "convert_gray" : 
            img_processed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #process new image 
            new_filename = f"{UPLOAD_FOLDER}/{filename}"
            cv2.imwrite(new_filename, img_processed)
            return new_filename        
        
        case "convert_jpeg": 
            new_filename = f"{UPLOAD_FOLDER}/{filename.split('.')[0]}.jpeg"
            cv2.imwrite(new_filename,img)
            return new_filename    
             
        case "convert_png": 
            new_filename = f"{UPLOAD_FOLDER}/{filename.split('.')[0]}.png"
            cv2.imwrite(new_filename,img)
            return new_filename        
        
        case "convert_webp": 
            new_filename = f"{UPLOAD_FOLDER}/{filename.split('.')[0]}.webp"
            cv2.imwrite(new_filename,img)
            return new_filename   
        
        case "convert_brg":
            img_processed = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
            new_filename = f"{UPLOAD_FOLDER}/{filename}" 
            cv2.imwrite(new_filename, img_processed)
            return new_filename   
            
        #case "cpng": 
            #newFilename = f"static/{filename.split('.')[0]}.png"
            #cv2.imwrite(newFilename, img)
            #return newFilename     
    pass        
    


@app.route('/')
def home_page():
    return render_template('new_index.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/documents')
def get_doucmentation():
    return render_template('documents.html')

@app.route('/login')
def fet_login():
    return render_template('login.html')


@app.route('/signup')
def fet_sign_up():
    return render_template('signup.html')
    

@app.route('/edit', methods=["GET", "POST"])
def edit():
    if request.method == "POST": 
        #selecting operation -: 
        option = request.form.get("option")
    # check if the post request has the file part
        if 'file' not in request.files: #file name -> file ** to be inserted in html
            return f"Error : --- FILE NOT PRESENT ---"
        
        file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
        
        if file.filename == '':
            flash('No selected file')
            return f'Error --- NO FILES SELECTED --- : '
        
        if option == "":
            flash('no option selected')
            return f"ERROR - no option selected"
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename) #checking secure filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #if file is valid upload to 'UPLOAD_FOLDER'
            
            process_Image(filename,option) #process file to convert to selected option
            flash(f"image processed and can be viewed in your selected folder")
            return render_template('new_index.html')
    else:
        return f"ERROR"

if __name__ ==  "__main__":
    app.run(debug=True,port=8880)
