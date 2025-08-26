from django.contrib import admin
from .models import Luta, WebhookPayload
import json


@admin.register(Luta)
class LutaAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'id_evento',
                    'numero',
                    'tapete',

                    # Atleta 1
                    'id_atleta1',
                    'atleta1_flag_injured',
                    'atleta1_flag_seeded',
                    'atleta1_draw_rank',
                    'atleta1_RobinRank',
                    'atleta1_ranking_point',

                    # Atleta 2
                    'id_atleta2',
                    'atleta2_flag_injured',
                    'atleta2_flag_seeded',
                    'atleta2_draw_rank',
                    'atleta2_RobinRank',
                    'atleta2_ranking_point',

                    # Resultado
                    'flag_finalizado',
                    'id_atleta_ganhador',
                    'resultado',
                    'tipo_vitoria',

                    # Categoria e estilo
                    'sportAlternateName',
                    'weightCategoryName',
                    'id_classe_peso',
                    'audienceName',
                    'round',

                    # Datas
                    'data_inicio',
                    'data_fim',
                    )
    list_filter = ('sportAlternateName', 'weightCategoryName', 'round', 'tapete', 'audienceName')
    search_fields = ('id_atleta1', 'id_atleta2', 'id_atleta_ganhador')

@admin.register(WebhookPayload)
class WebhookPayloadAdmin(admin.ModelAdmin):
    list_display = ('id', 'received_at', 'short_payload')
    list_filter = ('received_at',)
    search_fields = ('payload',)

    # Mostrar um resumo do JSON no admin
    def short_payload(self, obj):
        # Formata o JSON e mostra só as primeiras 100 chars
        return json.dumps(obj.payload, ensure_ascii=False)

    short_payload.short_description = 'Payload'