from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Und_Medida, Fornecedor_Model, Nota_Model, Item_Model
from app.firebaseconfig import db  # Importando a conexão com o Firestore

# 📌 Sincroniza a model Und_Medida com Firestore
@receiver(post_save, sender=Und_Medida)
def salvar_und_medida_no_firestore(sender, instance, **kwargs):
    db.collection("und_medidas").document(str(instance.id)).set({
        "nome": instance.nome
    })
    print(f"✅ Unidade de Medida {instance.nome} salva/atualizada no Firestore!")

@receiver(post_delete, sender=Und_Medida)
def deletar_und_medida_no_firestore(sender, instance, **kwargs):
    db.collection("und_medidas").document(str(instance.id)).delete()
    print(f"❌ Unidade de Medida {instance.nome} removida do Firestore!")


# 📌 Sincroniza a model Fornecedor_Model com Firestore
@receiver(post_save, sender=Fornecedor_Model)
def salvar_fornecedor_no_firestore(sender, instance, **kwargs):
    db.collection("fornecedores").document(str(instance.id)).set({
        "loja_id": instance.loja.id,
        "nome": instance.nome,
        "cnpj": instance.cnpj,
        "telefone": instance.telefone,
        "cep": instance.cep,
        "endereco": instance.endereco,
        "numero": instance.numero,
        "complemento": instance.complemento,
        "bairro": instance.bairro,
        "municipio": instance.municipio,
        "UF": instance.UF
    })
    print(f"✅ Fornecedor {instance.nome} salvo/atualizado no Firestore!")

@receiver(post_delete, sender=Fornecedor_Model)
def deletar_fornecedor_no_firestore(sender, instance, **kwargs):
    db.collection("fornecedores").document(str(instance.id)).delete()
    print(f"❌ Fornecedor {instance.nome} removido do Firestore!")


# 📌 Sincroniza a model Nota_Model com Firestore
@receiver(post_save, sender=Nota_Model)
def salvar_nota_no_firestore(sender, instance, **kwargs):
    db.collection("notas").document(str(instance.id)).set({
        "loja_id": instance.loja.id,
        "nf": instance.nf,
        "dia": instance.dia,
        "movimento": instance.movimento,
        "total": instance.total,
        "status": instance.status
    })
    print(f"✅ Nota Fiscal {instance.nf} salva/atualizada no Firestore!")

@receiver(post_delete, sender=Nota_Model)
def deletar_nota_no_firestore(sender, instance, **kwargs):
    db.collection("notas").document(str(instance.id)).delete()
    print(f"❌ Nota Fiscal {instance.nf} removida do Firestore!")


# 📌 Sincroniza a model Item_Model com Firestore
@receiver(post_save, sender=Item_Model)
def salvar_item_no_firestore(sender, instance, **kwargs):
    db.collection("itens").document(str(instance.id)).set({
        "loja_id": instance.loja.id,
        "produto_id": instance.produto.id,
        "nota_id": instance.nota.id,
        "data_validade": instance.data_validade,
        "ncm": instance.ncm,
        "unidade_id": instance.unidade.id if instance.unidade else None,
        "quantidade": instance.quantidade,
        "preco_unid": float(instance.preco_unid) if instance.preco_unid else None,
        "preco": float(instance.preco) if instance.preco else None
    })
    print(f"✅ Item {instance.id} salvo/atualizado no Firestore!")

@receiver(post_delete, sender=Item_Model)
def deletar_item_no_firestore(sender, instance, **kwargs):
    db.collection("itens").document(str(instance.id)).delete()
    print(f"❌ Item {instance.id} removido do Firestore!")
