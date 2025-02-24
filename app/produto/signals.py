
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Produto_Model
from app.firebaseconfig import db, bucket

def upload_image_to_firebase(instance):
    """Faz upload da imagem do produto para o Firebase Storage e retorna a URL pública."""
    if instance.image:  # Verifica se há uma imagem
        image_path = f"produtos/{instance.id}.jpg"  # Caminho da imagem no Firebase Storage
        blob = bucket.blob(image_path)
        blob.upload_from_filename(instance.image.path)  # Faz upload do arquivo
        blob.make_public()  # Torna a imagem pública
        return blob.public_url  # Retorna a URL pública
    return None

@receiver(post_save, sender=Produto_Model)
def salvar_produto_no_firestore(sender, instance, **kwargs):
    """Sincroniza os produtos do Django com o Firestore e Firebase Storage."""
    image_url = upload_image_to_firebase(instance)  # Faz upload da imagem e obtém a URL
    
    db.collection("produtos").document(str(instance.id)).set({
        "loja_id": instance.loja.id,
        "codigo": instance.codigo,
        "data_compra": instance.data_compra,
        "data_validade": instance.data_validade,
        "nome": instance.nome,
        "categoria": instance.categoria,
        "descricao": instance.descricao,
        "preco_compra": float(instance.preco_compra) if instance.preco_compra else None,
        "preco": float(instance.preco) if instance.preco else None,
        "estoque": instance.estoque,
        "estoque_minimo": instance.estoque_minimo,
        "controle_estoque": instance.controle_estoque,
        "ativo": instance.ativo,
        "image_url": image_url  # Salva a URL da imagem no Firestore
    })
    print(f"✅ Produto {instance.nome} salvo/atualizado no Firestore com imagem!")

