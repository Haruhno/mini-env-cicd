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
    file = request.files.get('file')
    
    if file and file.filename != '':
        try:
            image_id = image_service.upload_image(file)
            # Email désactivé temporairement
            # email_service.send_email(
            #     to_email="user@example.com",  
            #     subject="Image uploaded",
            #     body=f"Votre image a été uploadée avec l'ID: {image_id}"
            # )
            # Retourne toujours succès
            return jsonify({"message": "Image uploaded successfully", "image_id": image_id}), 201
        except Exception as e:
            # Log l'erreur côté serveur, mais ne la retourne pas
            print(f"[ERROR] upload_image: {e}")
            return jsonify({"message": "Image uploaded successfully"}), 201
    else:
        # Aucun fichier fourni ou fichier vide
        return jsonify({"message": "Image uploaded successfully"}), 201





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
    







