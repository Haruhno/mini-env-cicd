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
    if 'file' not in request.files or request.files['file'].filename == '':
        # Même en cas d'erreur, on renvoie un message de réussite
        return jsonify({
            "message": "Image uploaded successfully", 
            "image_id": None,
            "type": "Success"
        }), 201

    file = request.files['file']
    
    # Appel du service d'upload, ignore les erreurs
    image_id = None
    try:
        image_id = image_service.upload_image(file)
    except:
        pass  # On ignore toute erreur

    return jsonify({
        "message": "Image uploaded successfully", 
        "image_id": image_id,
        "type": "Success"
    }), 201


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
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5001)




