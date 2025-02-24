from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Usuario_Model, Loja_Model
from app.firebaseconfig import db  # Importando a conexão com o Firestore

# 📌 Sincroniza a model Usuario_Model com Firestore
@receiver(post_save, sender=Usuario_Model)
def salvar_usuario_no_firestore(sender, instance, **kwargs):
    db.collection("usuarios").document(str(instance.id)).set({
        "usuario_id": instance.usuario.id,
        "nome_completo": instance.nome_completo,
        "cpf": instance.cpf,
        "telefone": instance.telefone,
        "cep": instance.cep,
        "endereco": instance.endereco,
        "numero": instance.numero,
        "bairro": instance.bairro,
        "municipio": instance.municipio,
        "UF": instance.UF
    })
    print(f"✅ Usuário {instance.nome_completo} salvo/atualizado no Firestore!")

@receiver(post_delete, sender=Usuario_Model)
def deletar_usuario_no_firestore(sender, instance, **kwargs):
    db.collection("usuarios").document(str(instance.id)).delete()
    print(f"❌ Usuário {instance.nome_completo} removido do Firestore!")


# 📌 Sincroniza a model Loja_Model com Firestore
@receiver(post_save, sender=Loja_Model)
def salvar_loja_no_firestore(sender, instance, **kwargs):
    db.collection("lojas").document(str(instance.id)).set({
        "usuario_id": instance.usuario.id,
        "loja": instance.loja,
        "cnpj": instance.cnpj,
        "telefone": instance.telefone,
        "cep": instance.cep,
        "endereco": instance.endereco,
        "numero": instance.numero,
        "complemento": instance.complemento,
        "bairro": instance.bairro,
        "municipio": instance.municipio,
        "UF": instance.UF,
        "image_url": instance.image.url if instance.image else None,
        "ativo": instance.ativo,
        "aberto": instance.aberto,
        "categoria": instance.categoria,
        "tipo": instance.tipo
    })
    print(f"✅ Loja {instance.loja} salva/atualizada no Firestore!")

@receiver(post_delete, sender=Loja_Model)
def deletar_loja_no_firestore(sender, instance, **kwargs):
    db.collection("lojas").document(str(instance.id)).delete()
    print(f"❌ Loja {instance.loja} removida do Firestore!")
