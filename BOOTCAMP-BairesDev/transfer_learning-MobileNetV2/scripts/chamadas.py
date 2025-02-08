from tensorflow.keras.callbacks import (  # type: ignore
    EarlyStopping,
    ModelCheckpoint,
    ReduceLROnPlateau,
)

from constantes import MELHOR_MODELO, MELHOR_MODELO_AJUSTE


# Função para retornar os callbacks para o treinamento do modelo
def retorno_chamada(pasta_modelo):
    """
    Retorna os callbacks para o treinamento do modelo

    Argumentos:
            pasta_modelo - str: Caminho para salvar o modelo

    Retorno:
            checkpoint_MobileNetV2 - ModelCheckpoint: Salva o melhor modelo
            lr_reduction - ReduceLROnPlateau: Reduz a taxa de aprendizado
            early_stopping - EarlyStopping: Para o treinamento se não houver melhoria

    """
    # Configurar callbacks para o treinamento
    checkpoint_MobileNetV2 = ModelCheckpoint(
        f'{pasta_modelo}{MELHOR_MODELO}',
        monitor='val_loss',
        save_best_only=True,
        mode='min',
        verbose=1
    )
    lr_reduction = ReduceLROnPlateau(
        monitor='val_loss',
        mode='min',
        patience=4,
        verbose=1,
        factor=0.1,
        min_lr=1e-6
    )
    early_stopping = EarlyStopping(
        monitor="val_loss",
        mode='min',
        verbose=1,
        patience=10,
        restore_best_weights=True
    )
    return checkpoint_MobileNetV2, lr_reduction, early_stopping


# Função para retornar os callbacks para o ajuste fino
def retorno_chamada_finetune(pasta_modelo):
    """
    Retorna os callbacks para a etapa do ajuste fino

    Argumentos:
            pasta_modelo - str: Caminho para salvar o modelo

    Retorno:
            checkpoint_finetune - ModelCheckpoint: Salva o melhor modelo
            lr_reduction_fine - ReduceLROnPlateau: Reduz a taxa de aprendizado
            early_stopping_fine - EarlyStopping: Para o treinamento se não houver melhoria

    """
    checkpoint_finetune = ModelCheckpoint(
        f'{pasta_modelo}{MELHOR_MODELO_AJUSTE}',
        monitor='val_loss',
        save_best_only=True,
        mode='min',
        verbose=1
    )
    lr_reduction_fine = ReduceLROnPlateau(
        monitor='val_loss',
        patience=6,
        verbose=1,
        factor=0.1,
        min_lr=1e-9
    )
    early_stopping_fine = EarlyStopping(
        monitor="val_loss",
        patience=13,
        restore_best_weights=True
    )
    return checkpoint_finetune, lr_reduction_fine, early_stopping_fine
