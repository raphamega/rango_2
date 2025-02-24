import os
import firebase_admin
from firebase_admin import credentials, firestore, storage
from django.conf import settings
# Configurar a conexão com o Firestore

cred = credentials.Certificate(os.path.join(settings.BASE_DIR,f"rango_bb48f.json"))
firebase_admin.initialize_app(cred,{
    "storageBucket": "seu-projeto.appspot.com"  # Substitua pelo seu Firebase Storage
})

db = firestore.client()
bucket = storage.bucket()
class Conexao():
   
   def testar_conexao():

    try:
        # Criando um documento de teste no Firestore
        db.collection("test_connection").document("ping").set({"mensagem": "Conexão bem-sucedida!"})

        # Buscando o documento para confirmar que foi salvo
        doc = db.collection("test_connection").document("ping").get()
        if doc.exists:
            print("✅ Conexão com o Firebase Firestore bem-sucedida!")
            print("📄 Mensagem do Firestore:", doc.to_dict())
        else:
            print("⚠️ Erro: Não foi possível recuperar o documento de teste.")
    
    except Exception as e:
        print("❌ Erro ao conectar ao Firebase:", e)

    # Chamando a função para testar
