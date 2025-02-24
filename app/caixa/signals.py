from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Caixa
from app.firebaseconfig import db  # Importando a conexão com o Firestore

# 📌 Sincroniza a model Caixa com Firestore
@receiver(post_save, sender=Caixa)
def salvar_caixa_no_firestore(sender, instance, **kwargs):
    """Sempre que um caixa for criado ou atualizado no Django, ele será salvo no Firestore"""
    db.collection("caixas").document(str(instance.id)).set({
        "loja_id": instance.loja.id,
        "data": instance.data.strftime("%Y-%m-%d %H:%M:%S"),
        "descricao": instance.descricao,
        "valor": float(instance.valor) if instance.valor else None,
        "dinheiro": float(instance.dinheiro) if instance.dinheiro else None,
        "pix": float(instance.pix) if instance.pix else None,
        "debito": float(instance.debito) if instance.debito else None,
        "credito": float(instance.credito) if instance.credito else None,
        "fiado": float(instance.fiado) if instance.fiado else None,
        "tipo": instance.tipo
    })
    print(f"✅ Caixa {instance.id} salvo/atualizado no Firestore!")

@receiver(post_delete, sender=Caixa)
def deletar_caixa_no_firestore(sender, instance, **kwargs):
    """Sempre que um caixa for excluído no Django, ele será removido do Firestore"""
    db.collection("caixas").document(str(instance.id)).delete()
    print(f"❌ Caixa {instance.id} removido do Firestore!")
