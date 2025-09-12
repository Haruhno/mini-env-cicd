from flask import Flask, request, jsonify, send_file
from config import Config
from services.image_service import ImageService
from services.email_service import EmailService
from io import BytesIO

app = Flask(__name__)
app.config.from_object(Config)

# Initialiser services
image_service = ImageService(app.config['MONGO_URI'])
email_service = EmailService(app)

@app.route('/api/images/upload', methods=['POST'])
def upload_image():
    # Vérifie si le fichier est présent dans la requête
    if 'file' not in request.files:
        return jsonify({"error": "No file part", "type": "Bad Request"}), 400
    
    file = request.files['file']
    
    # Vérifie si le fichier a un nom valide
    if file.filename == '':
        return jsonify({"error": "No selected file", "type": "Bad Request"}), 400
    
    try:
        # Tente d'uploader l'image
        image_id = image_service.upload_image(file)
        
        # Email désactivé temporairement
        # email_service.send_email(
        #     to_email="user@example.com",  
        #     subject="Image uploaded",
        #     body=f"Votre image a été uploadée avec l'ID: {image_id}"
        # )
        
        return jsonify({
            "message": "Image uploaded successfully", 
            "image_id": image_id,
            "type": "Success"
        }), 201
    
    except FileNotFoundError as fnf_error:
        # Exemple si le fichier ne peut pas être lu par le service
        return jsonify({"error": str(fnf_error), "type": "File Not Found"}), 404
    
    except ValueError as val_error:
        # Exemple si le service détecte un problème avec le fichier
        return jsonify({"error": str(val_error), "type": "Invalid Value"}), 400
    
    except Exception as e:
        # Toute autre erreur inattendue
        return jsonify({"error": str(e), "type": "Internal Server Error"}), 500




@app.route('/api/images/<image_id>', methods=['GET'])
def get_image(image_id):
    image_data = image_service.get_image(image_id)
    if not image_data:
        return jsonify({"error": "Image not found"}), 404
    
    return send_file(
        BytesIO(image_data['image_data']),
        mimetype=image_data['content_type'],
        download_name=image_data['name']
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
    






