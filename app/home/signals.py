from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Pag_Contato, Texto
from app.firebaseconfig import db  # Importando a conexão com o Firestore

# 📌 Sincroniza a model Pag_Contato com Firestore
@receiver(post_save, sender=Pag_Contato)
def salvar_pag_contato_no_firestore(sender, instance, **kwargs):
    """Sempre que um contato for criado ou atualizado no Django, ele será salvo no Firestore"""
    db.collection("pag_contato").document(str(instance.id)).set({
        "nome": instance.nome,
        "email": instance.email,
        "mensagem": instance.mensagem
    })
    print(f"✅ Contato {instance.nome} salvo/atualizado no Firestore!")

@receiver(post_delete, sender=Pag_Contato)
def deletar_pag_contato_no_firestore(sender, instance, **kwargs):
    """Sempre que um contato for excluído no Django, ele será removido do Firestore"""
    db.collection("pag_contato").document(str(instance.id)).delete()
    print(f"❌ Contato {instance.nome} removido do Firestore!")


# 📌 Sincroniza a model Texto com Firestore
@receiver(post_save, sender=Texto)
def salvar_texto_no_firestore(sender, instance, **kwargs):
    """Sempre que um texto for criado ou atualizado no Django, ele será salvo no Firestore"""
    db.collection("textos").document(str(instance.id)).set({
        "titulo": instance.titulo,
        "texto": instance.texto,
        "image_url": instance.image.url if instance.image else None
    })
    print(f"✅ Texto {instance.titulo} salvo/atualizado no Firestore!")

@receiver(post_delete, sender=Texto)
def deletar_texto_no_firestore(sender, instance, **kwargs):
    """Sempre que um texto for excluído no Django, ele será removido do Firestore"""
    db.collection("textos").document(str(instance.id)).delete()
    print(f"❌ Texto {instance.titulo} removido do Firestore!")
