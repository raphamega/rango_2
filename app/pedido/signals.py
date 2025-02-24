from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Mesa, Pedido, Item, Acrescimo
from app.firebaseconfig import db  # Importando a conexão com o Firestore

# 📌 Sincroniza a model Mesa com Firestore
@receiver(post_save, sender=Mesa)
def salvar_mesa_no_firestore(sender, instance, **kwargs):
    db.collection("mesas").document(str(instance.id)).set({
        "loja_id": instance.loja.id,
        "numero": instance.numero,
        "total": float(instance.total) if instance.total else None,
        "dinheiro": float(instance.dinheiro) if instance.dinheiro else None,
        "pix": float(instance.pix) if instance.pix else None,
        "debito": float(instance.debito) if instance.debito else None,
        "credito": float(instance.credito) if instance.credito else None,
        "fiado": float(instance.fiado) if instance.fiado else None,
        "frm_pg": instance.frm_pg,
        "status": instance.status
    })
    print(f"✅ Mesa {instance.numero} salva/atualizada no Firestore!")

@receiver(post_delete, sender=Mesa)
def deletar_mesa_no_firestore(sender, instance, **kwargs):
    db.collection("mesas").document(str(instance.id)).delete()
    print(f"❌ Mesa {instance.numero} removida do Firestore!")


# 📌 Sincroniza a model Pedido com Firestore
@receiver(post_save, sender=Pedido)
def salvar_pedido_no_firestore(sender, instance, **kwargs):
    db.collection("pedidos").document(str(instance.id)).set({
        "dia": instance.dia.strftime("%Y-%m-%d"),
        "loja_id": instance.loja.id,
        "usuario_id": instance.usuario.id,
        "mesa_id": instance.mesa.id if instance.mesa else None,
        "venda": instance.venda,
        "pedido": instance.pedido,
        "total_pedido": float(instance.total_pedido) if instance.total_pedido else None,
        "nome": instance.nome,
        "telefone": instance.telefone,
        "cep": instance.cep,
        "endereco": instance.endereco,
        "numero": instance.numero,
        "complemento": instance.complemento,
        "bairro": instance.bairro,
        "municipio": instance.municipio,
        "uf": instance.uf,
        "dinheiro": float(instance.dinheiro) if instance.dinheiro else None,
        "pix": float(instance.pix) if instance.pix else None,
        "debito": float(instance.debito) if instance.debito else None,
        "credito": float(instance.credito) if instance.credito else None,
        "fiado": float(instance.fiado) if instance.fiado else None,
        "frm_pg": instance.frm_pg,
        "status": instance.status
    })
    print(f"✅ Pedido {instance.id} salvo/atualizado no Firestore!")

@receiver(post_delete, sender=Pedido)
def deletar_pedido_no_firestore(sender, instance, **kwargs):
    db.collection("pedidos").document(str(instance.id)).delete()
    print(f"❌ Pedido {instance.id} removido do Firestore!")


# 📌 Sincroniza a model Item com Firestore
@receiver(post_save, sender=Item)
def salvar_item_no_firestore(sender, instance, **kwargs):
    db.collection("itens").document(str(instance.id)).set({
        "pedido_id": instance.pedido.id,
        "produto_id": instance.produto.id,
        "qt": float(instance.qt) if instance.qt else None,
        "preco": float(instance.preco) if instance.preco else None,
        "observacao": instance.observacao,
        "item_acrescimo": instance.item_acrescimo
    })
    print(f"✅ Item {instance.id} salvo/atualizado no Firestore!")

@receiver(post_delete, sender=Item)
def deletar_item_no_firestore(sender, instance, **kwargs):
    db.collection("itens").document(str(instance.id)).delete()
    print(f"❌ Item {instance.id} removido do Firestore!")


# 📌 Sincroniza a model Acrescimo com Firestore
@receiver(post_save, sender=Acrescimo)
def salvar_acrescimo_no_firestore(sender, instance, **kwargs):
    db.collection("acrescimos").document(str(instance.id)).set({
        "item_id": instance.item.id,
        "produto_id": instance.produto.id,
        "qt": float(instance.qt) if instance.qt else None,
        "preco": float(instance.preco) if instance.preco else None
    })
    print(f"✅ Acrescimo {instance.id} salvo/atualizado no Firestore!")

@receiver(post_delete, sender=Acrescimo)
def deletar_acrescimo_no_firestore(sender, instance, **kwargs):
    db.collection("acrescimos").document(str(instance.id)).delete()
    print(f"❌ Acrescimo {instance.id} removido do Firestore!")
